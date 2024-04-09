from fastapi import FastAPI
from src.router import root_router

app = FastAPI(
    title="Fading Letter",
    version="1.0",
)

app.include_router(root_router)
