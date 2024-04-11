from datetime import datetime, timedelta
from secrets import token_urlsafe

from fastapi import HTTPException
from starlette import status

from src.config import get_settings
from src.models import UserSecret as ModelUserSecret
from src.repository import UserSecret as RepositoryUserSecret
from src.schemas import (
    CreateSecretRequestSchema,
    CreateSecretResponseSchema,
    GetSecretResponseSchema,
)
from src.utils import crypto


class UserSecret:
    @classmethod
    async def create_item(
        cls,
        data: CreateSecretRequestSchema,
    ) -> CreateSecretResponseSchema:
        conf = get_settings()
        secret_key = (
            data.secret_key
            if data.secret_key
            else token_urlsafe(conf.application.password_gen_len)
        )

        user_secret = ModelUserSecret(
            data=crypto.encrypt(data.message, secret_key),
            expireAt=(
                datetime.utcnow() + timedelta(seconds=data.ttl) if data.ttl else None
            ),
        )

        async with RepositoryUserSecret() as repo:
            user_secret = await repo.write_item(user_secret)

        return CreateSecretResponseSchema(
            secret_id=user_secret.id,
            secret_key=secret_key,
        )

    @classmethod
    async def get_item_by_id(
        cls,
        object_id: str,
        secret_key: str,
    ) -> GetSecretResponseSchema:
        async with RepositoryUserSecret() as repo:

            user_secret = await repo.get_item_by_id(object_id)

            if user_secret:
                try:
                    decrypt_data = crypto.decrypt(user_secret.data, secret_key)
                except ValueError:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

                await repo.delete_item(user_secret)
                return GetSecretResponseSchema(
                    data=decrypt_data,
                )
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
