import logging
import os
import tarfile

from .constants import APP_NAME
from .fileutils import (copy_files_to_container, create_directory,
                        norm_path_with_work_dir, put_archive)
from .layer import ImageLayer
from .output import CHAPTER, ERROR_SUBTITLE
from .utilclasses import CommandLog
from .utils import substitute_variables

logger = logging.getLogger(APP_NAME)


class Command:
    def __init__(self, value, content, layer_config, build_context):
        self.value = value
        self.layer_config = layer_config
        self._content = content
        self._build_context = build_context
        self._log = CommandLog(command=self._content)
        self.layer_config.add_log(self._log)

    @staticmethod
    def changes_data():
        pass

    def apply(self, client, config):
        pass

    def __str__(self):
        return "{} {}".format(self.__class__.__name__, self.value)

    def __call__(self, client, config):
        logger.info(CHAPTER.format(self._content))
        self.value = substitute_variables(text=self.value,
                                          variables=self.layer_config.envs)
        self.apply(client, config)


class Arg(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, config):
        value_split = self.value.split('=')

        if len(value_split) == 1:
            key, default_value = value_split[0], ""
        elif len(value_split) == 2:
            key, default_value = value_split
        else:
            raise Exception("Wrong format of ARG command.")

        self.layer_config.envs[key] = config.buildargs.get(key, default_value)
        config.mark_used_buildarg(key=key)


class Copy(Command):
    @staticmethod
    def changes_data():
        return True

    def apply(self, client, config):
        splited_command = self.value.split()
        if len(splited_command) < 2:
            logger.warning('Wrong command: {}'.format(str(self.value)))
            return
            # exception?

        source_files = splited_command[0:-1:]
        target_path = norm_path_with_work_dir(path=splited_command[-1],
                                              workdir=self.layer_config.workdir)
        copy_files_to_container(container=self.layer_config.current_container,
                                client=client,
                                config=config,
                                context=self._build_context,
                                source=source_files,
                                target=target_path)


class Add(Command):
    @staticmethod
    def changes_data():
        return True

    def apply(self, client, config):
        splited_command = self.value.split()
        if len(splited_command) < 2:
            logger.warning('Wrong command: {}'.format(str(self.value)))
            return
            # exception?

        source_files = splited_command[0:-1:]
        target_path = norm_path_with_work_dir(path=splited_command[-1],
                                              workdir=self.layer_config.workdir)

        for src in source_files:
            file = self._build_context.get_file(src)
            if file:
                try:
                    with tarfile.open(fileobj=file):
                        put_archive(client=client,
                                    config=config,
                                    container=self.layer_config.current_container,
                                    tar=file,
                                    target=target_path)
                        break
                except:
                    pass
            copy_files_to_container(container=self.layer_config.current_container,
                                    client=client,
                                    config=config,
                                    context=self._build_context,
                                    source=[src],
                                    target=target_path)


class Cmd(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, config):
        self.layer_config.add_property("Cmd", self.value)


class Env(Command):
    @staticmethod
    def changes_data():
        return False


class Expose(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, config):
        self.layer_config.add_to_dictionary("ExposedPorts", self.value, {})


class From(Command):
    @staticmethod
    def changes_data():
        return False


class Label(Command):
    @staticmethod
    def changes_data():
        return False


class Maintainer(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, config):
        self.layer_config.author = self.value


class Run(Command):
    @staticmethod
    def changes_data():
        return True

    def apply(self, client, config):

        if self.layer_config.workdir and self.layer_config.workdir != os.curdir:
            command = "sh -c \"cd {}; {}\"".format(self.layer_config.workdir, self.value)
        else:
            command = self.value

        for l in client.execute(container=self.layer_config.current_container,
                                cmd=command):
            logger.debug(str(l.decode().rstrip()))
            self._log.add_log(l)
        logger.debug("")


class User(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, config):
        self.layer_config.add_property("User", self.value)


class Workdir(Command):
    @staticmethod
    def changes_data():
        return False

    def apply(self, client, config):
        self.layer_config.workdir = self.value
        create_directory(client=client,
                         config=config,
                         container=self.layer_config.current_container,
                         target=self.layer_config.workdir)


COMMANDS = {
    "ADD": Add,
    "ARG": Arg,
    "CMD": Cmd,
    "COPY": Copy,
    "ENV": Env,
    "EXPOSE": Expose,
    "FROM": From,
    # "LABEL": Label,
    "MAINTAINER": Maintainer,
    "RUN": Run,
    "USER": User,
    "WORKDIR": Workdir
}


def get_layers_from_dockerfile_structure(structure, layers_split_mark, build_context):
    if layers_split_mark is None or layers_split_mark == []:
        layers_split_mark = [i for i in range(len(structure))]

    if layers_split_mark[-1] != len(structure):
        layers_split_mark.append(len(structure))

    logger.debug(CHAPTER.format("layer splits: {}".format(layers_split_mark)))

    for l in layers_split_mark:
        if l > len(structure):
            raise Exception("Layer split {} is bigger then number of instructions ({})."
                            .format(l, len(structure)))

    layers = []
    current_command = 0
    layer_number = 1
    layer = ImageLayer(number=0)
    data_changed = False
    for layer_split in layers_split_mark:

        for i in range(current_command, layer_split):
            cmd = structure[i]
            instruction = cmd["instruction"]
            cmdType = COMMANDS.get(instruction)
            if not cmdType:
                logger.warning(ERROR_SUBTITLE.format("Unknown instruction {}.".format(instruction)))
            else:
                layer.add_command(command=cmdType(value=cmd["value"],
                                                  content=cmd['content'],
                                                  layer_config=layer.conf,
                                                  build_context=build_context),
                                  content=cmd['content'])

                current_command += 1
                data_changed = data_changed or cmdType.changes_data()

        if data_changed or layer_split == len(structure):
            layers.append(layer)
            if not layer_split == len(structure):
                layer = ImageLayer(number=layer_number)
                layer_number += 1
            else:
                layer.is_last = True

    return layers
