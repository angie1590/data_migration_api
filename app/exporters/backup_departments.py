from sqlalchemy.orm import Session
from app.models import Department
from app.exporters.avro_utils import export_to_avro

department_schema = {
    "doc": "Backup of departments table",
    "name": "Department",
    "namespace": "com.migration.data",
    "type": "record",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "department", "type": "string"}
    ]
}

def backup_departments(session: Session):
    records = [
        {"id": d.id, "department": d.department}
        for d in session.query(Department).all()
    ]
    export_to_avro(records, department_schema, "departments")
