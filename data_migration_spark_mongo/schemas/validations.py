from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_timestamp
from config.logger_config import setup_logger

logger = setup_logger(__name__)

def validate_hired_employees(df: DataFrame, df_departments: DataFrame, df_jobs: DataFrame) -> DataFrame:
    required_cols = {"id", "name", "datetime", "department_id", "job_id"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    total_records = df.count()
    logger.info(f"Total registros leídos: {total_records}")

    df_clean = df.dropna(subset=list(required_cols))
    after_dropna = df_clean.count()
    logger.info(f"Registros luego de eliminar nulos: {after_dropna} (descartados: {total_records - after_dropna})")

    df_clean = df_clean.withColumn("datetime_parsed", to_timestamp("datetime"))
    df_clean = df_clean.filter(col("datetime_parsed").isNotNull()).drop("datetime").withColumnRenamed("datetime_parsed", "datetime")
    after_date_validation = df_clean.count()
    logger.info(f"Registros válidos tras validar datetime ISO: {after_date_validation}")

    df_clean = df_clean.join(
        df_departments.select("id").withColumnRenamed("id", "dep_id"),
        df_clean["department_id"] == col("dep_id"),
        "inner"
    ).drop("dep_id")
    after_dept_validation = df_clean.count()
    logger.info(f"Registros válidos tras validar department_id: {after_dept_validation}")

    df_clean = df_clean.join(
        df_jobs.select("id").withColumnRenamed("id", "job_ref_id"),
        df_clean["job_id"] == col("job_ref_id"),
        "inner"
    ).drop("job_ref_id")
    final_count = df_clean.count()
    logger.info(f"Registros finales tras validar job_id: {final_count} (total descartados: {total_records - final_count})")

    return df_clean
