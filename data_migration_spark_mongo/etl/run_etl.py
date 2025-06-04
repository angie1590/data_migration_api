import logging
from etl.load_departments import run as load_departments
from etl.load_jobs import run as load_jobs
from etl.load_hired_employees import run as load_hired_employees

from config.logger_config import setup_logger

logger = setup_logger("etl_orchestrator")

def main():
    logger.info(">>> Iniciando ETL completo...")

    try:
        logger.info("1. Cargando datos de Departments...")
        load_departments()

        logger.info("2. Cargando datos de Jobs...")
        load_jobs()

        logger.info("3. Cargando datos de Hired Employees...")
        load_hired_employees()

        logger.info(">>> ETL completado exitosamente.")
    except Exception as e:
        logger.exception(f"Error durante la ejecución del ETL: {e}")

if __name__ == "__main__":
    main()
