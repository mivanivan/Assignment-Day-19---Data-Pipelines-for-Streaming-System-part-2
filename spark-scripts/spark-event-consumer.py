import pyspark
import os
from dotenv import load_dotenv
from pathlib import Path
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, TimestampType

# Load environment variables
dotenv_path = Path("/opt/app/.env")
load_dotenv(dotenv_path=dotenv_path)

# Get environment variables
spark_hostname = os.getenv("SPARK_MASTER_HOST_NAME")
spark_port = os.getenv("SPARK_MASTER_PORT")
kafka_host = os.getenv("KAFKA_HOST")
kafka_topic = os.getenv("KAFKA_TOPIC_NAME")

# Set Spark master URL
spark_host = f"spark://{spark_hostname}:{spark_port}"

# Set PySpark submit arguments
os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 org.postgresql:postgresql:42.2.18 pyspark-shell"

# Initialize Spark context and session
sparkcontext = pyspark.SparkContext.getOrCreate(
    conf=(pyspark.SparkConf().setAppName("DibimbingStreaming").setMaster(spark_host))
)
sparkcontext.setLogLevel("WARN")
spark = pyspark.sql.SparkSession(sparkcontext)

# Define the schema of the JSON data
schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("furniture", StringType(), True),
    StructField("color", StringType(), True),
    StructField("price", IntegerType(), True),
    StructField("ts", LongType(), True)
])

# Read from Kafka topic
stream_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", f"{kafka_host}:9092")
    .option("subscribe", kafka_topic)
    .option("startingOffsets", "latest")
    .load()
)

# Select and parse the JSON data
parsed_df = (
    stream_df.selectExpr("CAST(value AS STRING)")
    .select(F.from_json(F.col("value"), schema).alias("data"))
    .select("data.*")
    .withColumn("timestamp", F.col("ts").cast(TimestampType()))
)

# Create a running total of the price
running_total_df = (
    parsed_df
    .withWatermark("timestamp", "1 minute")
    .groupBy(F.window("timestamp", "1 minute"))
    .agg(F.sum("price").alias("running_total"))
    .select(F.col("window.start").alias("timestamp"), F.col("running_total"))
)

# Write the running total data to the console with a trigger interval of 1 minute
query = (
    running_total_df.writeStream
    .outputMode("complete")
    .format("console")
    .trigger(processingTime="1 minute")
    .start()
    .awaitTermination()
)
