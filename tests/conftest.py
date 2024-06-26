import unittest.mock

import pytest
from httpx import AsyncClient, ASGITransport

from src.config.settings import Settings
from src.main import app


@pytest.fixture(scope="session")
def fixture_override_settings() -> Settings:

    class OverrideSettings(Settings, env_file=".env.test"):
        def __init__(self):
            super().__init__()
            self.database.mongo_db_name = "test_db"

            self.application.url_scheme = "https"
            self.application.hostname = "test.host.com"

    test_settings = OverrideSettings()

    yield test_settings


@pytest.fixture()
def fixture_fake_get_setting(fixture_override_settings):
    with unittest.mock.patch("src.config.get_settings") as mock:
        mock.return_value = fixture_override_settings
        yield mock


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
