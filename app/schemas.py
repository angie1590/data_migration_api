from pydantic import BaseModel
from typing import List
from datetime import datetime

class DepartmentCreate(BaseModel):
    id: int
    department: str

class JobCreate(BaseModel):
    id: int
    job: str

class HiredEmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int

class BatchHiredEmployee(BaseModel):
    employees: List[HiredEmployeeCreate]