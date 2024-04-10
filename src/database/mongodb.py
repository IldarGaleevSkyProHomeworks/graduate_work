from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import Settings, get_settings


@asynccontextmanager
async def get_db_context(
    prop: Settings = get_settings(),
) -> AsyncIOMotorDatabase:
    conn = AsyncIOMotorClient(prop.database.mongo_dsn)
    try:
        yield conn.get_database(prop.database.mongo_db_name)
    finally:
        conn.close()
