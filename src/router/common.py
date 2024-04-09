from fastapi import APIRouter

from src.schemas import CommonSchema

router = APIRouter(
    tags=["common"],
)


@router.get("/")
async def common_home_handler() -> CommonSchema:
    return CommonSchema()
