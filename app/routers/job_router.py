from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import JobCreate
from app.models import Job
from app.database import get_db
from app.core.logger import logger

router = APIRouter(tags=["Jobs"])

@router.post("", status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    existing = db.get(Job, job.id)
    if existing:
        logger.warning(f"Attempted to insert duplicate job ID {job.id}")
        raise HTTPException(status_code=400, detail=f"Job with ID {job.id} already exists")

    new_job = Job(**job.model_dump())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    logger.info(f"Inserted new job with ID {job.id}")
    return new_job


@router.post("/batch", status_code=201)
def create_jobs_batch(jobs: list[JobCreate], db: Session = Depends(get_db)):
    if len(jobs) > 1000:
        logger.error("Batch size exceeded limit of 1000")
        raise HTTPException(status_code=400, detail="Maximum batch size is 1000")

    inserted_ids = []
    skipped_ids = []

    for job in jobs:
        try:
            if db.get(Job, job.id):
                skipped_ids.append(job.id)
                logger.warning(f"Skipped duplicate job ID {job.id}")
                continue

            new_job = Job(**job.model_dump())
            db.add(new_job)
            inserted_ids.append(job.id)

        except Exception as e:
            logger.exception(f"Unexpected error while processing job ID {job.id}: {e}")
            raise HTTPException(status_code=500, detail="Unexpected server error")

    db.commit()
    logger.info(f"Inserted {len(inserted_ids)} jobs. Skipped {len(skipped_ids)} duplicates.")

    return {
        "message": f"{len(inserted_ids)} jobs inserted successfully.",
        "inserted_ids": inserted_ids,
        "skipped_duplicates": skipped_ids
    }
