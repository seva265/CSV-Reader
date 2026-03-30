from fastapi import APIRouter
from typing import List

from app.schemas import StudentCount
from app.database import get_db
from app.services import get_students_with_more_than_n_twos, get_students_with_less_than_n_twos

router = APIRouter(prefix="/students")


@router.get("/more-than-3-twos", response_model=List[StudentCount])
async def more_than_3_twos():
    async with get_db() as conn:
        return await get_students_with_more_than_n_twos(conn, 3)


@router.get("/less-than-5-twos", response_model=List[StudentCount])
async def less_than_5_twos():
    async with get_db() as conn:
        return await get_students_with_less_than_n_twos(conn, 5)
