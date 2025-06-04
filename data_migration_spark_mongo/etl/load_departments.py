from pyspark.sql.types import IntegerType, StringType
from config.logger_config import setup_logger
from config.spark_config import get_spark_session
from etl.common import clean_collection

logger = setup_logger("load_departments")

def run():
    logger.info("Iniciando proceso de carga de departments...")

    spark = get_spark_session()
    clean_collection("departments")

    df = spark.read.option("header", "false").csv("../data/departments.csv") \
        .toDF("id", "department")

    df = df.withColumn("id", df["id"].cast(IntegerType()))
    df = df.withColumn("department", df["department"].cast(StringType()))

    df_valid = df.dropna(subset=["id", "department"])

    df_valid.write.format("mongo") \
        .mode("append") \
        .option("collection", "departments") \
        .save()

    logger.info("Carga de departments finalizada.")

