[![build status](https://gitlab.com/lachmanfrantisek/incubator/badges/master/build.svg)](https://gitlab.com/lachmanfrantisek/incubator/commits/master)
[![coverage report](https://gitlab.com/lachmanfrantisek/incubator/badges/master/coverage.svg)](https://gitlab.com/lachmanfrantisek/incubator/commits/master)
[![License: MIT](https://img.shields.io/pypi/l/incubator.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/documentation-pdoc-green.svg)](https://lachmanfrantisek.gitlab.io/incubator/)

-------

[![PyPI - incubator](https://img.shields.io/pypi/v/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/status/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/pyversions/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/format/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/wheel/incubator.svg)](https://pypi.python.org/pypi/incubator/)
[![PyPI - incubator](https://img.shields.io/pypi/implementation/incubator.svg)](https://pypi.python.org/pypi/incubator/)

-------

# Incubator

**Python library and command line interface for building container images in better and more secure way.**

With Incubator you can:

* precisely control layering of the image
* mounting build-time volumes (for secrets present only during the build)
* better metadata handling
* use standard *Dockerfile* (extended functionality is defined externally)

Documentation can be found at [lachmanfrantisek.gitlab.io/incubator/](https://lachmanfrantisek.gitlab.io/incubator/).

Want to test it without any installation? Try our interactive tutorial at [KataCoda](https://www.katacoda.com/incubator/scenarios/tutorial). The web browser is everything you need.


## Installation

Installation can be done with following commands:

- Using `pip`:
```bash
pip install incubator
```

- From source:
```bash
git clone https://lachmanfrantisek@gitlab.com/lachmanfrantisek/incubator.git
cd incubator
python setup.py install
#
# update
git pull
python setup.py install
```

- Via *Docker* image:

```bash
$ docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/app:z --privileged=true \
    registry.gitlab.com/lachmanfrantisek/incubator

[root@5d7845db4d12 /]# incubator
Usage: incubator [OPTIONS] COMMAND [ARGS]...

  Incubator is an alternative image builder for docker containers.

Options:
  -V, --version
  -h, --help     Show this message and exit.

Commands:
  build  Alternative to docker build command.
```

The provided image also provides *ipython* to test the python interface:

```python
$ docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/app:z --privileged=true \
    registry.gitlab.com/lachmanfrantisek/incubator ipython

In [1]: from incubator.api import build

In [2]: import six

In [3]: dockerfile = six.BytesIO("FROM fedora:25\nRUN echo \"hello\"\nRUN echo \"world\"".encode())

In [4]: result = build(fileobj=dockerfile)

In [5]: result.id
Out[5]: 'sha256:2d84f4a77bc35c1d484a146a5107408240ce65a23a30208c45c87affdba02d8a'

In [6]: for cmd_log in result.logs:
   ...:     print(cmd_log.logs)
   ...:     
['hello']
['world']

```

## Usage

Incubator is accessible as a *command-line* tool `incubator` as well as the python module `incubator`

### CLI

Commandline utility for incubator is called `incubator`.

```bash
$ incubator 
Usage: incubator [OPTIONS] COMMAND [ARGS]...

  Incubator is an alternative image builder for docker containers.

Options:
  -V, --version
  -h, --help     Show this message and exit.

Commands:
  build  Alternative to docker build command.

```

```bash
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
```bash
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
