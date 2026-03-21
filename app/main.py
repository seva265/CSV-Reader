import csv
import codecs
from io import TextIOWrapper

import asyncpg
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload-grades")
async def upload_grades(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail='File has no name')
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail='Not a .csv')
    stream = codecs.iterdecode(file.file, 'utf-8')
    csv_reader = csv.DictReader(stream)

    expected_headers = ['Дата', 'Номер группы', 'ФИО', 'Оценка']
    if csv_reader.fieldnames != expected_headers:
        raise HTTPException(status_code=400, detail='Invalid headers')
    
    #валидация и добавление корректных записей для дальнейшей вставки в бд
    marks_to_insert = []
    for row_number, row_content in enumerate(csv_reader, start=1):
        try:
            date = row_content['Дата'].strip()
            group_number = row_content['Номер группы'].strip()
            full_name = row_content['ФИО'].strip()
            mark = row_content['Оценка'].strip()

            if not full_name or not mark:
                print(f'Warning: Empty name or mark in line {row_number}. Skipped')
                continue

            if int(mark) > 5 or int(mark) < 2:
                print(f'Warning: Incorrect mark on line {row_number}. Skipped')
                continue
            
            marks_to_insert.append((date, group_number, full_name, mark))

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
    
    sql_query = '''INSERT INTO marks (record_date, group_number, full_name, grade)
                   VALUES ($1, $2, $3, $4)'''
    async with db.pool.acquire() as connection:
        await connection.executemany(sql_query, marks_to_insert)
        return {
            "status": "ok",
            "records_loaded": len(marks_to_insert),
            "students": len(set([x[2] for x in marks_to_insert]))
            }