from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# 1. Création de la session Spark
spark = SparkSession.builder \
    .appName("IoT_Sensor_Processing") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Définition du schéma
json_schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("location", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("metrics", StructType([
        StructField("temperature", DoubleType(), True),
        StructField("humidity", DoubleType(), True)
    ])),
    StructField("status", StringType(), True)
])

# 3. Lecture Kafka 
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "iot_sensor_data") \
    .option("startingOffsets", "earliest") \
    .load()

# 4. Transformation DES DONNÉES
processed_stream = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), json_schema).alias("data")) \
    .select("data.*")

analyzed_stream = processed_stream.withColumn("is_critical", expr("metrics.temperature > 50"))

# --- CORRECTIONS APPLIQUÉES ICI ---
print("--- Démarrage de l'écriture vers MongoDB ---")

# URI de connexion
MONGO_URI = "mongodb://admin:password123@mongodb:27017/iot_database.sensor_data?authSource=admin"

query = analyzed_stream.writeStream \
    .outputMode("append") \
    .format("mongodb") \
    .option("spark.mongodb.connection.uri", MONGO_URI) \
    .option("spark.mongodb.database", "iot_database") \
    .option("spark.mongodb.collection", "sensor_data") \
    .option("checkpointLocation", "/tmp/checkpoint_dir_v3") \
    .start()

query.awaitTermination()