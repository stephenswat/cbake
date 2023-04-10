import typer
import pathlib
import rich
from xdg_base_dirs import xdg_cache_home, xdg_config_home

import cbake
import cbake.workdir
import cbake.config
import cbake.exceptions


DEFAULT_INSTANCE = "default"


cli = typer.Typer(
    help="CBake is a CMake wrapper script that helps you manage multiple builds concurrently."
)
state = {"verbose": False, "config": None}


@cli.command()
def init():
    """
    Create a working directory associated with the current project.
    """
    print(state["config"])
    workdir = cbake.workdir.get_workdir(state["config"].cache_dir, pathlib.Path.cwd())
    cbake.workdir.init_workdir(workdir)

    rich.print(f"[bold green]Success:[/] Working directory {workdir} initialized!")


@cli.command()
def deinit():
    """
    Delete the working directory associated with the current project.

    This method must be called in the exact project directory. Parent directories are not considered.
    """
    workdir = cbake.workdir.get_workdir(state["config"].cache_dir, pathlib.Path.cwd())
    cbake.workdir.deinit_workdir(workdir)

    rich.print(f"[bold green]Success:[/] Working directory {workdir} deleted!")


@cli.command()
def status():
    """
    Print the status of the current project.
    """
    project_dir = cbake.workdir.find_project_dir(state["config"].cache_dir)
    workdir = cbake.workdir.get_workdir(state["config"].cache_dir, project_dir)
    cbake.workdir.check_workdir(workdir)

    rich.print(f"[blue]Project directory[/] is {project_dir}")
    rich.print(f"[blue]Working directory[/] is {workdir}")

    instances = cbake.workdir.get_instances(workdir)

    if len(instances) > 0:
        rich.print(f"This project has {len(instances)} instance(s):")
        for i in instances:
            rich.print(f" - [yellow]{i.name}[/]")
    else:
        rich.print(f"This project has no instances. Go make some!")


@cli.command()
def add(
    name: str = typer.Argument(DEFAULT_INSTANCE),
    freeze: bool = False,
    force: bool = False,
    isolate: bool = False,
    settings: list[str] = typer.Option([], "-D"),
):
    """
    Add a new instance with a set of configuration parameters.
    """

    # TODO: Support freezing

    project_dir = cbake.workdir.find_project_dir(state["config"].cache_dir)
    workdir = cbake.workdir.get_workdir(state["config"].cache_dir, project_dir)
    cbake.workdir.check_workdir(workdir)

    try:
        cbake.workdir.add_instance(workdir, name)
        rich.print(f"[bold green]Success:[/] Instance [yellow]{name}[/] created.")
    except cbake.exceptions.InstanceExistsException:
        if force:
            cbake.workdir.remove_instance(workdir, name)
            rich.print(
                f"[bold blue]Information:[/] Overriding existing instance [yellow]{name}[/]."
            )
            cbake.workdir.add_instance(workdir, name)
            rich.print(f"[bold green]Success:[/] Instance [yellow]{name}[/] created.")
        else:
            rich.print(
                f"[bold red]Error:[/] Instance [yellow]{name}[/] already exists; try [cyan]--force[/]?"
            )


@cli.command()
def remove(name: str, yes: bool = False):
    """
    Remove a given instance.
    """

    project_dir = cbake.workdir.find_project_dir(state["config"].cache_dir)
    workdir = cbake.workdir.get_workdir(state["config"].cache_dir, project_dir)
    cbake.workdir.check_workdir(workdir)

    if name == "ALL":
        targets = [i.name for i in cbake.workdir.get_instances(workdir)]

        if len(targets) == 0:
            rich.print(f"[bold blue]Information:[/] There are no instances to delete!")
            raise typer.Abort()
    else:
        targets = [name]

    if not yes:
        if len(targets) > 1:
            rich.print(
                f"[bold magenta]Warning:[/] This will delete {len(targets)} instances!"
            )
        else:
            rich.print(
                f"[bold magenta]Warning:[/] This will delete the [yellow]{targets[0]}[/] instance!"
            )

        conf = typer.confirm(
            "Are you sure you want to delete the aforementioned instances?"
        )

        if not conf:
            raise typer.Abort()

    rich.print(f"[bold blue]Information:[/] Deleting {len(targets)} instance(s).")

    for t in targets:
        cbake.workdir.remove_instance(workdir, t)


@cli.command()
def clean(name: str = typer.Argument(DEFAULT_INSTANCE)):
    """
    Cleans out a given instance, requiring reconfiguration.
    """
    print(name)


@cli.command()
def configure(name: str = typer.Argument(DEFAULT_INSTANCE)):
    """
    Generate or regenerate a build system for a given instance.
    """
    print(name, settings)


@cli.command()
def build(name: str, args: list[int]):
    """
    Build the code for a given instance.
    """
    print(xdg_cache_home())
    print(xdg_config_home())
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@cli.command()
def inspect(name: str = typer.Argument(DEFAULT_INSTANCE)):
    """
    Print information about a given instance.
    """
    print(xdg_cache_home())
    print(xdg_config_home())
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@cli.command()
def about(version: bool = False):
    if version:
        print(cbake.__version__)
    else:
        rich.print(f"[bold]CBake[/] version [bold green]v{cbake.__version__}[/]")

@cli.command(hidden=True)
def cake():
    """
    Prints a nice cake. What else is there to say?
    """
    rich.print("   [bold yellow], , , , , ,[/]")
    rich.print("   [bold]| | | | | |[/]")
    rich.print("  [bold orange_red1]@$@$@$@$@$@$@[/]")
    rich.print("  [bold orange_red1]|[/]           [bold orange_red1]|[/]")
    rich.print("[bold orange_red1]@$@$@$@$@$@$@$@$@[/]")
    rich.print("[bold orange_red1]|[/]     CBake     [bold orange_red1]|[/]")
    rich.print("[bold orange_red1]@$@$@$@$@$@$@$@$@[/]")


@cli.callback()
def main(verbose: bool = False, config: pathlib.Path = None):
    if verbose:
        state["verbose"] = True

    state["config"] = cbake.config.get_config(config)
