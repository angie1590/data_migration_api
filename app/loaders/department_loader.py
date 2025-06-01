from app import models
from app.loaders.base_loader import load_csv_generic
from app.schemas import DepartmentCreate
from sqlalchemy.orm import Session

def load_departments(session: Session):
    load_csv_generic(
        session=session,
        csv_path="data/departments.csv",
        model_class=models.Department,
        schema_class=DepartmentCreate
    )