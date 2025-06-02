from app.database import SessionLocal
from app.models import Department, Job, HiredEmployee
from app.core.logger import logger

def clean_all_data():
    db = SessionLocal()
    try:
        db.query(HiredEmployee).delete()
        db.query(Job).delete()
        db.query(Department).delete()
        db.commit()
        logger.info("✅ All data deleted from the database.")
    except Exception as e:
        logger.error(f"❌ Failed to delete data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clean_all_data()