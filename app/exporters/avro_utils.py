import os
from datetime import datetime
from fastavro import writer, parse_schema
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
