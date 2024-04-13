import pytest
from starlette import status

from src.enums import ResponseStatusEnum


@pytest.mark.anyio
async def test_endpoint__get_common(client):

    response = await client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == ResponseStatusEnum.OK
