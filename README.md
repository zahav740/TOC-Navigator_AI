# TOC Navigator AI

Простой прототип серверной части на FastAPI.

## Запуск

Скопируйте `.env.example` в `.env` и при необходимости измените значения.

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Откройте [http://localhost:8000/docs](http://localhost:8000/docs) для просмотра API.

### Docker

Альтернативно можно использовать Docker Compose:

```bash
docker-compose up --build
```

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `DATABASE_URL` | URL базы данных PostgreSQL | `postgresql://postgres:postgres@db:5432/postgres` |
| `REDIS_URL` | URL сервера Redis | `redis://redis:6379/0` |
| `QDRANT_URL` | URL Qdrant | `http://qdrant:6333` |

## Development

Перед коммитом запустите проверки:

```bash
pre-commit run --files <file1> <file2>
pytest -q
```

Старый прототип на Flask сохранён в `app/legacy_app.py`.
