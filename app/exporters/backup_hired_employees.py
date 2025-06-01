from sqlalchemy.orm import Session
from app.models import HiredEmployee
from app.exporters.avro_utils import export_to_avro

hired_employee_schema = {
    "doc": "Backup of hired_employees table",
    "name": "HiredEmployee",
    "namespace": "com.migration.data",
    "type": "record",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "datetime", "type": "string"},
        {"name": "department_id", "type": "int"},
        {"name": "job_id", "type": "int"}
    ]
}

def backup_hired_employees(session: Session):
    records = [
        {
            "id": e.id,
            "name": e.name,
            "datetime": e.datetime,
            "department_id": e.department_id,
            "job_id": e.job_id
        }
        for e in session.query(HiredEmployee).all()
    ]
    export_to_avro(records, hired_employee_schema, "hired_employees")
