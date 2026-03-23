import csv
import codecs
from io import TextIOWrapper
from datetime import datetime

import asyncpg
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from contextlib import asynccontextmanager
from app.database import init_pool, close_pool, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    yield
    await close_pool()

app = FastAPI(lifespan=lifespan)

@app.get("/", include_in_schema=False)
def read_root():
    return {"Hello": "World"}

@app.post("/upload-grades")
async def upload_grades(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail='File has no name')
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail='Not a .csv')
    stream = codecs.iterdecode(file.file, 'utf-8-sig') #utf-8-sig нужно что бы убрать префикс при парсе csv файла
    csv_reader = csv.DictReader(stream, delimiter=';')

    expected_headers = ['Дата', 'Номер группы', 'ФИО', 'Оценка']
    if csv_reader.fieldnames != expected_headers:
        print(csv_reader.fieldnames)
        raise HTTPException(status_code=400, detail='Invalid headers')
    
    
    #валидация и добавление корректных записей для дальнейшей вставки в бд
    marks_to_insert = []
    for row_number, row_content in enumerate(csv_reader, start=1):
        try:
            date = row_content['Дата'].strip()
            date = datetime.strptime(date, "%d.%m.%Y").date()

            group_number = row_content['Номер группы'].strip()
            full_name = row_content['ФИО'].strip()
            mark = row_content['Оценка'].strip()

            if not full_name or not mark:
                print(f'Warning: Empty name or mark in line {row_number}. Skipped')
                continue

            if int(mark) > 5 or int(mark) < 2:
                print(f'Warning: Incorrect mark on line {row_number}. Skipped')
                continue
            
            marks_to_insert.append((date, group_number, full_name, int(mark)))

        except Exception as e:
            print(f"Unexpected error on line {row_number}: {e}")
            continue
    
    #ответ если корректных значений в файле нет
    if not marks_to_insert:
        return {
        "status": "ok",
        "records_loaded": 0,
        "students": 0
        }
    
    insert_query = '''INSERT INTO marks (record_date, group_number, full_name, grade)
                   VALUES ($1, $2, $3, $4)'''
    
    async with get_db() as connection:
        await connection.executemany(insert_query, marks_to_insert)
        return {
            "status": "ok",
            "records_loaded": len(marks_to_insert),
            "students": len(set([x[2] for x in marks_to_insert]))
            }
    
@app.get("/students/more-than-3-twos")
async def analysis1():
    async with get_db() as conn:
        rows = await conn.fetch('''SELECT full_name, COUNT(*) as count_twos FROM marks
                                         WHERE grade = 2 GROUP BY full_name HAVING COUNT(*) > 3''')
        result = []
        for row in rows:
            result.append({"full_name": row["full_name"], "count_twos": row["count_twos"]})
        return result

@app.get("/students/less-than-5-twos")
async def analysis2():
    async with get_db() as conn:
        rows = await conn.fetch('''SELECT full_name, COUNT(*) FILTER (WHERE grade = 2) AS count_twos FROM marks
                                        GROUP BY full_name HAVING COUNT(*) FILTER (WHERE grade = 2) < 5;''')
        result = []
        for row in rows:
            result.append({"full_name": row["full_name"], "count_twos": row["count_twos"]})
        return result