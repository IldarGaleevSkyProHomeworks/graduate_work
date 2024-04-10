from pydantic import BaseModel, Field


class ApplicationSettings(BaseModel):
    url_scheme: str = Field(default="https", max_length=5)
    hostname: str = Field(default="localhost")
    password_gen_len: int = Field(default=10)
