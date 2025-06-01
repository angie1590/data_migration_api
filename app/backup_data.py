import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.exporters.backup_departments import backup_departments
from app.exporters.backup_jobs import backup_jobs
from app.exporters.backup_hired_employees import backup_hired_employees
from app.core.logger import logger

TABLE_BACKUPS = {
    "departments": backup_departments,
    "jobs": backup_jobs,
    "hired_employees": backup_hired_employees
}

def backup_all(session: Session):
    for name, func in TABLE_BACKUPS.items():
        logger.info(f"Backing up table: {name}")
        func(session)
        logger.info(f"Backup of table {name} completed.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python backup_data.py [all|departments|jobs|hired_employees]")
        sys.exit(1)

    target = sys.argv[1]
    session = SessionLocal()

    if target == "all":
        backup_all(session)
    elif target in TABLE_BACKUPS:
        logger.info(f"Backing up table: {target}")
        TABLE_BACKUPS[target](session)
        logger.info(f"Backup of table {target} completed.")
    else:
        print(f"Unknown table name '{target}'. Valid options: all, {', '.join(TABLE_BACKUPS.keys())}")
        sys.exit(1)

    session.close()

if __name__ == "__main__":
    main()
