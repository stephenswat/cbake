import typer
import pathlib
import rich
from xdg_base_dirs import xdg_cache_home, xdg_config_home

import cbake.workdir
import cbake.config


cli = typer.Typer()
state = {"verbose": False, "config": None}


@cli.command()
def init():
    workdir = cbake.workdir.get_workdir(state["config"].get("cache_dir", None))
    cbake.workdir.init_workdir(workdir)

    rich.print(f"[bold green]Success:[/] Working directory {workdir} initialized!")


@cli.command()
def status():
    workdir = cbake.workdir.get_workdir(state["config"].get("cache_dir", None))
    cbake.workdir.check_workdir(workdir)

    # TODO: Add warning for uninitialized workdir here.

    rich.print(f"[bold blue]Status:[/] Working directory {workdir}")
    rich.pretty.pprint(["Hello", "world"])


@cli.command()
def configure(name: str, formal: bool = False):
    print(xdg_cache_home())
    print(xdg_config_home())
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@cli.command()
def build(name: str, formal: bool = False):
    print(xdg_cache_home())
    print(xdg_config_home())
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@cli.command()
def run():
    print("Hello")


@cli.callback()
def main(verbose: bool = False, config: pathlib.Path = None):
    if verbose:
        state["verbose"] = True

    state["config"] = cbake.config.get_config(config)
