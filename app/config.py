from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@db:5432/postgres"
    redis_url: str = "redis://redis:6379/0"
    qdrant_url: str = "http://qdrant:6333"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
