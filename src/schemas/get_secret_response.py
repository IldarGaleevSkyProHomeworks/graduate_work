from pydantic import Field

from .common import CommonResponseSchema


class GetSecretResponseSchema(CommonResponseSchema):
    data: str | None = Field(default=None)
