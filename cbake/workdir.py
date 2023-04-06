from xdg_base_dirs import xdg_cache_home
import hashlib
import pathlib


def get_workdir(base_dir: pathlib.Path = None) -> pathlib.Path:
    if base_dir is None:
        base_dir = xdg_cache_home() / "cbake"

    if not base_dir.exists():
        base_dir.mkdir()

    cwd = pathlib.Path.cwd()

    dir_hash = hashlib.md5(str(cwd).encode("utf-8")).hexdigest()

    rv = base_dir / (cwd.name + "_" + dir_hash)

    return rv


def init_workdir(workdir: pathlib.Path):
    if not workdir.exists():
        workdir.mkdir()
        (workdir / ".cbake_lock").touch()
    else:
        raise RuntimeError(f"Attempted to create working directory {workdir}, but it already exists.")


def check_workdir(workdir: pathlib.Path):
    if workdir.is_dir():
        if (workdir / ".cbake_lock").is_file():
            return workdir
        else:
            raise RuntimeError(
                f"Target workdir {workdir} exists, but is not a CBake workdir!"
            )
    else:
        raise RuntimeError(
            f"Target workdir {workdir} is not a directory!"
        )
