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
| POSTGRES_USER    | PostgreSQL user                        | toc_ai                                    |
| POSTGRES_PASSWORD| PostgreSQL password                    | magarel                                   |
| POSTGRES_DB      | PostgreSQL database name               | toc_ai                                    |
| DATABASE_URL     | SQLAlchemy connection string           | postgresql://toc_ai:magarel@db:5432/toc_ai |
| REDIS_URL        | Redis connection URL                   | redis://redis:6379/0                      |
| QDRANT_URL       | Qdrant vector DB URL                   | http://qdrant:6333                        |

Старый прототип на Flask сохранён в `app/legacy_app.py`.
