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

    # Anti-spam — Cloudflare Turnstile
    TURNSTILE_SECRET_KEY: str = "1x0000000000000000000000000000000AA"  # test key always passes in dev
    TURNSTILE_SITE_KEY: str = "1x0000000000000000000000000000000AA"

    # Anti-spam — behavioral scoring
    SPAM_SCORING_ENABLED: bool = True
    SPAM_SCORE_THRESHOLD: int = 5  # max score before rejection
    SPAM_RATE_LIMIT_WINDOW: int = 60  # seconds
    SPAM_RATE_LIMIT_MAX: int = 10  # max submissions per window per fingerprint
    SPAM_IP_RATE_LIMIT: str = "20/minute"  # per-IP limit on public endpoint
    SPAM_FINGERPRINT_RATE_LIMIT: str = "10/minute"  # per (IP+UA) fingerprint

    # Analytics
    GOACCESS_ENABLED: bool = True

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


settings = Settings()
