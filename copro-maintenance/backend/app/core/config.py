from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./copro_maintenance.db"
    SECRET_KEY: str = "copro-maintenance-secret-key-change-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    APP_NAME: str = "CoproMaintenance"

    model_config = {"env_prefix": "COPRO_"}


settings = Settings()
