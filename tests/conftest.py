import unittest

import pytest

from src.config.settings import Settings


@pytest.fixture(scope="session")
def fixture_override_settings() -> Settings:

    class OverrideSettings(Settings, env_file=".env.test"):
        def __init__(self):
            super().__init__()
            self.database.mongo_db_name = "test_db"

    test_settings = OverrideSettings()

    yield test_settings


@pytest.fixture()
def fixture_fake_get_setting(fixture_override_settings):
    with unittest.mock.patch("src.config.get_settings") as mock:
        mock.return_value = fixture_override_settings
        yield mock
