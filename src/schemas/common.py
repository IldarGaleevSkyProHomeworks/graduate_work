from pydantic import BaseModel, Field

from src.enums import ResponseStatusEnum


class CommonSchema(BaseModel):
    status: ResponseStatusEnum = ResponseStatusEnum.OK
