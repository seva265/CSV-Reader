# Система управления оценками студентов

## 🚀 Быстрый запуск (Docker)

### 1. Подготовка окружения

```bash
# Копируем .env файл
cp .env.example .env
```

### 2. Сборка и запуск

```bash
# Собираем и запускаем сервисы в фоне
docker-compose up --build -d
```

### 3. Применение миграций

```bash
# Внутри контейнера
docker-compose exec app python3 scripts/migrate.py
```

### 4. Загрузка тестовых данных (опционально)

```bash
docker-compose exec app python3 scripts/seed_db.py
```

### 5. Доступ к API

```
http://localhost:8000/docs
```

### 6. Остановка

```bash
docker-compose down
```

---

## 📋 Описание проекта

API для управления оценками студентов. Позволяет загружать данные из CSV, анализировать успеваемость и получать статистику по двойкам.

### Возможности

- **Загрузка данных** — импорт оценок из CSV-файлов
- **Аналитика** — получение списков студентов с количеством двоек
- **Нормализованная БД** — данные разбиты на таблицы `students`, `groups`, `marks`
- **Миграции** — версионирование схемы БД через SQL-файлы
- **Сиды** — тестовые данные для быстрой проверки

### Технологии

- **FastAPI** — асинхронный веб-фреймворк
- **asyncpg** — асинхронный драйвер PostgreSQL
- **Poetry** — управление зависимостями
- **yoyo-migrations** — применение миграций
- **pytest** — тестирование

---

## 📁 Структура проекта

```
ecom_test/
├── app/                      # Исходный код приложения
│   ├── main.py              # Точка входа
│   ├── database.py          # Подключение к БД
│   ├── services.py          # Бизнес-логика
│   ├── schemas.py           # Pydantic-схемы
│   ├── config.py            # Конфигурация
│   └── routers/             # API-роуты
│       ├── grades.py
│       └── analysis.py
├── migrations/              # SQL-миграции
│   ├── 0001_initial.sql
│   └── 0002_normalize.sql
├── seeds/                   # Тестовые данные
│   └── seeds.sql
├── scripts/                 # Утилиты
│   ├── migrate.py          # Раннер миграций
│   ├── seed_db.py          # Загрузка сидов
│   ├── init_db.py          # Инициализация
│   └── run_tests.py        # Запуск тестов
├── tests/                   # Тесты
│   ├── conftest.py
│   ├── fixtures.py
│   ├── test_upload_errors.py
│   ├── test_database_errors.py
│   └── test_analysis_endpoints.py
├── docker-compose.yml       # Docker-оркестрация
├── Dockerfile               # Сборка образа
├── pyproject.toml           # Зависимости Poetry
└── .env.example             # Пример переменных окружения
```

---

## 🔧 Локальная разработка (без Docker)

### Установка Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Запуск

```bash
# Установка зависимостей
poetry install

# Применение миграций
poetry run python scripts/migrate.py

# Загрузка сидов
poetry run python scripts/seed_db.py

# Запуск сервера
poetry run uvicorn app.main:app --reload
```

---

## 🧪 Тестирование

```bash
# Через скрипт (рекомендуется)
python scripts/run_tests.py

# Или напрямую
poetry run pytest tests/ -v

# В контейнере
docker-compose exec app pytest tests/ -v
```

---

## 📊 Эндпоинты API

### Загрузка данных

```
POST /upload-grades
Content-Type: multipart/form-data
file: <csv-файл>
```

### Аналитика

```
GET /students/more-than-3-twos    # Студенты с >3 двойками
GET /students/less-than-5-twos   # Студенты с <5 двойками
```

---

## 📝 Примечания

- Миграции применяются через `scripts/migrate.py` и записываются в таблицу `schema_migrations`
- `migrations/` — единственный источник правды для схемы БД
- Проект использует `asyncpg` без ORM
- Для экспорта `requirements.txt`: `poetry export -f requirements.txt --without-hashes`