import tomllib
import pathlib
import os
from xdg_base_dirs import xdg_config_home


def get_config(config: pathlib.Path = None) -> dict:
    if config is None:
        config = xdg_config_home() / "cbake.toml"
        error_on_missing = False
    else:
        error_on_missing = True

    if os.path.isfile(config):
        return tomllib.load(config)
    elif error_on_missing:
        raise RuntimeError(f"Config file {config} does not exist!")
    else:
        return {}
