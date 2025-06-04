
from pyspark.sql import SparkSession

from pyspark.sql import SparkSession

def get_spark_session(app_name="DataMigrationMongo") -> SparkSession:
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.jars.packages",
                "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,"
                "org.apache.spark:spark-avro_2.12:3.5.1") \
        .config("spark.mongodb.output.uri", "mongodb://localhost:27017/challenge") \
        .config("spark.mongodb.read.connection.uri", "mongodb://localhost:27017/challenge") \
        .getOrCreate()

    return spark


