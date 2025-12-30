from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, explode, when
import os

spark = SparkSession.builder.appName("WeatherTransformation").getOrCreate()

def transform_data():
    json_path = "bronze/*.json"
    raw_df = spark.read.option("multiline", "true").json(json_path)
    
    silver_df = raw_df.select(
        col("name").alias("City"),
        col("state").alias("State"),
        col("main.temp").alias("Temperature_C"),
        col("main.humidity").alias("Humidity"),
        col("wind.speed").alias("Wind_Speed_Kmph"),
        col("weather")[0]["main"].alias("Condition"),
        current_timestamp().alias("Processed_At")
    )
    
    silver_df.write.mode("overwrite").parquet("silver_weather")
    
    gold_df = silver_df.withColumn(
        "Status",
        when(col("Temperature_C") > 40, "Heat Wave").otherwise(
            when(col("Wind_Speed_Kmph") > 20, "High Wind").otherwise("Normal")
        )
    )
    
    gold_df.write.mode("overwrite").partitionBy("State").parquet("gold_weather")
    print("Transformation complete.")

if __name__ == "__main__":
    transform_data()