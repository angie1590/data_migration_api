from pyspark.sql import SparkSession
from pyspark.sql.functions import col, quarter, year, count, lit
from pyspark.sql import functions as F

def get_hiring_quarterly_report():
    spark = SparkSession.builder \
        .appName("HiringQuarterlyReport") \
        .config("spark.driver.extraClassPath", "drivers/sqlite-jdbc-3.36.0.3.jar") \
        .getOrCreate()

    jdbc_url = "jdbc:sqlite:app.db"
    query = "(SELECT he.id, he.datetime, j.job, d.department FROM hired_employees he JOIN jobs j ON he.job_id = j.id JOIN departments d ON he.department_id = d.id) AS hired_info"

    df = spark.read.format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", query) \
        .option("driver", "org.sqlite.JDBC") \
        .load()

    df_2021 = df.filter(year(col("datetime")) == 2021)
    df_quartered = df_2021.withColumn("quarter", quarter(col("datetime")))
    result = df_quartered.groupBy("department", "job", "quarter").agg(count("id").alias("hires"))
    pivoted = result.groupBy("department", "job").pivot("quarter", [1, 2, 3, 4]).sum("hires")

    filled = pivoted.fillna(0).orderBy("department", "job")

    data = [row.asDict() for row in filled.collect()]

    spark.stop()
    return data
