from config.logger_config import setup_logger
from schemas.validations import validate_hired_employees
from config.spark_config import get_spark_session
from etl.common import clean_collection

logger = setup_logger("load_hired_employees")

def run():
    logger.info("Iniciando proceso de carga de hired_employees...")

    spark = get_spark_session()

    clean_collection("hired_employees")

    df = spark.read.option("header", "false").csv("../data/hired_employees (1).csv") \
        .toDF("id", "name", "datetime", "department_id", "job_id")


    df_departments = spark.read.format("mongo") \
        .option("uri", "mongodb://localhost:27017") \
        .option("database", "challenge") \
        .option("collection", "departments") \
        .option("uri", "mongodb://localhost:27017") \
        .load()

    df_jobs = spark.read.format("mongo") \
        .option("uri", "mongodb://localhost:27017") \
        .option("database", "challenge") \
        .option("collection", "jobs") \
        .load()

    validated_df = validate_hired_employees(df, df_departments, df_jobs)

    validated_df.write.format("mongo") \
        .mode("append") \
        .option("collection", "hired_employees") \
        .save()

    logger.info("Carga de hired_employees finalizada.")
