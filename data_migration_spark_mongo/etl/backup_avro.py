import os
from datetime import datetime
from pyspark.sql import SparkSession
from config.logger_config import setup_logger
from config.spark_config import get_spark_session

logger = setup_logger("backup_avro")

BACKUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backups"))

def backup_collection(spark, collection_name: str, db_name: str = "challenge"):
    date_suffix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{collection_name}-{date_suffix}.avro"
    output_path = os.path.join(BACKUP_DIR, filename)

    logger.info(f"Iniciando backup de colección '{collection_name}' en '{output_path}'")

    df = spark.read.format("mongo") \
        .option("uri", "mongodb://localhost:27017") \
        .option("database", db_name) \
        .option("collection", collection_name) \
        .load()

    df.write.format("avro").mode("overwrite").save(output_path)

    logger.info(f"Backup completado para '{collection_name}' → {filename}")

def run():
    logger.info("Iniciando proceso de backup en formato AVRO...")

    spark = get_spark_session()

    collections = ["departments", "jobs", "hired_employees"]
    for collection in collections:
        try:
            backup_collection(spark, collection)
        except Exception as e:
            logger.error(f"Error al respaldar '{collection}': {e}")

    logger.info("Proceso de backup finalizado.")

if __name__ == "__main__":
    run()