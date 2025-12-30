from pyspark.sql import SparkSession

def check_gold_data():
    spark = SparkSession.builder.appName("Check_Data").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    print("\n--- Reading the Gold Layer ---")
    df = spark.read.parquet("gold_weather")
    
    # Show the top ranked cities
    df.orderBy("Temp_Rank").show()

    print(f"Total records in Gold: {df.count()}")

if __name__ == "__main__":
    check_gold_data()