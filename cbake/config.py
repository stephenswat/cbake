import tomllib
import pathlib
import os
import xdg_base_dirs

import cbake.schema.settings


def get_config(config: pathlib.Path = None) -> cbake.schema.settings.Settings:
    if config is None:
        config = xdg_base_dirs.xdg_config_home() / "cbake.toml"
        error_on_missing = False
    else:
        error_on_missing = True

    if os.path.isfile(config):
        return Settings(tomllib.load(config))
    elif error_on_missing:
        raise RuntimeError(f"Config file {config} does not exist!")
    else:
        return cbake.schema.settings.Settings()
