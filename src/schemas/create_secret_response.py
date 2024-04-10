from pydantic import Field

from .common import CommonResponseSchema


class CreateSecretResponseSchema(CommonResponseSchema):
    """
    Information about new secret.
    """

    secret_id: str = Field(
        max_length=24,
        description="Index for secret.",
    )

    secret_key: str | None = Field(
        default=None,
        description="Key for decrypt secret.",
    )
