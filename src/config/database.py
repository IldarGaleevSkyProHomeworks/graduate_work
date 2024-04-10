from pydantic import (
    Field,
    BaseModel,
    MongoDsn,
)


class DatabaseSettings(BaseModel):
    mongo_dsn: MongoDsn = Field(default="mongodb://localhost:27017/")
    mongo_db_name: str = Field(default="fading_later")
