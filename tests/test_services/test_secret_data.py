import unittest.mock

import pytest
from fastapi import HTTPException
from starlette import status

from src import repository, services, schemas, models
from tests import testing_data
from unittest import mock


class FakeRepo(repository.RepositoryItem):
    async def write_item(
        self,
        item: models.UserSecret,
    ) -> models.UserSecret:
        self._last_index += 1
        new_id = testing_data.GENERATED_SECRET_ID.format(self._last_index)
        self._database[new_id] = item
        item.id = new_id
        return item

    async def get_item_by_id(
        self,
        item_id: str,
    ) -> models.UserSecret | None:
        if item_id in self._database:
            return self._database[item_id]
        return None

    async def delete_item(
        self,
        item: models.UserSecret,
    ) -> models.UserSecret:
        pass

    def __init__(self):
        self._database = {}
        self._last_index = 0
        self._database[testing_data.GENERATED_SECRET_ID.format(0)] = (
            testing_data.USER_SECRET_TEST_DATA_1
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture()
def fixture_fake_repo():
    with unittest.mock.patch("src.repository.UserSecret") as mk:
        mk.return_value = FakeRepo()
        yield mk


@pytest.fixture(scope="module")
def fixture_fake_crypto_decrypt():

    def decrypt(data: bytes, pwd: str) -> str:
        text = data.decode("utf-8")
        d_data, d_pwd = text.split("__")
        if d_pwd != pwd:
            raise ValueError()
        return d_data

    with mock.patch("src.utils.crypto.decrypt") as mk:
        mk.side_effect = decrypt
        yield mk


@pytest.fixture(scope="module")
def fixture_fake_crypto_encrypt():
    with mock.patch("src.utils.crypto.encrypt") as mk:
        mk.side_effect = lambda data, pwd: f"{data}__{pwd}".encode("utf-8")
        yield mk


@pytest.fixture()
def fixture_fake_token():
    with mock.patch("secrets.token_urlsafe") as mk:
        mk.return_value = testing_data.GENERATED_SECRET_KEY
        yield mk


@pytest.mark.services
async def test_create_item(
    fixture_fake_repo,
    fixture_fake_get_setting,
    fixture_fake_crypto_encrypt,
    fixture_fake_token,
):

    data = schemas.CreateSecretRequestSchema(
        message=testing_data.STRING_TEST_DATA_1,
    )

    new_item = await services.UserSecret.create_item(
        data=data,
    )

    assert new_item.secret_key == testing_data.GENERATED_SECRET_KEY
    assert new_item.secret_id == testing_data.GENERATED_SECRET_ID.format(1)


@pytest.mark.services
async def test_get_item_by_id__exists__return_item(
    fixture_fake_repo,
    fixture_fake_get_setting,
    fixture_fake_crypto_decrypt,
    fixture_fake_token,
):
    item_exists = await services.UserSecret.get_item_by_id(
        testing_data.GENERATED_SECRET_ID.format(0),
        testing_data.GENERATED_SECRET_KEY,
    )

    assert item_exists.data == testing_data.STRING_TEST_DATA_1


@pytest.mark.services
async def test_get_item_by_id__not_exists__return__http_404(
    fixture_fake_repo,
    fixture_fake_get_setting,
    fixture_fake_crypto_decrypt,
    fixture_fake_token,
):

    with pytest.raises(HTTPException) as ex_info:
        await services.UserSecret.get_item_by_id(
            testing_data.GENERATED_SECRET_ID.format(99),
            testing_data.GENERATED_SECRET_KEY,
        )

    assert ex_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.services
async def test_get_item_by_id__wrong_secret_key__return_http_403(
    fixture_fake_repo,
    fixture_fake_get_setting,
    fixture_fake_crypto_decrypt,
    fixture_fake_token,
):

    with pytest.raises(HTTPException) as ex_info:
        await services.UserSecret.get_item_by_id(
            testing_data.GENERATED_SECRET_ID.format(0),
            "WrongKey",
        )

    assert ex_info.value.status_code == status.HTTP_403_FORBIDDEN
