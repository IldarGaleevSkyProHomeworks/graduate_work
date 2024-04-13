from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import Settings


@asynccontextmanager
async def get_db_connection(
    prop: Settings,
) -> AsyncIOMotorClient:
    conn = AsyncIOMotorClient(str(prop.database.mongo_dsn))
    try:
        yield conn
    finally:
        conn.close()


@asynccontextmanager
async def get_db_context(
    prop: Settings,
) -> AsyncIOMotorDatabase:
    async with get_db_connection(prop) as conn:
        yield conn.get_database(str(prop.database.mongo_db_name))
