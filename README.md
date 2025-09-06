# TOC Navigator AI

Простой прототип серверной части на FastAPI.

## Требования

- Python 3.11+
- Запущенный PostgreSQL (по умолчанию используется `postgres:magarel1@localhost:5432/ai_base`)

## Запуск

```bash
pip install -r requirements.txt
# при необходимости поменяйте строку подключения к БД
export DATABASE_URL=postgresql://postgres:magarel1@localhost:5432/ai_base
uvicorn app.main:app --reload
```

Откройте [http://localhost:8000/docs](http://localhost:8000/docs) для просмотра API.

Старый прототип на Flask сохранён в `app/legacy_app.py`.
