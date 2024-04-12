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
