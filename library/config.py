import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AccessToken(BaseModel):
    lifetime_seconds = 3600


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )
    access_token: AccessToken = AccessToken()


settings = Settings()


def get_db_url():
    return f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"