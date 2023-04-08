from xdg_base_dirs import xdg_cache_home
import hashlib
import pathlib
import shutil

import cbake.exceptions


def get_workdir(base_dir: pathlib.Path, project_dir: pathlib.Path) -> pathlib.Path:
    dir_hash = hashlib.md5(str(project_dir).encode("utf-8")).hexdigest()

    rv = base_dir / (project_dir.name + "_" + dir_hash)

    return rv


def find_project_dir(base_dir: pathlib.Path) -> pathlib.Path:
    cwd = pathlib.Path.cwd().resolve()

    while cwd.parent != cwd:
        dir_hash = hashlib.md5(str(cwd).encode("utf-8")).hexdigest()

        rv = base_dir / (cwd.name + "_" + dir_hash)

        if rv.is_dir() and (rv / ".cbake_lock").is_file():
            return cwd
        else:
            cwd = cwd.parent

    raise RuntimeError(
        f"No working directory matches {pathlib.Path.cwd().resolve()} or any of its parents."
    )


def init_workdir(workdir: pathlib.Path):
    if not workdir.exists():
        workdir.mkdir()
        (workdir / "instances").mkdir()
        (workdir / ".cbake_lock").touch()
    else:
        raise RuntimeError(
            f"Attempted to create working directory {workdir}, but it already exists."
        )


def deinit_workdir(workdir: pathlib.Path):
    if workdir.is_dir() and (workdir / ".cbake_lock").is_file():
        shutil.rmtree(workdir)
    else:
        raise RuntimeError(
            f"Attempted to delete working directory {workdir}, but it is not a working directory."
        )


def check_workdir(workdir: pathlib.Path):
    if workdir.is_dir():
        if (workdir / ".cbake_lock").is_file():
            return workdir
        else:
            raise RuntimeError(
                f"Target workdir {workdir} exists, but is not a CBake workdir!"
            )
    else:
        raise RuntimeError(f"Target workdir {workdir} is not a directory!")


def get_instances(workdir: pathlib.Path):
    return [
        i for i in (workdir / "instances").glob("*/") if (i / "config.toml").is_file()
    ]


def add_instance(workdir: pathlib.Path, name: str):
    ip = workdir / "instances" / name

    if not ip.exists():
        ip.mkdir()
        (ip / "config.toml").touch()
    else:
        raise cbake.exceptions.InstanceExistsException(
            f"Attempting to create instance {name} in {workdir}, but something already exists."
        )


def remove_instance(workdir: pathlib.Path, name: str):
    ip = workdir / "instances" / name

    if ip.is_dir() and (ip / "config.toml").is_file():
        shutil.rmtree(ip)
    else:
        raise RuntimeError(
            f"Attempting to delete instance {name} in {workdir}, but it is not an instance."
        )
