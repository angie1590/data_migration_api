from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
from config.logger_config import setup_logger

logger = setup_logger("api")

client = MongoClient("mongodb://localhost:27017/")
db = client["challenge"]

app = FastAPI(title="API MongoDB - Data Migration", version="1.0")

class Department(BaseModel):
    id: int
    department: str

class Job(BaseModel):
    id: int
    job: str

class HiredEmployee(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

def insert_records(collection_name: str, records: List[dict]):
    if len(records) > 1000:
        logger.warning(f"Límite de batch excedido para '{collection_name}'")
        raise HTTPException(status_code=400, detail="El tamaño máximo permitido por batch es de 1000 registros.")

    collection = db[collection_name]
    existing_ids = {doc["id"] for doc in collection.find({}, {"id": 1})}
    nuevos = [r for r in records if r["id"] not in existing_ids]

    if not nuevos:
        logger.info(f"No se insertaron registros en '{collection_name}' porque todos eran duplicados.")
        raise HTTPException(status_code=409, detail="Los registros ya existen. No se insertó ningún dato.")

    result = collection.insert_many(nuevos)
    logger.info(f"Insertados {len(result.inserted_ids)} registros en '{collection_name}'")
    return {"registros_insertados": len(result.inserted_ids)}

@app.post("/departments", summary="Insertar un departamento")
def insertar_departamento(dept: Department):
    return insert_records("departments", [dept.dict()])

@app.post("/departments/batch", summary="Insertar múltiples departamentos")
def insertar_departamentos(depts: List[Department]):
    return insert_records("departments", [d.dict() for d in depts])

@app.post("/jobs", summary="Insertar un puesto de trabajo")
def insertar_puesto(job: Job):
    return insert_records("jobs", [job.dict()])

@app.post("/jobs/batch", summary="Insertar múltiples puestos de trabajo")
def insertar_puestos(jobs: List[Job]):
    return insert_records("jobs", [j.dict() for j in jobs])

@app.post("/hired_employees", summary="Insertar un empleado contratado")
def insertar_empleado(emp: HiredEmployee):
    return insert_records("hired_employees", [emp.dict()])

@app.post("/hired_employees/batch", summary="Insertar múltiples empleados contratados")
def insertar_empleados(emps: List[HiredEmployee]):
    return insert_records("hired_employees", [e.dict() for e in emps])
