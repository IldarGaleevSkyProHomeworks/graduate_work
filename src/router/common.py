from fastapi import APIRouter

from src.schemas import CommonResponseSchema

router = APIRouter(
    tags=["common"],
)


@router.get("/")
async def common_home_handler() -> CommonResponseSchema:
    return CommonResponseSchema()
