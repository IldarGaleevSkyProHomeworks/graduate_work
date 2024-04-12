from abc import abstractmethod

from motor.motor_asyncio import AsyncIOMotorCollection

from src.config import Settings, get_settings
from src.database.mongodb import get_db_context


class RepositoryItem:
    COLLECTION_NAME = None

    def __init__(self, prop: Settings = None):  # pragma: no cover

        if self.COLLECTION_NAME is None:
            raise Exception("Collection is not set")

        if prop is None:
            prop = get_settings()

        self._db_session = get_db_context(prop)

    async def __aenter__(self):
        db_ctx = await self._db_session.__aenter__()

        self._collection: AsyncIOMotorCollection = db_ctx.get_collection(
            self.COLLECTION_NAME
        )

        return self

    async def __aexit__(self, *args):
        await self._db_session.__aexit__(*args)

    @abstractmethod
    async def write_item(
        self,
        item,
    ):
        pass  # pragma: no cover

    @abstractmethod
    async def get_item_by_id(
        self,
        user_secret_id: str,
    ):
        pass  # pragma: no cover

    @abstractmethod
    async def delete_item(
        self,
        item,
    ):
        pass  # pragma: no cover
