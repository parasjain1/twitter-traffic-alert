from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from mtwitter.predictor import predict

import os

# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.6 pyspark-shell'
print(os.environ.get('PYSPARK_SUBMIT_ARGS'))


@udf
def prediction(tweet):
    return str(predict([tweet.decode("utf-8")])[0])


@udf
def to_string_value(tweet):
    return tweet.decode("utf-8")


if __name__ == '__main__':

    kafka_broker = 'kafka:9093'  # Docker IP for Kafka Broker as job would be submitted to the VM
    kafka_topic = 'twitter-test'

    spark = SparkSession \
        .builder \
        .appName("twitter-stream-app") \
        .master("spark://spark:7077") \
        .config("spark.executor.memory", "1g") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_broker) \
        .option("kafka.max.partition.fetch.bytes", 1024 * 1024 * 50) \
        .option("kafka.fetch.max.bytes", 1024 * 1024 * 50) \
        .option("subscribe", kafka_topic) \
        .load()

    console_output = df.select(to_string_value("value"), prediction("value").alias("prediction")) \
        .show(df.count(), False) \
        .writeStream \
        .outputMode("append") \
        .format("console")  \
        .start()

    console_output.awaitTermination()
