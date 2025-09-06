# TOC Navigator AI

Простой прототип серверной части на FastAPI.

## Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Откройте [http://localhost:8000/docs](http://localhost:8000/docs) для просмотра API.

## Запуск в Docker

Сборка и запуск всех контейнеров:

```bash
docker-compose up --build
```

Будут подняты сервисы `api`, `postgres`, `qdrant` и опционально `redis`. API будет доступен по адресу [http://localhost:8000/docs](http://localhost:8000/docs).

Старый прототип на Flask сохранён в `legacy/legacy_app.py`.
