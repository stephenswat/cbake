import xdg_base_dirs
import pydantic
import pathlib


class Settings(pydantic.BaseSettings):
    cache_dir: pathlib.Path = xdg_base_dirs.xdg_cache_home() / "cbake"
