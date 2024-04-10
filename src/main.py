from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.database.mongodb import get_db_context
from src.repository import UserSecret
from src.router import root_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_db_context(get_settings()) as db:
        await db.get_collection(UserSecret.COLLECTION_NAME).create_index(
            {"expireAt": 1},
            expireAfterSeconds=0,
        )

    yield


app = FastAPI(
    title="Fading Letter",
    version="1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().application.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
