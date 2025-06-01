from app import models
from app.loaders.base_loader import load_csv_generic
from app.schemas import JobCreate
from sqlalchemy.orm import Session

def load_jobs(session: Session):
    load_csv_generic(
        session=session,
        csv_path="data/jobs.csv",
        model_class=models.Job,
        schema_class=JobCreate
    )