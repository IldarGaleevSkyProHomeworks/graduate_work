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
from src import services

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
        return await services.UserSecret.create_item(
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
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "If a secret key is wrong",
            "model": ExceptionSchema,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "If a secret is not found",
            "model": ExceptionSchema,
        },
    },
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
    return await services.UserSecret.get_item_by_id(secret_id, secret_key)
