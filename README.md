# FastAPI Notes App — Skeleton

Мини-каркас backend-приложения на **FastAPI** с **PostgreSQL** и **Alembic**.
Цель — показать архитектуру проекта, модели и миграции, Pydantic-схемы, CRUD-заглушки и **моковые** REST-эндпоинты. Бизнес-логика хранения/чтения из БД **пока не реализуется**.

## ✨ Возможности

* Структурированное приложение: `app/api`, `app/core`, `app/db`
* Pydantic-схемы: `UserCreate`, `UserRead`, `NoteCreate`, `NoteRead`, `NoteUpdate`
* SQLAlchemy-модель: `Note`
* Alembic-миграции (таблица `notes`)
* Моковые эндпоинты `/api/notes` (POST, GET, GET/{id}, PATCH/{id}, DELETE/{id})

---

## 📂 Структура проекта

```
app/
├─ api/
│  ├─ endpoints/
│  │  ├─ __init__.py
│  │  └─ notes.py
│  ├─ schemas/
│  │  ├─ __init__.py
│  │  ├─ note.py
│  │  └─ user.py
│  ├─ __init__.py
│  └─ routers.py
│
├─ core/
│  ├─ __init__.py
│  ├─ base.py
│  ├─ config.py
│  ├─ constants.py
│  └─ db.py
│
├─ db/
│  ├─ __init__.py
│  ├─ crud/
│  │  ├─ __init__.py
│  │  └─ note.py
│  └─ models/
│     ├─ __init__.py
│     └─ note.py
│
├─ main.py
│
alembic/
├─ env.py
├─ script.py.mako
└─ versions/
   └─ 0001_create_notes_table.py

alembic.ini
.env.example
requirements.txt
```

---

## 🧰 Требования

* Python **3.10+**
* PostgreSQL **15+** (локально или в Docker)
* Установленные зависимости из `requirements.txt`

`requirements.txt` (минимум):

```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
SQLAlchemy>=2.0.32
psycopg2-binary>=2.9.9
alembic>=1.13.2
pydantic>=2.9.2
pydantic-settings>=2.4.0
python-dotenv>=1.0.1
email-validator>=2.2.0
```

---

## 🚀 Быстрый старт

### 1) Клонирование и окружение

```bash
git clone <your-repo-url> fastapi-notes-app
cd fastapi-notes-app

python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .\.venv\Scripts\activate

pip install -U pip
pip install -r requirements.txt
```

### 2) Настрой `.env`

Скопируй пример и поправь строку подключения:

```bash
cp .env.example .env
```

`.env`:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/notes_db
APP_ENV=local
DEBUG=true
```

> На macOS надёжнее использовать `127.0.0.1`, а не `localhost`.

### 3A) Поднять PostgreSQL (локально через Homebrew)

```bash
brew install postgresql@15
echo 'export PATH="$(brew --prefix postgresql@15)/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
brew services start postgresql@15

# создать пользователя/пароль и БД
psql -h 127.0.0.1 -U "$(whoami)" -d postgres -c \
"DO \$\$ BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='postgres') THEN
     CREATE ROLE postgres WITH LOGIN SUPERUSER PASSWORD 'postgres';
   ELSE
     ALTER ROLE postgres WITH LOGIN SUPERUSER PASSWORD 'postgres';
   END IF;
 END \$\$;"

createdb -h 127.0.0.1 -U postgres notes_db
psql "postgresql://postgres:postgres@127.0.0.1:5432/notes_db" -c "SELECT 1;"
```

### 3B) (Альтернатива) Поднять PostgreSQL в Docker

```bash
docker run -d --name notes-pg \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=notes_db \
  -p 5432:5432 \
  -v notes_pgdata:/var/lib/postgresql/data \
  postgres:15

psql "postgresql://postgres:postgres@127.0.0.1:5432/notes_db" -c "SELECT 1;"
```

### 4) Миграции Alembic

```bash
alembic upgrade head
```

Если всё ок — таблица `notes` появится в БД.

### 5) Запуск приложения

```bash
uvicorn app.main:create_app --reload
```

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 🔌 API (моки)

Базовый префикс: `/api`

### POST `/api/notes/` — создать заметку (мок)

```bash
curl -X POST http://127.0.0.1:8000/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test",
    "content": "Hello",
    "is_public": false,
    "is_completed": false
  }'
```

### GET `/api/notes/` — список заметок (мок)

```bash
curl http://127.0.0.1:8000/api/notes
```

### GET `/api/notes/{note_id}` — получить заметку (мок)

```bash
curl http://127.0.0.1:8000/api/notes/1
```

### PATCH `/api/notes/{note_id}` — обновить заметку (мок)

```bash
curl -X PATCH http://127.0.0.1:8000/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated title"
  }'
```

### DELETE `/api/notes/{note_id}` — удалить заметку (мок)

```bash
curl -X DELETE http://127.0.0.1:8000/api/notes/1 -i
```

Коды ответов: `201` (создание), `200` (получение/обновление), `204` (удаление), `404` (не найдено), `422` (невалидные данные — отдаёт FastAPI).

---

## 🧱 Модели и схемы

### SQLAlchemy модель

`app/db/models/note.py`:

* `id: int` (PK)
* `title: str`
* `content: str`
* `is_public: bool` (default: `False`)
* `is_completed: bool` (default: `False`)
* `created_at: datetime` (default: UTC now / CURRENT_TIMESTAMP)

### Pydantic схемы

`app/api/schemas/note.py`:

* `NoteCreate` — вход для создания
* `NoteUpdate` — частичное обновление (все поля опциональны)
* `NoteRead` — выходные данные (`from_attributes=True`)

`app/api/schemas/user.py`:

* `UserCreate(email, password)`
* `UserRead(id, email)`

> Для `EmailStr` нужна зависимость `email-validator`.

---

## 🔄 Миграции: полезные команды

Сгенерировать новую пустую ревизию:

```bash
alembic revision -m "message"
```

Сгенерировать ревизию по diff (если использовать автогенерацию):

```bash
alembic revision --autogenerate -m "auto"
```

Применить/откатить:

```bash
alembic upgrade head
alembic downgrade -1
```

> **Важно:** чтобы Alembic видел модели, в `alembic/env.py` импортируются файлы с моделями, например:
>
> ```python
> import app.db.models.note  # noqa: F401
> ```

---

## 🧪 Быстрая самопроверка

```bash
# .env подхватывается?
python -c "from app.core.config import get_settings; print(get_settings().DATABASE_URL)"

# БД отвечает?
psql 'postgresql://postgres:postgres@127.0.0.1:5432/notes_db' -c 'SELECT 1;'

# Миграции проходят?
alembic upgrade head

# Сервер поднимается?
uvicorn app.main:create_app --reload
```

---

## 🧯 Тротблшутинг

* **`ImportError: cannot import name 'Base' from partially initialized module ...`**
  Удали импорты моделей из `app/core/base.py`. Импортируй модели **в `alembic/env.py`**, а не в `base.py`.

* **`pydantic ValidationError: DATABASE_URL Field required`**
  `.env` не найден/не в корне. Проверь путь и содержимое. На крайний случай экспортни переменную окружения:

  ```bash
  export DATABASE_URL="postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/notes_db"
  ```

* **`ModuleNotFoundError: No module named 'email_validator'`**

  ```
  pip install email-validator
  ```

* **`psycopg2` не ставится на Linux**

  ```
  sudo apt-get install -y libpq-dev python3-dev build-essential
  ```

* **`connection refused` / порт 5432**
  Подними Postgres (Homebrew/Docker) и проверь:

  ```
  lsof -i :5432
  ```

* **`password authentication failed`**
  Проверь пароль пользователя `postgres`:

  ```bash
  psql -h 127.0.0.1 -U postgres -d postgres -c "ALTER USER postgres WITH PASSWORD 'postgres';"
  ```

---

## 🧱 (Опционально) Docker-Compose

`docker-compose.db.yml`:

```yaml
version: "3.9"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: notes_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata_notes:/var/lib/postgresql/data
volumes:
  pgdata_notes:
```

Запуск БД:

```bash
docker compose -f docker-compose.db.yml up -d
```

---

## 🔧 (Опционально) Makefile

```make
.PHONY: dev migrate down

dev:
\tuvicorn app.main:create_app --reload

migrate:
\talembic upgrade head

down:
\talembic downgrade -1
```

Использование:

```bash
make migrate
make dev
```

---

## 📜 Лицензия

MIT.

