from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas import HiredEmployeeCreate
from app.models import HiredEmployee, Department, Job
from app.database import get_db
from app.core.logger import logger

router = APIRouter(tags=["Hired Employees"])

@router.post("", status_code=201)
def create_hired_employee(emp: HiredEmployeeCreate, db: Session = Depends(get_db)):
    if db.get(HiredEmployee, emp.id):
        logger.warning(f"Duplicate employee ID {emp.id}")
        raise HTTPException(status_code=400, detail=f"Employee ID {emp.id} already exists")

    if not db.get(Department, emp.department_id):
        logger.warning(f"Invalid department_id {emp.department_id} for employee ID {emp.id}")
        raise HTTPException(status_code=400, detail=f"Department ID {emp.department_id} does not exist")

    if not db.get(Job, emp.job_id):
        logger.warning(f"Invalid job_id {emp.job_id} for employee ID {emp.id}")
        raise HTTPException(status_code=400, detail=f"Job ID {emp.job_id} does not exist")

    new_emp = HiredEmployee(**emp.model_dump())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    logger.info(f"Inserted employee ID {emp.id}")
    return new_emp


@router.post("/batch", status_code=201)
def create_hired_employees_batch(employees: list[HiredEmployeeCreate], db: Session = Depends(get_db)):
    if len(employees) > 1000:
        logger.error("Batch size exceeded limit of 1000")
        raise HTTPException(status_code=400, detail="Maximum batch size is 1000")

    inserted_ids = []
    skipped_ids = []

    for emp in employees:
        try:
            if db.get(HiredEmployee, emp.id):
                skipped_ids.append(emp.id)
                logger.warning(f"Skipped duplicate employee ID {emp.id}")
                continue

            if not db.get(Department, emp.department_id):
                logger.warning(f"Invalid department_id {emp.department_id} for employee ID {emp.id}")
                continue

            if not db.get(Job, emp.job_id):
                logger.warning(f"Invalid job_id {emp.job_id} for employee ID {emp.id}")
                continue

            new_emp = HiredEmployee(**emp.model_dump())
            db.add(new_emp)
            inserted_ids.append(emp.id)

        except Exception as e:
            logger.exception(f"Error processing employee ID {emp.id}: {e}")
            raise HTTPException(status_code=500, detail="Unexpected error occurred")

    db.commit()
    logger.info(f"Inserted {len(inserted_ids)} employees. Skipped {len(skipped_ids)} duplicates.")
    return {
        "message": f"{len(inserted_ids)} employees inserted successfully.",
        "inserted_ids": inserted_ids,
        "skipped_duplicates": skipped_ids
    }
