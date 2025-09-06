# TOC Navigator AI

Простой прототип серверной части на FastAPI.

## Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Либо через Docker:

```bash
cp .env.example .env
docker compose up --build
```

Откройте [http://localhost:8000/docs](http://localhost:8000/docs) для просмотра API.

## Environment Variables

Файл `.env` содержит настройки окружения.

| Variable         | Description                            | Default                                   |
|------------------|----------------------------------------|-------------------------------------------|
| POSTGRES_USER    | PostgreSQL user                        | postgres                                  |
| POSTGRES_PASSWORD| PostgreSQL password                    | postgres                                  |
| POSTGRES_DB      | PostgreSQL database name               | postgres                                  |
| DATABASE_URL     | SQLAlchemy connection string           | postgresql://postgres:postgres@db:5432/postgres |
| REDIS_URL        | Redis connection URL                   | redis://redis:6379/0                      |
| QDRANT_URL       | Qdrant vector DB URL                   | http://qdrant:6333                        |

Старый прототип на Flask сохранён в `app/legacy_app.py`.
