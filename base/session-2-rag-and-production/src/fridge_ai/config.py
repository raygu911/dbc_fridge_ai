from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FridgeAI"
    app_env: str = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str = (
        "postgresql+psycopg://fridge_ai:change-me@localhost:5432/fridge_ai"
    )
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "recipes"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3:4b"
    rag_result_limit: int = 3
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
