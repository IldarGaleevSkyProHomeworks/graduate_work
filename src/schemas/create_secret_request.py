from pydantic import BaseModel, Field


class CreateSecretRequestSchema(BaseModel):
    """
    Data for creating new secret
    """

    message: str = Field(
        max_length=1024,
        description="Message for encrypt",
    )

    secret_key: str | None = Field(
        max_length=100,
        default=None,
        description="Key for decrypt secret. Leave the field blank for generate secret.",
    )

    ttl: int | None = Field(
        default=None,
        le=24 * 365,
        description="Time to live (Minutes)",
    )
