# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

This is the code repository for {{ cookiecutter.project_name }}.


## Installation

{{ cookiecutter.project_name }} relies on Conda for virtual environments. You can install Conda through either the [Miniconda]() or [Anaconda]() installers. While developer dependencies are handled by Conda, the actual dependecies of {{ cookiecutter.project_name }} are managed by Pip. This is to make the use of Docker as streamlined as possible - plain Python Docker images are much smaller than the corresponding Conda Docker images.

To install {{ cookiecutter.project_name }} locally is therefore a three-step process:

1. Create a new Conda environment with the necessary packages:

        $ conda env create -n {{ cookiecutter.conda_environment }} -f environment.yml
        $ conda activate {{ cookiecutter.repo_name }}

2. Install dependencies with Pip:

        $ python -m pip install -r requirements.txt

3. Install {{ cookiecutter.project_name }}. The `-e` option installs the package in _editable_ mode, meaning that you can change the source code:

        $ python -m pip install -e .


## Running {{ cookiecutter.project_name }}

{{ cookiecutter.project_name }} is installed as an executable, named `{{ cookiecutter.exe_name }}`. 

To get help about the program, run the executable:

    $ {{ cookiecutter.exe_name }} --help

You can change the help text by changing the doc-string in `{{ cookiecutter.repo_name }}/__main__.py`.


# Pipelines

{{ cookiecutter.project_name }} is organized by pipelines. The default pipeline is `{{ cookiecutter.default_pipeline }}`. You can add other pipelines by adding a files into the `{{ cookiecutter.repo_name }}/pipelines` directory.


## {{ cookiecutter.default_pipeline }}

TODO: Describe {{ cookiecutter.default_pipeline }} pipeline


# Development

This section describes the organization and developer tools associated with
{{ cookiecutter.project_name }}.


## Code Style

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Use [Black](https://github.com/python/black). Black can be run on the command
line:

    $ black {{ cookiecutter.repo_name }}

Even better is to set Black to be automatically run whenever you save a file. In Visual Studio Code, you can set this up as follows:

1. Ctrl-Shift P, search "settings" and click _Preferences: Open Settings (UI)_
2. Search "black", then

    - _Python > Formatting: Provider_ - Choose "black"

3. Search "format", then

    - _Editor: Format on Save_ - Click to enable

Similar options are available for other IDEs, see [github.com/python/black#editor-integration](https://github.com/python/black#editor-integration)

A configuration for Flake8 is available in `setup.cfg` that is compatible with Black. You can set Flake8 as your default linter in Visual Studio Code and other IDEs.


## Source Code

The source code of {{ cookiecutter.project_name }} is stored within the {{ cookiecutter.repo_name }} directory.

### `{{ cookiecutter.repo_name }}/__main__.py`

This file contains the entry point of the executable `{{ cookiecutter.exe_name }}`. Additionally, the docstring at the top of the file is used as the help text for the program.

The command line interface is provided by [Typer](https://typer.tiangolo.com/). You can add or change arguments and options by changing the parameters to the `run_model()` function.


### `{{ cookiecutter.repo_name }}/__init__.py`

This file contains meta-information about the project such as the (base) name of the executable, the version of the program, and a list of maintainers.

You can add maintainers to the `AUTHORS` list in this file.

Use the [Bumpversion tool](https://pypi.org/project/bumpversion/) to change the version. Bumpversion handles updating the version number in all relevant files. If you mention the version number in any file, you should add the filename to `.bumpversion.cfg`. You can access the version number programmatically as follows:

    >>> import {{ cookiecutter.repo_name }}
    >>> print({{ cookiecutter.repo_name }}.__version__)
    {{ cookiecutter.version }}

To update the version using Bumpversion, do one of the following:

    $ bumpversion patch
    $ bumpversion minor
    $ bumpversion major

These will increase the patch-, minor-, or major-part of the version number, respectively.


### `{{ cookiecutter.repo_name}}/config`

Configuration files are stored in the `{{ cookiecutter.repo_name }}/config` directory. They are in the [TOML-format](https://toml.io/), and read by the [`toml`](https://pypi.org/project/toml/) package.

To access a configuration setting in your program, you should use `config` as follows:

    >>> from {{ cookiecutter.repo_name }} import config
    >>> config.{{ cookiecutter.repo_name }}.{{ cookiecutter.default_pipeline }}.stages
    ( ..., ... )

Note that you access values through the structure of the configuration file.


See [PyConfs](https://pypi.org/project/pyconfs/) for more information about configurations.

You can also add other configuration files to {{ cookiecutter.project_name }}. Add the `.toml` files to the same `{{ cookiecutter.repo_name }}/config` directory. You can read the config file once by doing:

    >>> from {{ cookiecutter.repo_name }} import config
    >>> cfg = config.read_config("my_new_config")

This will read from `my_new_config.toml`. You can also include this configuration in the `config` module by adding the following line at the bottom of `{{ cookiecutter.repo_name }}/config/__init__.py`:

    my_new_config = config.read_config("my_new_config")

You can have local configuration files that override the regular configuration settings. This is for instance useful when you are testing or developing certain features, but don't want those settings to be commited to GitHub or deployed to production.

For any configuration file `my_config.toml`, you can create a corresponding `my_config_local.toml` with a `_local` suffix. Any settings defined in the local configuration file will override the corresponding setting in the regular configuration file. However, the local configuration file will be ignored by Git and if/when building a Docker image.

### `{{ cookiecutter.repo_name}}/utils`

The `{{ cookiecutter.repo_name}}/utils` directory contains utility modules that
are typically useful all over {{ cookiecutter.project_name }}.

To log messages, you can do the following:

    >>> from {{ cookiecutter.repo_name }}.utils.log import logger
    >>> logger.info(f"The magic word is {magic_word}")

The `logger` is based on [Loguru](https://github.com/Delgan/loguru). Each message is logged at a specific level (the example above logs at the INFO level). When running {{ cookiecutter.project_name }} you can choose at which level messages will be shown. Loguru defines some [default logging levels](https://loguru.readthedocs.io/en/stable/api/logger.html#levels), but there are additional levels defined in `{{ cookiecutter.repo_name }}/utils/log.py` as well.

You can change the active log level--for example to DEBUG--at the command line:

    $ {{ cookiecutter.exe_name }} ... --log-level debug

To see all log levels that have been defined, you can do:

    $ {{ cookiecutter.exe_name }} --show-log-levels


## Docker Support

The `Dockerfile` can be used to build a Docker image for {{ cookiecutter.project_name }}. Build the image as follows:

    $ docker build -t {{ cookiecutter.repo_name }} .

The image can be run using:

    $ docker run --rm {{ cookiecutter.repo_name }}
