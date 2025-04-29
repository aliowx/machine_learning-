from typing import Any
from pydantic import (
    AnyHttpUrl,
    EmailStr,
    PostgresDsn,
    RedisDsn,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

REFRESH_TOKEN_BLOCKLIST_KEY = "refresh_token_blocklist:{token}"
ACCESS_TOKEN_BLOCKLIST_KEY = "access_token_blocklist:{token}"

class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {"postgres+asyncpg", "postgresql+asyncpg"}

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    SECRET_KEY: str
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | str = []
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str = "HS256"
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    POSTGRES_ASYNC_URI: AsyncPostgresDsn | None = None
    REDIS_URI: RedisDsn | None = None
    SUB_PATH: str = ""
    HEALTH_USERNAME: str
    HEALTH_PASSWORD: str
    COMMIT_ID: str | None = None
    APP_VERSION: str | None = None

    @classmethod
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.strip("[]").split(",")]
        return v

    @property
    def allow_origins(self) -> list[str]:
        return [str(origin).strip("/") for origin in self.BACKEND_CORS_ORIGINS]

    @field_validator("POSTGRES_ASYNC_URI", mode="before")
    @classmethod
    def assemble_async_db_connection(cls, v: str | None) -> Any:
        if isinstance(v, str):
            return AsyncPostgresDsn(v)

    @field_validator("REDIS_URI", mode="before")
    @classmethod
    def assemble_redis_URI_connection(cls, v: str | None) -> Any:
        if isinstance(v, str):
            return RedisDsn(v)

    model_config = SettingsConfigDict(env_file=".env", extra="allow")  # Allow extra inputs

settings = Settings()
