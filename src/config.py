from collections import namedtuple
from functools import lru_cache
from urllib.parse import urljoin

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False
    api_str: str = "/api"
    access_token_expire_minutes: int = 60 * 24 * 14
    auth_secret_key: str
    jwt_algorithm: str
    database_url: str
    rds_hostname: str | None = None
    rds_user: str | None = None
    rds_port: int | None = None
    rds_db: str | None = None
    rds_password: str | None = None

    model_config = SettingsConfigDict(env_file='.env')


@lru_cache()
def get_settings() -> Settings:
    return Settings()
