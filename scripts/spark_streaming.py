from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# 1. Création de la session Spark
# On ajoute les "packages" nécessaires pour que Spark sache parler à Kafka
spark = SparkSession.builder \
    .appName("IoT_Sensor_Processing") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN") # Pour éviter d'avoir trop de blabla dans la console

# 2. Définition du schéma (La structure de tes données JSON)
# C'est obligatoire en Streaming structuré
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

# 3. Lecture du flux Kafka (ReadStream)
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "iot_sensor_data") \
    .option("startingOffsets", "latest") \
    .load()

# 4. Transformation des données
# Kafka envoie les données sous forme binaire (colonne 'value'). Il faut les convertir en String puis en JSON.
processed_stream = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), json_schema).alias("data")) \
    .select("data.*") # On "aplatit" la structure pour avoir les colonnes directes

# Petit traitement Data Engineer : On ajoute une colonne "Alert" si T° > 800
analyzed_stream = processed_stream.withColumn("is_critical", expr("metrics.temperature > 50"))

# 5. Affichage dans la console (WriteStream)
query = analyzed_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

print("--- Streaming Spark démarré ---")
query.awaitTermination()