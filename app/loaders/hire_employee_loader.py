from datetime import datetime
from sqlalchemy.orm import Session
from app.models import HiredEmployee, Department, Job
from app.schemas import HiredEmployeeCreate
from app.loaders.base_loader import load_csv_generic
from app.core.logger import logger

def get_hired_employee_validator(session: Session):
    invalid_departments = set()
    invalid_jobs = set()

    def validate_hired_employee(row):
        try:
            datetime.strptime(row["datetime"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise ValueError(f"Invalid datetime format: {row['datetime']}")

        if not session.get(Department, row["department_id"]):
            invalid_departments.add(row["department_id"])
            raise ValueError(f"Department ID {row['department_id']} does not exist")

        if not session.get(Job, row["job_id"]):
            invalid_jobs.add(row["job_id"])
            raise ValueError(f"Job ID {row['job_id']} does not exist")

    def log_summary():
        if invalid_departments:
            logger.warning(f"Invalid department_ids found: {sorted(invalid_departments)}")
        if invalid_jobs:
            logger.warning(f"Invalid job_ids found: {sorted(invalid_jobs)}")

    return validate_hired_employee, log_summary

def load_hired_employees(session: Session):
    validator_fn, log_summary = get_hired_employee_validator(session)

    load_csv_generic(
        session=session,
        csv_path="data/hired_employees (1).csv",
        model_class=HiredEmployee,
        schema_class=HiredEmployeeCreate,
        validator=validator_fn
    )

    log_summary()
