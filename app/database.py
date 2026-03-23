import os
import asyncpg
from fastapi import Depends
from contextlib import asynccontextmanager
from config import DB_URL

db_pool = None

async def run_scripts():
    assert db_pool is not None
    async with db_pool.acquire() as conn:
        path = os.path.join(os.path.dirname(__file__), "sql", "001_init.sql")
        with open(path, 'r', encoding='utf-8') as f:
            sql = f.read()
        await conn.execute(sql)

async def init_pool():
    global db_pool
    db_pool = await asyncpg.create_pool(DB_URL, min_size=2, max_size=10)
    await run_scripts()

async def close_pool():
    global db_pool
    if db_pool:
        await db_pool.close()

@asynccontextmanager
async def get_db():
    assert db_pool is not None

    conn = await db_pool.acquire()
    try:
        yield conn
    finally:
        await db_pool.release(conn)