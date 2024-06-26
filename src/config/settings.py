from functools import lru_cache

from pydantic_settings import BaseSettings

from .application import ApplicationSettings
from .database import DatabaseSettings


class Settings(
    BaseSettings,
    env_file=".env",
    env_file_encoding="utf-8",
    extra="allow",
    env_nested_delimiter="__",
):
    application: ApplicationSettings = ApplicationSettings()
    database: DatabaseSettings = DatabaseSettings()


@lru_cache
def get_settings():  # pragma: no cover
    return Settings()
