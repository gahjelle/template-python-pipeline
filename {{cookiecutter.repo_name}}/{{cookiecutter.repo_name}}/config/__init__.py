"""Handle configuration settings in {{ cookiecutter.project_name }}"""

# Standard library imports
import pathlib

# Third party imports
import dotenv
from pyconfs import Configuration

# Read environment variables from an optional .env file
dotenv.load_dotenv()

# Base directory for the {{ cookiecutter.repo_name }} package
_BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# Prioritized list of possible locations for all {{ cookiecutter.project_name }} config files
_CONFIG_DIRECTORIES = (
    pathlib.Path.cwd(),
    pathlib.Path.home() / ".{{ cookiecutter.repo_name }}",
    _BASE_DIR / "config",
)

# Pointers to existing configurations
_CFGS = {}


def read_config(cfg_name: str) -> Configuration:
    """Read one configuration from file

    Args:
        cfg_name:  Name of configuration, used for documentation

    Returns:
        A configuration object
    """
    if cfg_name not in _CFGS:
        cfg = _CFGS[cfg_name] = Configuration(cfg_name)
        for file_path in config_paths(cfg_name):
            cfg.update_from_file(file_path)

    return _CFGS[cfg_name]


def config_paths(cfg_name: str) -> pathlib.Path:
    """Yield all files that contain the given configuration"""
    file_names = (f"{cfg_name}.toml", f"{cfg_name}_local.toml")

    for file_name in file_names:
        for file_dir in _CONFIG_DIRECTORIES:
            file_path = file_dir / file_name
            if file_path.exists():
                yield file_path
                break


def get(module_name: str):
    """Get the configuration for the given module"""
    cfg, *sections = module_name.split(".")
    return _CFGS.get(cfg, Configuration()).get(sections, Configuration())


# Read configuration from file, update paths and from environment variables
{{ cookiecutter.repo_name }} = read_config("{{ cookiecutter.repo_name }}")
{{ cookiecutter.repo_name }}.vars.update(
    {
        "path_home": str(pathlib.Path.home()),
        "path_{{ cookiecutter.repo_name }}": str(_BASE_DIR),
        **{f"path_{k}": v for k, v in {{ cookiecutter.repo_name }}.paths.entries},
    }
)
{{ cookiecutter.repo_name }}.update_from_env(
    {
        "LOG_LEVEL": ("log", "console", "level"),
        "JSON_LOGS": ("log", "console", "json_logs"),
    },
    converters={"JSON_LOGS": "bool"},
    prefix="{{ cookiecutter.repo_name|upper }}",
)
