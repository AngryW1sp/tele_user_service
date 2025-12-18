"""Конфигурация приложения через pydantic-settings.

Параметры читаются из `.env` (при наличии) и доступны через `settings`.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Набор конфигурационных параметров приложения."""

    app_env: str = "local"
    app_port: int = 8001
    database_url: str = ""
    database_url_sync: str = ""
    internal_api_token: str = "super-long-random-string"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
