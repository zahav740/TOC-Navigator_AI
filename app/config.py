from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://toc_ai:magarel@localhost:5432/toc_ai"
    redis_url: str = "redis://redis:6379/0"
    qdrant_url: str = "http://qdrant:6333"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
