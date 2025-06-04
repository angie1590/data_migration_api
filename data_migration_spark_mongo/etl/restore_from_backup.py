import os
from datetime import datetime
from pyspark.sql import SparkSession
from config.logger_config import setup_logger
from config.spark_config import get_spark_session
from etl.common import clean_collection

logger = setup_logger("restore_from_backup")

BACKUP_DIR = os.path.join(os.path.dirname(__file__), "../backups")
TABLES = ["departments", "jobs", "hired_employees"]

def find_latest_backup(table_name: str) -> str:
    if not os.path.exists(BACKUP_DIR):
        raise FileNotFoundError(f"No existe el directorio de backups: '{BACKUP_DIR}'")

    files = [
        f for f in os.listdir(BACKUP_DIR)
        if f.startswith(table_name) and f.endswith(".avro")
    ]
    if not files:
        raise FileNotFoundError(f"No se encontraron backups para la tabla '{table_name}'.")

    files.sort(reverse=True)
    return os.path.join(BACKUP_DIR, files[0])

def restore_table(spark: SparkSession, table_name: str, file_path: str):
    logger.info(f"Restaurando '{table_name}' desde '{file_path}'")
    clean_collection(table_name)

    df = spark.read.format("avro").load(file_path)
    df.write.format("mongo") \
        .mode("append") \
        .option("collection", table_name) \
        .save()
    logger.info(f"Restauración de '{table_name}' completada con {df.count()} registros")

def run():
    logger.info("Iniciando proceso de restauración desde backups")
    spark = get_spark_session()

    for table in TABLES:
        try:
            latest_backup = find_latest_backup(table)
            restore_table(spark, table, latest_backup)
        except Exception as e:
            logger.error(f"Error restaurando '{table}': {e}")

    logger.info("Proceso de restauración finalizado")

if __name__ == "__main__":
    run()
