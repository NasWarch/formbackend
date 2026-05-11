"""Pydantic Settings — toute la config via variables d'environnement."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    APP_NAME: str = "Monito"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "postgresql://monetization:***@localhost:5432/monetization"

    # Redis
    REDIS_URL: str = "redis://localhost:***@formapi.app"

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    # Rate limiting
    RATE_LIMIT: str = "60/minute"

    # CORS
    CORS_ORIGINS: str = "http://localhost:8000"

    # Analytics
    GOACCESS_ENABLED: bool = True

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


settings = Settings()
