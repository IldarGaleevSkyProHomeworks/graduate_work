from datetime import datetime, timedelta
from secrets import token_urlsafe

from bson import ObjectId
from fastapi import HTTPException
from starlette import status

from src.config import get_settings
from src.database.mongodb import get_db_context
from src.schemas import (
    CreateSecretRequestSchema,
    CreateSecretResponseSchema,
    GetSecretResponseSchema,
)
from src.utils import crypto


class UserSecret:
    COLLECTION_NAME = "secrets"

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

        mongo_data = {
            "data": crypto.encrypt(data.message, secret_key),
        }
        if data.ttl:
            mongo_data["expireAt"] = datetime.utcnow() + timedelta(seconds=data.ttl)

        async with get_db_context() as db:
            result = await db.get_collection(cls.COLLECTION_NAME).insert_one(mongo_data)

        secret_id = str(result.inserted_id)

        return CreateSecretResponseSchema(
            secret_id=secret_id,
            secret_key=secret_key,
        )

    @classmethod
    async def get_item_by_id(
        cls,
        object_id: str,
        secret_key: str,
    ) -> GetSecretResponseSchema:
        async with get_db_context() as db:

            query = {
                "_id": ObjectId(object_id),
            }

            collection = db.get_collection(cls.COLLECTION_NAME)

            user_secret = await collection.find_one(query)

            if user_secret:
                try:
                    decrypt_data = crypto.decrypt(user_secret["data"], secret_key)
                except ValueError:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

                await collection.find_one_and_delete(query)
                return GetSecretResponseSchema(
                    data=decrypt_data,
                )
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
