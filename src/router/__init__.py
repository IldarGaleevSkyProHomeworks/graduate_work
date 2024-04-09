__all__ = ["root_router"]
from fastapi import APIRouter
from .common import router as common_router


class RootRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.include_router(common_router)


root_router = RootRouter()
