from datetime import datetime

from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField


class UserSecret(BaseModel):
    id: ObjectIdField = None

    data: bytes = Field()

    expireAt: datetime | None = Field(
        default=None,
    )
