from sqlalchemy.orm import Session
from app.models import Job
from app.exporters.avro_utils import export_to_avro

job_schema = {
    "doc": "Backup of jobs table",
    "name": "Job",
    "namespace": "com.migration.data",
    "type": "record",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "job", "type": "string"}
    ]
}

def backup_jobs(session: Session):
    records = [
        {"id": j.id, "job": j.job}
        for j in session.query(Job).all()
    ]
    export_to_avro(records, job_schema, "jobs")

