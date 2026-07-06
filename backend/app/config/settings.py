from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "VitalSync"
    environment: str = "development"
    secret_key: str = Field(default="change-this-secret-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./vitalsync.db"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    openweather_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return list(value)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
