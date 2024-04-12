import unittest.mock
from asyncio import sleep

import pytest
from starlette import status

from src.schemas import (
    CreateSecretRequestSchema,
    CreateSecretResponseSchema,
    GetSecretResponseSchema,
)
from tests import testing_data

DB_FAIL_SIGNAL = "DBFail"


@pytest.fixture()
def fixture_override_service_create_item():

    async def create_item(
        data: CreateSecretRequestSchema,
    ) -> CreateSecretResponseSchema:
        if data.message == DB_FAIL_SIGNAL:
            raise Exception()

        await sleep(0)
        return CreateSecretResponseSchema(
            secret_id=testing_data.GENERATED_SECRET_ID,
            secret_key=data.secret_key,
        )

    with unittest.mock.patch("src.services.secret_data.UserSecret.create_item") as mk:
        mk.side_effect = create_item
        yield mk


@pytest.fixture()
def fixture_override_service_get_item_by_id():

    async def get_item(
        secret_id: str,
        secret_key: str,
    ) -> GetSecretResponseSchema:
        await sleep(0)
        return GetSecretResponseSchema(
            data=f"{secret_id}_{secret_key}",
        )

    with unittest.mock.patch(
        "src.services.secret_data.UserSecret.get_item_by_id"
    ) as mk:
        mk.side_effect = get_item
        yield mk


@pytest.mark.anyio
async def test_endpoint__post_generate_success(
    fixture_override_service_create_item,
    client,
):
    response = await client.post(
        "/generate",
        json={
            "message": testing_data.STRING_TEST_DATA_1,
            "secret_key": testing_data.GENERATED_SECRET_KEY,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "ok",
        "secret_id": testing_data.GENERATED_SECRET_ID,
        "secret_key": testing_data.GENERATED_SECRET_KEY,
    }


@pytest.mark.anyio
async def test_endpoint__post_generate_database_failed(
    fixture_override_service_create_item,
    client,
):

    response = await client.post(
        "/generate",
        json={"message": DB_FAIL_SIGNAL},
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.anyio
async def test_endpoint__get_secrets(
    fixture_override_service_get_item_by_id,
    client,
):

    response = await client.get(
        f"/secrets/{testing_data.GENERATED_SECRET_ID}",
        headers={
            "secret_key": testing_data.GENERATED_SECRET_KEY,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "ok",
        "data": f"{testing_data.GENERATED_SECRET_ID}_{testing_data.GENERATED_SECRET_KEY}",
    }
