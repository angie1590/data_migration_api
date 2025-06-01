from app.database import SessionLocal
from app.loaders.department_loader import load_departments
from app.loaders.job_loader import load_jobs
from app.loaders.hire_employee_loader import load_hired_employees
from app.core.logger import logger

def load_all_data():
    session = SessionLocal()
    try:
        logger.info("🚀 Starting full data load...")

        logger.info("🔹 Loading departments...")
        load_departments(session)

        logger.info("🔹 Loading jobs...")
        load_jobs(session)

        logger.info("🔹 Loading hired employees...")
        load_hired_employees(session)

        logger.info("✅ Data load completed successfully.")
    except Exception as e:
        logger.error(f"❌ Data load failed: {e}")
    finally:
        session.close()
        logger.info("🔚 Database session closed.")
