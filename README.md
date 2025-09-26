# FastAPI Notes App (skeleton)

## Быстрый старт
```bash
cp .env.example .env
# создайте БД вручную (например, notes_db), либо измените DATABASE_URL

# миграции
alembic upgrade head

# запуск
uvicorn app.main:create_app --reload
