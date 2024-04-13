from typing import List

from pydantic import BaseModel, Field
from pydantic_core import Url


class ApplicationSettings(BaseModel):
    url_scheme: str = Field(default="https", max_length=5)
    hostname: str = Field(default="localhost")
    password_gen_len: int = Field(default=10)
    origins: List[str] = Field(default_factory=lambda: [])
