from unittest import mock

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.repository import UserSecret


@pytest.fixture(scope="module")
def fixture_override_db():

    class FakeDBContext:

        def __init__(self, *args, **kwargs):

            def create_index(*ci_args, **ci_kwargs):
                assert ci_args[0] == {"expireAt": 1}
                assert ci_kwargs["expireAfterSeconds"] == 0

            self.get_collection_mock = mock.MagicMock()
            self.get_collection_mock.create_index = mock.AsyncMock()
            self.get_collection_mock.create_index.side_effect = create_index

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        def get_collection(self, *args, **kwargs):
            assert args[0] == UserSecret.COLLECTION_NAME
            return self.get_collection_mock

    with mock.patch(
        "src.database.mongodb.get_db_context",
    ) as mk:
        mk.return_value = FakeDBContext()
        yield mk


def test_lifespan(
    fixture_fake_get_setting,
    fixture_override_db,
):
    with TestClient(app):
        pass
