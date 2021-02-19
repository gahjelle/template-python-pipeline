"""Example of how to use a plugin"""

# Standard library imports
import math

# Third party imports
import pyplugs

# {{ cookiecutter.project_name }} imports
from {{ cookiecutter.repo_name }} import config, models

# Configuration of pipeline
CFG = config.get(__name__)


@pyplugs.register
def read(data, meta):
    """Add information to data"""
    data.name = "{{ cookiecutter.project_name }}"
    data.path = __file__
    data.model_data = {
        "name": CFG.model_name,
        "pi": math.pi,
        "value": 28.1,
        "num_rooms": 4,
    }


@pyplugs.register
def run_model(data, meta):
    """Run a model on the data"""
    models.run(CFG.model_name, data=data.model_data, number=42)


@pyplugs.register
def dump_to_screen(data, meta):
    """Dump infomation to screen"""
    for key, value in data.items():
        print(f"{key:<10} = {value}")
