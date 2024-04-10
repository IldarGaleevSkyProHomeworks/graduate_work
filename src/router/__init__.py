__all__ = ["root_router"]
from fastapi import APIRouter
from .common import router as common_router
from .secret_data import router as secret_data_router


class RootRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.include_router(common_router)
        self.include_router(secret_data_router)


root_router = RootRouter()
