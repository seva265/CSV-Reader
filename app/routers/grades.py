from fastapi import APIRouter, File, UploadFile, HTTPException
import csv
import codecs
from datetime import datetime
from typing import List

from app.schemas import UploadGradesResponse
from app.database import get_db
from app.services import insert_marks

router = APIRouter()


@router.post("/upload-grades", response_model=UploadGradesResponse)
async def upload_grades(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail='File has no name')
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail='Not a .csv')

    stream = codecs.iterdecode(file.file, 'utf-8-sig')
    csv_reader = csv.DictReader(stream, delimiter=';')

    expected_headers = ['Дата', 'Номер группы', 'ФИО', 'Оценка']
    if csv_reader.fieldnames != expected_headers:
        raise HTTPException(status_code=400, detail='Invalid headers')

    marks_to_insert: List[tuple] = []
    for row_number, row_content in enumerate(csv_reader, start=1):
        try:
            date = row_content['Дата'].strip()
            date = datetime.strptime(date, "%d.%m.%Y").date()

            group_number = row_content['Номер группы'].strip()
            full_name = row_content['ФИО'].strip()
            mark = row_content['Оценка'].strip()

            if not full_name or not mark:
                continue

            if int(mark) > 5 or int(mark) < 2:
                continue

            marks_to_insert.append((date, group_number, full_name, int(mark)))

        except Exception:
            continue

    if not marks_to_insert:
        return {"status": "ok", "records_loaded": 0, "students": 0}

    async with get_db() as conn:
        inserted, unique_students = await insert_marks(conn, marks_to_insert)
        return {"status": "ok", "records_loaded": inserted, "students": unique_students}
