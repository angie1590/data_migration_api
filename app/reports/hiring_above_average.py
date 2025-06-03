from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, count, avg

def generate_hiring_above_average_report():
    spark = SparkSession.builder \
        .appName("HiringAboveAverage") \
        .config("spark.driver.extraClassPath", "drivers/sqlite-jdbc-3.36.0.3.jar") \
        .getOrCreate()

    jdbc_url = "jdbc:sqlite:app.db"

    query = """
    (
    SELECT he.id AS employee_id,
            he.datetime,
            d.id AS department_id,
            d.department
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    ) AS hired_info
    """

    df = spark.read.format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", query) \
        .option("driver", "org.sqlite.JDBC") \
        .load()

    df_2021 = df.filter(year(col("datetime")) == 2021)

    hires_per_department = df_2021.groupBy("department_id", "department").agg(count("employee_id").alias("hired"))

    avg_hires = hires_per_department.agg(avg("hired").alias("avg_hires")).collect()[0]["avg_hires"]

    result = hires_per_department \
        .filter(col("hired") > avg_hires) \
        .withColumnRenamed("department_id", "id") \
        .orderBy(col("hired").desc())

    data = [row.asDict() for row in result.collect()]

    spark.stop()

    return data
