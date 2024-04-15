from typing import List

from pydantic import BaseModel, Field


class ApplicationSettings(BaseModel):
    url_scheme: str = Field(default="https", max_length=5)
    hostname: str = Field(default="localhost")
    password_gen_len: int = Field(default=10)
    cors_origins: List[str] = Field(default_factory=lambda: [])
    cors_headers: List[str] = Field(default_factory=lambda: ["*"])
    cors_methods: List[str] = Field(default_factory=lambda: ["*"])
