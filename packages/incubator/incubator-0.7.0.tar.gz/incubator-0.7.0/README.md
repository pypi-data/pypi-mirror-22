[![build status](https://gitlab.com/lachmanfrantisek/incubator/badges/master/build.svg)](https://gitlab.com/lachmanfrantisek/incubator/commits/master)
[![coverage report](https://gitlab.com/lachmanfrantisek/incubator/badges/master/coverage.svg)](https://gitlab.com/lachmanfrantisek/incubator/commits/master)
[![License: MIT](https://img.shields.io/pypi/l/incubator.svg)](https://opensource.org/licenses/MIT)

-------

[![PyPI - incubator](https://img.shields.io/pypi/v/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/wheel/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/format/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/status/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/pyversions/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/implementation/incubator.svg)](https://pypi.python.org/pypi/incubator/)

[![PyPI - incubator](https://img.shields.io/pypi/dm/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/dw/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/dd/incubator.svg)](https://pypi.python.org/pypi/incubator/)

-------

Python library and command line interface for building docker images.

## Instalation

Installation can be done with following commands:

- Using `pip`:
```
pip install incubator
```

- From source:
```
git clone https://lachmanfrantisek@gitlab.com/lachmanfrantisek/incubator.git
cd incubator
python setup.py install
#
# update
git pull
python setup.py install
```

## Usage

### Docker image
```
$ docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/app --privileged=true \
    registry.gitlab.com/lachmanfrantisek/incubator
``
In [1]: import incubator.api as ia

In [2]: import six

In [3]: d = six.BytesIO("FROM fedora:25\nRUN touch /tmp/a".encode())

In [4]: ia.build(fileobj=d)
id: None : parent: sha256:19d5ca7afb564ef868001eab5e910c99ab27954b93931c4731fd2da7d5f5f360 : ['FROM fedora:25\n', 'RUN touch /tmp/a']
Out[4]: 'sha256:19d5ca7afb564ef868001eab5e910c99ab27954b93931c4731fd2da7d5f5f360'

```

### CLI

Commandline utility for incubator is called `incubator`.

```
$ incubator 
Usage: incubator [OPTIONS] COMMAND [ARGS]...

  Incubator is an alternative image builder for docker containers.

Options:
  -V, --version
  -h, --help     Show this message and exit.

Commands:
  build  Alternative to docker build command.

```

```
$ incubator build -h
Usage: incubator build [OPTIONS] PATH

  Alternative to docker build command.

  Build process can be controlled  with config file.

Options:
  --build-arg KEY=VALUE           Set build-time variables (default [])
  -c, --cpu-shares INTEGER        CPU shares (relative weight).
  -g, --config FILENAME           File with config.
  --context-file-limit INTEGER    Limit for in-memory context. Default is
                                  0=unlimited.
  --cpuset-cpus TEXT              CPUs in which to allow execution (0-3, 0,1)
  --default-layering              Sets the layering to default behaviour (one
                                  instruction per layer). Overrides --split-
                                  layer.
  -f, --file PATH                 Name of the Dockerfile.
  --force-rm                      Always remove intermediate containers
  -l, --label TEXT                Set metadata for an image (default [])
  -m, --memory TEXT               Memory limit.
  --memory-swap TEXT              Swap limit equal to memory plus swap: '-1'
                                  to enable unlimited swap.
  --no-cache                      Do not use cache when building the image.
  --pull                          Always attempt to pull a newer version of
                                  the image
  -q, --quiet                     Only display ID.
  --rm BOOLEAN                    Remove intermediate containers after a
                                  successful build (default true)
  -s, --split-layer INTEGER RANGE
                                  Make a layer after the instruction with this
                                  number.
  --squash                        Squash all layers to one. Overrides --split-
                                  layer.
  -t, --tag TEXT                  Tag for final image.
  --test-config                   Print only given configuration and exit.
  --verbose                       Be verbose.
  -v, --volume VOLUME             Set build-time bind mounts (default [])
  -h, --help                      Show this message and exit.
```

Bash completion can be activated with: 
```
eval "$(_INCUBATOR_COMPLETE=source incubator)"
```

### Configuration files

The configuration can be loaded from two default files (`~/.incubator.rc` and `./.incubator`), another file(s) can be set with the `--config`/`-g` option.

Example of merging:

Available options for `JSON` configuration files:

- `version` (number) -- version of schema (now `1`)
- `buildargs` (dict) -- build arguments
- `container_limits` (dict) -- limits for build-time containers
- `context_file_limit` (integer>=0) -- Maximum size of in memory config. (0 is unlimited and default)
- `forcerm` (bool) -- always remove intermediate containers, even after unsuccessful builds
- `infinite_command` -- command used as to run container infinitely (default `sh`)
- `labels` (dict) -- labels to add to the image (visible with `docker inspect image_id_or_name`)
- `layers` (array(integer>=0)) -- array of layer splits (each number `i` sets commit between instruction `i` and `i+1`), empty array means default behaviour and splits commit between each instruction, `[0]` can be used to squash all lyaers
- `mkdir_command` (string) -- command used to create directory (recursively) (default `mkdir --parent`)
- `config_name` (string) -- configuration can have name to better error handling
- `pull` (bool) -- downloads the base image even if it is present
- `rm` (bool) -- remove intermediate containers (default `True`)
- `tags` (array(string)) -- tags to set to the image
- `volumes` (array(string)) -- bind (build-time) volumes, `source:destination` or `source:destination:mode` (modes: `ro`, `rw`, `z` and `Z`)

Example of merging:

![Configuration files](./doc/img/config.svg)

![Result of merging](./doc/img/config-result.svg)
