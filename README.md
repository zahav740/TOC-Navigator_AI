# TOC Navigator AI

Простой прототип серверной части на FastAPI.

## Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Откройте [http://localhost:8000/docs](http://localhost:8000/docs) для просмотра API.

## Запуск в Docker

Для локального запуска доступны контейнеры приложения и баз данных.

```bash
docker compose up --build
```

Эта команда использует `docker-compose.yml` и поднимает сервисы `api`, `postgres` и `qdrant`.
При необходимости Redis можно включить с помощью профиля:

```bash
docker compose --profile redis up --build
```

После старта API будет доступен по адресу [http://localhost:8000/docs](http://localhost:8000/docs).

Старый прототип на Flask сохранён в `legacy/legacy_app.py`.
