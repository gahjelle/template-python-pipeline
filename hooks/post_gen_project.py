import shlex
import subprocess

EXECUTE_COMMANDS = "{{ cookiecutter.set_up }}" != "Only create files"


def run_shell_command(description, commands, use_environment):
    """Run the given shell command"""
    if not EXECUTE_COMMANDS:
        print("\n".join(f"    $ {c}" for c in commands))
        return

    line = "-" * (len(description) + 4)
    print(f"\n\n{line}\n  {description}\n{line}\n")

    for command in commands:
        if use_environment:
            command = f"conda run -n {{ cookiecutter.conda_environment }} {command}"

        try:
            subprocess.run(shlex.split(command), check=True)
        except subprocess.CalledProcessError as err:
            print(
                "Setup of {{ cookiecutter.project_name }} failed at "
                f"the command {command!r}\n"
            )
            raise SystemExit(err.returncode)


if not EXECUTE_COMMANDS:
    # Report that files are created
    print("\n\nCreated files for {{ cookiecutter.project_name }}\n")
    print(
        "You should run the following commands yourself to finish setting up the project:\n\n"
        "    $ cd {{ cookiecutter.repo_name }}"
    )


# Set up Conda environment
run_shell_command(
    "Create '{{ cookiecutter.conda_environment }}' conda environment",
    commands=[
        "conda env create -q "
        "-n {{ cookiecutter.conda_environment }} "
        "-f environment.yml"
    ],
    use_environment=False,
)

# Activate the conda environment (This is handled by use_environment when
# running in the hook, but is important when redoing the commands manually)
if not EXECUTE_COMMANDS:
    run_shell_command(
        "Activate the '{{ cookiecutter.conda_environment }}' conda environment",
        commands=["conda activate {{ cookiecutter.conda_environment }}"],
        use_environment=False,
    )

# Use piptools to pin dependencies
run_shell_command(
    "Pin dependencies with Pip-tools",
    commands=["python -m piptools compile requirements.in"],
    use_environment=True,
)

# Install dependencies
run_shell_command(
    "Install required dependencies to '{{ cookiecutter.conda_environment }}'",
    commands=["python -m pip install -r requirements.txt"],
    use_environment=True,
)

# Install package
run_shell_command(
    "Install {{ cookiecutter.project_name }} as '{{ cookiecutter.exe_name }}'",
    commands=["python -m pip install -e ."],
    use_environment=True,
)

# Clean up formatting
run_shell_command(
    "Run black and isort to format code and imports properly",
    commands=["python -m black .", "python -m isort ."],
    use_environment=True,
)

# Report that installation is finished
if EXECUTE_COMMANDS:
    print(
        "\n\nFinished installing {{ cookiecutter.project_name }} "
        "into the '{{ cookiecutter.conda_environment }}' conda environment\n"
    )
    print("Remember to do 'conda activate {{ cookiecutter.conda_environment }}'")
