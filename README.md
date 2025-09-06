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

| Variable             | Description                     | Default                                    |
|----------------------|---------------------------------|--------------------------------------------|
| NODE_ENV             | Runtime environment             | development                                |
| VITE_BACKEND_URL     | Frontend URL for backend API    | http://localhost:3001                      |
| DATABASE_URL         | SQLAlchemy connection string    | postgresql://postgres:magarel@localhost:5432/toc_ai |
| DB_HOST              | Database host                   | localhost                                  |
| DB_PORT              | Database port                   | 5432                                       |
| DB_NAME              | Database name                   | toc_ai                                     |
| DB_USER              | Database user                   | postgres                                   |
| DB_PASSWORD          | Database password               | magarel                                    |
| POSTGRES_USER        | Postgres container user         | postgres                                   |
| POSTGRES_PASSWORD    | Postgres container password     | magarel                                    |
| POSTGRES_DB          | Postgres container database     | toc_ai                                     |
| VITE_AI_ENDPOINT     | AI service endpoint             | /api/gemini/chat                           |
| VITE_GOOGLE_API_KEY  | Google API key (frontend)       | your-google-api-key                        |
| VITE_GEMINI_API_KEY  | Gemini API key (frontend)       | your-gemini-api-key                        |
| GOOGLE_API_KEY       | Google API key (backend)        | your-google-api-key                        |
| QDRANT_URL           | Qdrant vector DB URL            | http://localhost:6333                      |
| VITE_QDRANT_URL      | Qdrant URL for frontend         | http://localhost:6333                      |
| REDIS_URL            | Redis connection URL            | redis://localhost:6379/0                   |

Старый прототип на Flask сохранён в `app/legacy_app.py`.
