from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import Settings


@asynccontextmanager
async def get_db_context(
    prop: Settings,
) -> AsyncIOMotorDatabase:
    conn = AsyncIOMotorClient(prop.database.mongo_dsn)
    try:
        yield conn.get_database(prop.database.mongo_db_name)
    finally:
        conn.close()
