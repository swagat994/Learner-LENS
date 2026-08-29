from pydantic import BaseModel

from .sections.app import AppSettings
from .sections.database import DatabaseSettings
from .sections.jwt import JWTSettings
from .sections.llm import LLMSettings
from .sections.cors import CORSSettings


class Settings(BaseModel):
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    llm: LLMSettings = LLMSettings()
    cors: CORSSettings = CORSSettings()


settings = Settings()