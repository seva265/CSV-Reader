#!/usr/bin/env python3
"""
заполнить бд тестовыми данными из sql/seeds.sql
"""
import asyncio
import os
import asyncpg
from app.config import DB_URL


async def apply_seeds():
    conn = await asyncpg.connect(DB_URL)
    try:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "seeds", "seeds.sql")
        with open(path, 'r', encoding='utf-8') as f:
            sql = f.read()
        await conn.execute(sql)
        print("seeds applied")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(apply_seeds())
