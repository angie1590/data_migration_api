import os
from datetime import datetime
from fastavro import writer, parse_schema, reader
from sqlalchemy.orm import Session
from app.core.logger import logger



BACKUP_DIR = "backups"

def export_to_avro(records: list[dict], schema: dict, name: str) -> None:
    if not records:
        logger.warning(f"No records to backup for {name}")
        return

    parsed_schema = parse_schema(schema)

    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filepath = os.path.join(BACKUP_DIR, f"{name}_{timestamp}.avro")

    try:
        with open(filepath, "wb") as out:
            writer(out, parsed_schema, records)
        logger.info(f"✅ Backup created: {filepath} ({len(records)} records)")
    except Exception as e:
        logger.exception(f"❌ Failed to backup {name}: {e}")


def import_from_avro(session: Session, model_class, avro_path: str):
    if not os.path.exists(avro_path):
        logger.error(f"Backup file not found at path: {avro_path}")
        return

    try:
        count = 0
        with open(avro_path, "rb") as f:
            for record in reader(f):
                session.merge(model_class(**record))
                count += 1
        session.commit()
        logger.info(f"✅ Restored {count} records into table '{model_class.__tablename__}' from {avro_path}")
    except Exception as e:
        logger.exception(f"❌ Failed to restore from AVRO: {e}")