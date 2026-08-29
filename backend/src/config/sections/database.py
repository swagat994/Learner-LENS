from pydantic import Field

from .base import BaseConfig


class DatabaseSettings(BaseConfig):
    mongodb_uri: str = Field(alias="MONGODB_URI")
    database_name: str = Field(alias="DATABASE_NAME")