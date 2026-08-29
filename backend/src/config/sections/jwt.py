from pydantic import Field

from .base import BaseConfig


class JWTSettings(BaseConfig):
    secret_key: str = Field(alias="JWT_SECRET_KEY")
    algorithm: str = Field(alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )