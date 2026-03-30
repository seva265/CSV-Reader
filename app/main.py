import csv
import codecs
from datetime import datetime
from typing import List

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_pool, close_pool

from app.routers import grades as grades_router
from app.routers import analysis as analysis_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    yield
    await close_pool()


app = FastAPI(lifespan=lifespan)


@app.get("/", include_in_schema=False)
def read_root():
    return {"Hello": "World"}


app.include_router(grades_router.router)
app.include_router(analysis_router.router)