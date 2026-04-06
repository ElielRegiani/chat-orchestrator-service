from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "chat-service"
    log_level: str = "INFO"

    insight_service_url: str = "http://localhost:8001"
    insight_timeout_seconds: float = 30.0
    insight_max_retries: int = 3

    whatsapp_api_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_api_version: str = "v21.0"
    whatsapp_graph_base: str = "https://graph.facebook.com"

    http_timeout_seconds: float = 30.0

    # observability
    metrics_enabled: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
