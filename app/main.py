import csv
import codecs
from io import TextIOWrapper

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
    
    
