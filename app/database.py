import os
import asyncpg
import asyncio
from fastapi import Depends
from contextlib import asynccontextmanager
from app.config import DB_URL

db_pool = None

async def init_pool():
    global db_pool
    db_pool = await asyncpg.create_pool(DB_URL, min_size=2, max_size=10)

async def apply_migrations():
    """apply migrations using scripts/migrate.py (runs in thread to avoid blocking loop)"""
    import scripts.migrate as migrate
    await asyncio.to_thread(migrate.main)

async def run_scripts():
    """backwards-compatible wrapper: применить миграции через мигратор"""
    await apply_migrations()

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