#!/usr/bin/env python3
"""
простой мигратор: применяет sql-файлы из папки migrations по имени в порядке возрастания
создаёт таблицу schema_migrations для учёта применённых файлов
"""
import asyncio
import sys
from pathlib import Path
import asyncpg
from app.config import DB_URL


async def run_migrations(migrations_dir: str = "migrations"):
    conn = await asyncpg.connect(DB_URL)
    try:
        # ensure migrations table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                filename TEXT PRIMARY KEY,
                applied_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
            """
        )

        mig_dir = Path(migrations_dir)
        if not mig_dir.exists():
            print(f"no migrations folder: {migrations_dir}")
            return

        files = sorted([p for p in mig_dir.iterdir() if p.suffix == ".sql"])
        for f in files:
            name = f.name
            applied = await conn.fetchval("SELECT 1 FROM schema_migrations WHERE filename=$1", name)
            if applied:
                continue

            sql = f.read_text(encoding="utf-8")
            try:
                async with conn.transaction():
                    await conn.execute(sql)
                    await conn.execute("INSERT INTO schema_migrations(filename) VALUES($1)", name)
                print(f"applied {name}")
            except Exception as e:
                print(f"failed {name}: {e}")
                raise
    finally:
        await conn.close()


def main():
    migrations_dir = sys.argv[1] if len(sys.argv) > 1 else "migrations"
    asyncio.run(run_migrations(migrations_dir))


if __name__ == "__main__":
    main()
