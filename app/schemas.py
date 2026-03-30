from pydantic import BaseModel
from typing import List


class UploadGradesResponse(BaseModel):
    status: str
    records_loaded: int
    students: int


class StudentCount(BaseModel):
    full_name: str
    count_twos: int
