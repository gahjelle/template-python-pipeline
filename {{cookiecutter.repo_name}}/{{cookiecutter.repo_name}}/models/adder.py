"""Add a number to the given model

Plug-ins are defined using @pyplugs.register on the function that is the entry
point to the plug-in.
"""

# Third party imports
import pyplugs

# {{ cookiecutter.project_name }} imports
from {{ cookiecutter.repo_name }} import config

# Configuration of plug-in
CFG = config.get(__name__)


@pyplugs.register
def add(data, number, ignore_keys=None):
    """Add number to the given model"""
    ignore_keys = set(CFG.ignore_keys if ignore_keys is None else ignore_keys)

    for key in data.keys():
        if key in ignore_keys:
            continue
        data[key] += number

    return data
