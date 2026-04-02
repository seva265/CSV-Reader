import os
import asyncio
from pathlib import Path
import asyncpg
import pytest
from app.config import DB_URL


def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        return asyncio.ensure_future(coro)
    else:
        return asyncio.run(coro)


async def _apply_sql(path: str):
    conn = await asyncpg.connect(DB_URL)
    try:
        sql = Path(path).read_text(encoding='utf-8')
        await conn.execute(sql)
    finally:
        await conn.close()


def apply_sql_file(path: str):
    _run_async(_apply_sql(path))


@pytest.fixture(scope="session")
def seed_db():
    """apply sql/seeds.sql to real db when USE_REAL_DB=1 is set"""
    if os.getenv("USE_REAL_DB") == "1":
        path = Path(__file__).parent / "seeds" / "seeds.sql"
        apply_sql_file(str(path))
    yield
