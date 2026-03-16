from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Inventory API"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api"
    cors_origins: list[str] = ["*"]
    log_level: str = "INFO"
    database_url: str = "postgresql+psycopg://inventory:inventory@postgres:5432/inventory"
    celery_broker_url: str = "amqp://guest:guest@rabbitmq:5672//"
    celery_result_backend: str = "rpc://"
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
