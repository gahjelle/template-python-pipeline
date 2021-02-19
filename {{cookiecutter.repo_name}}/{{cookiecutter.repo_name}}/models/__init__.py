"""Example of a plug-in directory

Plug-ins can be called in the code using something like

    from {{ cookiecutter.repo_name }} import models

    models.run("adder", data={}, number=42)
"""

# Third party imports
import pyplugs


run = pyplugs.call_factory(__package__)
