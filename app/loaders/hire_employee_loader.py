from datetime import datetime
from sqlalchemy.orm import Session
from app.models import HiredEmployee
from app.schemas import HiredEmployeeCreate
from app.loaders.base_loader import load_csv_generic

def validate_hired_employee(row):
    try:
        datetime.strptime(row["datetime"], "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ValueError(f"Invalid datetime format: {row['datetime']}")

def load_hired_employees(session: Session):
    load_csv_generic(
        session=session,
        csv_path="data/hired_employees (1).csv",
        model_class=HiredEmployee,
        schema_class=HiredEmployeeCreate,
        validator=validate_hired_employee
    )
