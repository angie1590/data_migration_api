from pyspark.sql.types import IntegerType, StringType
from config.logger_config import setup_logger
from config.spark_config import get_spark_session
from etl.common import clean_collection

logger = setup_logger("load_jobs")

def run():
    logger.info("Iniciando proceso de carga de jobs...")

    spark = get_spark_session()
    clean_collection("jobs")

    df = spark.read.option("header", "false").csv("../data/jobs.csv") \
        .toDF("id", "job")

    # Validación de tipos
    df = df.withColumn("id", df["id"].cast(IntegerType()))
    df = df.withColumn("job", df["job"].cast(StringType()))

    # Filtrar registros válidos
    df_valid = df.dropna(subset=["id", "job"])
    registros_validos = df_valid.count()
    registros_invalidos = df.count() - registros_validos

    logger.info(f"Registros válidos: {registros_validos}")
    logger.info(f"Registros descartados por validación: {registros_invalidos}")

    df_valid.write.format("mongo") \
        .mode("append") \
        .option("collection", "jobs") \
        .save()

    logger.info("Carga de jobs finalizada.")
