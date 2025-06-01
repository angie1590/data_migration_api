from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import DepartmentCreate
from app.models import Department
from app.database import get_db
from app.core.logger import logger

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("", status_code=201)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    existing = db.get(Department, dept.id)
    if existing:
        logger.warning(f"Attempted to insert duplicate department ID {dept.id}")
        raise HTTPException(status_code=400, detail=f"Department with ID {dept.id} already exists")

    new_department = Department(**dept.model_dump())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    logger.info(f"Inserted new department with ID {dept.id}")
    return new_department


@router.post("/batch", status_code=201)
def create_departments_batch(departments: list[DepartmentCreate], db: Session = Depends(get_db)):
    if len(departments) > 1000:
        logger.error("Batch size exceeded limit of 1000")
        raise HTTPException(status_code=400, detail="Maximum batch size is 1000")

    inserted_ids = []
    skipped_ids = []

    for dept in departments:
        try:
            if db.get(Department, dept.id):
                skipped_ids.append(dept.id)
                logger.warning(f"Skipped duplicate department ID {dept.id}")
                continue

            department = Department(**dept.model_dump())
            db.add(department)
            inserted_ids.append(dept.id)

        except Exception as e:
            logger.exception(f"Unexpected error while processing department ID {dept.id}: {e}")
            raise HTTPException(status_code=500, detail="Unexpected server error")

    db.commit()
    logger.info(f"Inserted {len(inserted_ids)} departments. Skipped {len(skipped_ids)} duplicates.")

    return {
        "message": f"{len(inserted_ids)} departments inserted successfully.",
        "inserted_ids": inserted_ids,
        "skipped_duplicates": skipped_ids
    }
