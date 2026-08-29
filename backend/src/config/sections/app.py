from .base import BaseConfig


class AppSettings(BaseConfig):
    app_name: str
    api_version: str
    environment: str
    debug: bool
    host: str
    port: int