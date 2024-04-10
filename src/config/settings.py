from functools import lru_cache

from pydantic_settings import BaseSettings

from .application import ApplicationSettings


class Settings(
    BaseSettings,
    env_file=".env",
    env_file_encoding="utf-8",
    extra="allow",
    env_nested_delimiter="__",
):
    application: ApplicationSettings = ApplicationSettings()


@lru_cache
def get_settings():
    return Settings()
