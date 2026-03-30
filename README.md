# Система управления оценками студентов

## Быстрый старт

1. скопируйте и заполните `.env` из `.env.example`.
2. примените миграции:

```bash
# локально (с poetry)
poetry run python scripts/migrate.py

# или внутри контейнера
docker-compose exec app python3 -c "import scripts.migrate as m; m.main()"
```

3. (опционально) загрузите сиды:

```bash
poetry run python scripts/seed_db.py
```

4. запустите сервис:

```bash
## Быстрый старт (Docker)

1. Установите Docker и docker-compose.
2. Скопируйте `.env.example` в `.env` и при необходимости измените значения.
3. Постройте и запустите сервисы:

```bash
docker-compose up --build -d
```

4. Примените миграции (если они не применяются автоматически):

```bash
# внутри контейнера
docker-compose exec app python3 scripts/migrate.py

# или локально (через poetry)
poetry run python scripts/migrate.py
```

5. По желанию загрузите сиды (тестовые данные):

```bash
docker-compose exec app python3 scripts/seed_db.py
```

6. Документация API доступна по адресу:

```
http://localhost:8000/docs
```

7. Остановить сервисы:

```bash
docker-compose down
```

## Структура проекта

- `app/` — источник приложения FastAPI:
	- `app/main.py` — точка входа и регистрация роутеров;
	- `app/database.py` — инициализация пула, помощники доступа к БД;
	- `app/services.py` — бизнес-логика и SQL-запросы;
	- `app/routers/` — маршруты API (grades, analysis);
	- `app/schemas.py` — Pydantic-схемы для ответов/запросов;
	- `app/config.py` — конфигурация окружения.
- `migrations/` — SQL-файлы миграций; являются источником правды для схемы БД.
- `seeds/` — сиды (тестовые данные), применяются явно через `scripts/seed_db.py`.
- `scripts/` — вспомогательные утилиты:
	- `migrate.py` — раннер миграций (помечает применённые в таблице `schema_migrations`);
	- `seed_db.py` — применяет `seeds/seeds.sql`;
	- `init_db.py` — обёртка/инициализатор (вызывает мигратор при необходимости).
- `tests/` — набор pytest тестов и фикстур для проверки логики и ошибок.
- `Dockerfile`, `docker-compose.yml` — образ и оркестрация контейнеров.
- `pyproject.toml` — конфигурация Poetry и зависимости проекта.
- `.env.example` — пример переменных окружения (скопируйте в `.env`).

## Миграции

- Все изменения схемы должны попадать в `migrations/` как отдельные `.sql` файлы, пронумерованные по порядку.
- `scripts/migrate.py` применяет все новые файлы и записывает их в таблицу `schema_migrations`, чтобы не дублировать применение.
- Не храните противоположные/дублирующие инициализационные дампы — `migrations/` должен быть единственным источником правды.

## Сиды

- Сиды находятся в `seeds/seeds.sql` и применяются вручную командой `scripts/seed_db.py`.
- Скрипт `seed_db.py` использует `app.config.DB_URL` и подключается напрямую к базе.

## Тестирование

- Локально (с Poetry):

```bash
poetry install
poetry run pytest -q
```

- В контейнере:

```bash
docker-compose exec app pytest -q
```

## Разработка локально

1. Установите Poetry (если не установлен):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Установите зависимости и запустите сервис:

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

## Полезные команды

- Применить миграции локально: `poetry run python scripts/migrate.py`
- Загрузить сиды: `poetry run python scripts/seed_db.py` или через `docker-compose exec app python3 scripts/seed_db.py`
- Запустить тесты: `poetry run pytest` или `docker-compose exec app pytest`
 - Запустить тесты: `poetry run pytest` или `docker-compose exec app pytest`
- Через скрипт: `./scripts/run_tests.py` (автоматически использует Poetry / venv / python)

## Примечания

- Проект использует `asyncpg` для асинхронной работы с PostgreSQL (без ORM).
- `migrations/` — единственный источник правды для схемы БД; старые инициализационные дампы были удалены.
- Если нужно экспортировать `requirements.txt` для окружений без Poetry, используйте:

```bash
poetry export -f requirements.txt --without-hashes --output requirements.txt
```

Если хотите, я могу добавить простую CI конфигурацию (GitHub Actions) для прогонки тестов и применения миграций на PR.