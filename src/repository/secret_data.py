from bson import ObjectId

from src.models import UserSecret as ModelUserSecret
from .repository_item import RepositoryItem


class UserSecret(RepositoryItem):
    COLLECTION_NAME = "secrets"

    async def write_item(
        self,
        user_secret: ModelUserSecret,
    ) -> ModelUserSecret:
        data = user_secret.model_dump(exclude_none=True)

        index = await self._collection.insert_one(data)

        user_secret.id = str(index.inserted_id)
        return user_secret

    async def get_item_by_id(
        self,
        user_secret_id: str,
    ) -> ModelUserSecret | None:
        obj_id = ObjectId(user_secret_id)

        item = await self._collection.find_one({"_id": obj_id})

        if item:
            found = ModelUserSecret(**item)
            found.id = obj_id
            return found

        return None

    async def delete_item(
        self,
        user_secret: ModelUserSecret,
    ) -> ModelUserSecret:
        await self._collection.delete_one({"_id": user_secret.id})
        return user_secret
