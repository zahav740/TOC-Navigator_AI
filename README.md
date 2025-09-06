# TOC Navigator AI

Простой прототип серверной части на FastAPI.

## Требования

- Python 3.11+
- Запущенный PostgreSQL

## Конфигурация

Скопируйте `.env.example` в `.env` и при необходимости измените значения:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
SECRET_KEY=changeme
GEMINI_API_KEY=changeme
```

Для единичного запуска без `.env` установите переменную окружения `DATABASE_URL`.

- **Unix**:
  ```bash
  export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
  ```
- **PowerShell**:
  ```powershell
  $env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"
  ```

## Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Откройте [http://localhost:8000/docs](http://localhost:8000/docs) для просмотра API.

Старый прототип на Flask сохранён в `app/legacy_app.py`.
