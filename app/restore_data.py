import sys
from app.core.logger import logger
from app.exporters.avro_utils import import_from_avro
from app.models import Department, Job, HiredEmployee
from app.database import SessionLocal
from pathlib import Path
import os
from glob import glob


TABLE_MODEL_MAP = {
    "departments": Department,
    "jobs": Job,
    "hired_employees": HiredEmployee,
}


def get_latest_backup_file(table_name: str, base_dir: str = "backups") -> str | None:
    pattern = str(Path(base_dir) / f"{table_name}_*.avro")
    matching_files = glob(pattern)
    if not matching_files:
        return None
    return max(matching_files, key=os.path.getctime)


def restore_backup(table_name: str):
    logger.info(f"🚀 Starting restore process for table: {table_name}")

    base_dir = Path(__file__).resolve().parents[1] / "backups"
    logger.debug(f"🧭 Backup directory resolved to: {base_dir}")

    backup_file = get_latest_backup_file(table_name, base_dir=base_dir)
    if not backup_file:
        logger.error(f"❌ Backup file for table '{table_name}' not found in: {base_dir}")
        return

    logger.info(f"📄 Latest backup file found: {backup_file}")

    model_class = TABLE_MODEL_MAP.get(table_name)
    if not model_class:
        logger.error(f"❌ Model for table '{table_name}' not found.")
        return

    db = SessionLocal()
    try:
        import_from_avro(db, model_class, backup_file)
        logger.info(f"✅ Data restored for table '{table_name}' from file '{backup_file}'")
    except Exception as e:
        logger.exception(f"❌ Error restoring data for table '{table_name}': {e}")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("❌ You must provide the table name to restore. Example: make restore TABLE=departments")
        sys.exit(1)

    table = sys.argv[1]
    restore_backup(table)
