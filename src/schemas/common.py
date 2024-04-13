from pydantic import BaseModel

from src.enums import ResponseStatusEnum


class CommonResponseSchema(BaseModel):
    status: ResponseStatusEnum = ResponseStatusEnum.OK
