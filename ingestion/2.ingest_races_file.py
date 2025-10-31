# Databricks notebook source
# MAGIC %md
# MAGIC ### Ingest races.csv file
# MAGIC #### Step 1 - Read the CSV file using spark dataframe reader

# COMMAND ----------

dbutils.widgets.text("p_data_source", "")
v_data_source = dbutils.widgets.get("p_data_source")

# COMMAND ----------

dbutils.widgets.text("p_file_date", "2021-03-21")
v_file_date = dbutils.widgets.get("p_file_date")

# COMMAND ----------

# MAGIC %run "../includes/configuration"

# COMMAND ----------

# MAGIC %run "../includes/common_functions"

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

# COMMAND ----------

races_schema = StructType(fields=[
    StructField("raceId", IntegerType(), False), # False because its the primary key and its not acceptable null values
    StructField("year", IntegerType(), True),
    StructField("round", IntegerType(), True),
    StructField("circuitId", IntegerType(), False),
    StructField("name", StringType(), True),
    StructField("date", StringType(), True),
    StructField("time", StringType(), True),
    StructField("url", StringType(), True)
])

# COMMAND ----------

races_df = spark.read \
    .option("header", True) \
    .schema(races_schema) \
    .csv(f"{raw_folder_path}/{v_file_date}/races.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Add race_timestamp and ingestion date

# COMMAND ----------

from pyspark.sql.functions import col, to_timestamp, concat, lit

# COMMAND ----------

races_with_timestamps_df = races_df.withColumn("race_timestamp", to_timestamp(concat(col("date"), lit(" "), col("time")), "yyyy-MM-dd HH:mm:ss"))

# COMMAND ----------

races_with_timestamps_df = add_ingestion_date(races_with_timestamps_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Select only the required columns

# COMMAND ----------

from pyspark.sql.functions import col
races_selected_df = races_with_timestamps_df.select(col("raceId"), col("year"), col("round"), col("circuitId"), col("name"), col("race_timestamp"), col("ingestion_date"))
display(races_selected_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 3 - Rename the columns as required and add data source column

# COMMAND ----------

from pyspark.sql.functions import lit

# COMMAND ----------

races_renamed_df = races_selected_df.withColumnRenamed("raceId", "race_id") \
.withColumnRenamed("year", "race_year") \
.withColumnRenamed("circuitId", "circuit_id") \
.withColumn("data_source", lit(v_data_source)) \
.withColumn("file_date", lit(v_file_date))

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 5 - Write data to data lake as parquet

# COMMAND ----------

# races_renamed_df.write.mode("overwrite").partitionBy("race_year").parquet(f"{processed_folder_path}/races")

# COMMAND ----------

races_renamed_df.write.mode("overwrite").partitionBy("race_year").format("delta").saveAsTable("f1_processed.races")

# COMMAND ----------

dbutils.notebook.exit("Success")