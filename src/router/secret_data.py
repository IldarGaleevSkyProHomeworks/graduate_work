import logging
from typing import Annotated

from fastapi import APIRouter, Header, Path, Body
from starlette import status

from src.exceptions import AppHTTPException
from src.schemas import (
    CreateSecretRequestSchema,
    CreateSecretResponseSchema,
    GetSecretResponseSchema,
    ExceptionSchema,
)
from src.services import UserSecret

router = APIRouter(tags=["secret"])
logger = logging.getLogger(__name__)


@router.post("/generate")
async def create_secret_handler(
    data: Annotated[
        CreateSecretRequestSchema,
        Body(),
    ],
) -> CreateSecretResponseSchema:
    try:
        return await UserSecret.create_item(
            data,
        )
    except Exception as e:
        logger.error(e)
        raise AppHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Secret create failed",
        )


@router.get(
    "/secrets/{secret_id}",
    responses={404: {"model": ExceptionSchema}},
)
async def get_secret_handler(
    secret_id: Annotated[
        str,
        Path(
            max_length=24,
        ),
    ],
    secret_key: Annotated[
        str,
        Header(
            alias="secret_key",
            max_length=100,
        ),
    ],
) -> GetSecretResponseSchema:
    return await UserSecret.get_item_by_id(secret_id, secret_key)
