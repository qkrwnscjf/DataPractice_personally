from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from kafka import KafkaConsumer
import json

KAFKA_TOPIC = "stock_prices"
BOOTSTRAP_SERVERS = "localhost:9092"

# Spark 세션 생성
spark = SparkSession.builder \
    .appName("StockPriceProcessor") \
    .getOrCreate()

# 데이터 스키마 정의
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("symbol", StringType(), True),
    StructField("open", FloatType(), True),
    StructField("high", FloatType(), True),
    StructField("low", FloatType(), True),
    StructField("close", FloatType(), True),
    StructField("volume", FloatType(), True)
])

# Kafka Consumer 설정
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

for message in consumer:
    stock_df = spark.createDataFrame([message.value], schema=schema)
    
    # 이동 평균 계산 (5개 데이터 기준)
    moving_avg_df = stock_df.groupBy("symbol").agg(avg("close").alias("moving_avg"))
    
    moving_avg_df.show()
