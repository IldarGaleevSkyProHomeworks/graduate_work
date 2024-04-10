from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import Settings, get_settings


def get_db(prop: Settings = Depends(get_settings)) -> AsyncIOMotorDatabase:
    conn = AsyncIOMotorClient(prop.database.mongo_dsn)
    try:
        yield conn.get_database(prop.database.mongo_db_name)
    finally:
        conn.close()
