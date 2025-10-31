# Databricks notebook source
# MAGIC %md
# MAGIC ### Ingest results.json file

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

# MAGIC %md
# MAGIC ##### Step 1 - Read the JSON file using the spark dataframe reader

# COMMAND ----------

# constructor_schema = "constructorId INT, constructorRef STRING, name STRING, nationality STRING, url STRING"
# race_schema = "raceId INT, year INT, round INT, circuitId INT, name STRING, date DATE, time STRING, url STRING"
# circuit_schema = "circuitId INT, circuitRef STRING, name STRING, location STRING, country STRING, lat DOUBLE, lng DOUBLE, alt INT, url STRING"
# drivers_schema = "driverId INT, driverRef STRING, number INT, code STRING, name STRING, dob DATE, nationality STRING, url STRING"
results_schema = "resultId INT, raceId INT, driverId INT, constructorId INT, number INT, grid INT, position INT, positionText STRING, positionOrder INT, points DOUBLE, laps INT, time STRING, milliseconds INT, fastestLap INT, rank INT, fastestLapTime STRING, fastestLapSpeed STRING, statusId INT"

# COMMAND ----------

results_df = spark.read \
.schema(results_schema) \
.json(f"{raw_folder_path}/{v_file_date}/results.json")

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 2 - Drop unwanted column from the dataframe

# COMMAND ----------

from pyspark.sql.functions import col

# COMMAND ----------

results_dropped_df = results_df.drop('statusId')

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 3 - Rename columns and add ingestion date

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

# COMMAND ----------

results_final_df = results_dropped_df.withColumnRenamed('resultId', 'result_id') \
        .withColumnRenamed('raceId', 'race_id') \
        .withColumnRenamed('driverId', 'driver_id') \
        .withColumnRenamed('constructorId', 'constructor_id') \
        .withColumnRenamed('positionText', 'position_text') \
        .withColumnRenamed('positionOrder', 'position_order') \
        .withColumnRenamed('fastestLap', 'fastest_lap') \
        .withColumnRenamed('fastestLapTime', 'fastest_lap_time') \
        .withColumnRenamed('fastestLapSpeed', 'fastest_lap_speed') \
        .withColumn("data_source", lit(v_data_source)) \
        .withColumn("file_date", lit(v_file_date))

# COMMAND ----------

results_final_df = add_ingestion_date(results_final_df)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- DROP TABLE f1_processed.results;

# COMMAND ----------

results_deduped_df = results_final_df.dropDuplicates(['race_id', 'driver_id'])

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Step 4 - Write to output to processed container in parquet format

# COMMAND ----------

# results_final_df.write.mode('overwrite').parquet(f'{processed_folder_path}/results')

# COMMAND ----------

# results_final_df.write.mode("overwrite").partitionBy("race_id").parquet(f"{processed_folder_path}/results")

# COMMAND ----------

# MAGIC %md
# MAGIC Method 1

# COMMAND ----------

# for race_id_list in results_final_df.select("race_id").distinct().collect():
#     if (spark._jsparkSession.catalog().tableExists("f1_processed.results")):
#         spark.sql(f"ALTER TABLE f1_processed.results DROP IF EXISTS PARTITION (race_id={race_id_list.race_id})")

# COMMAND ----------

# results_final_df.write.mode("append").partitionBy("race_id").format("parquet").saveAsTable("f1_processed.results")

# COMMAND ----------

# MAGIC %md
# MAGIC Method 2

# COMMAND ----------

# MAGIC %sql
# MAGIC -- drop table f1_processed.results;

# COMMAND ----------

# spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

# COMMAND ----------

# results_final_df = results_final_df.select("result_id", "driver_id", "constructor_id", "number", "grid", "position", "position_text", "position_order", "points", "laps", "time", "milliseconds", "fastest_lap", "rank", "fastest_lap_time", "fastest_lap_speed", "data_source", "file_date", "ingestion_date", "race_id")


# COMMAND ----------

# if (spark._jsparkSession.catalog().tableExists("f1_processed.results")):
#     results_final_df.write.mode("overwrite").insertInto("f1_processed.results")
# else:
#     results_final_df.write.mode("overwrite").partitionBy("race_id").format("parquet").saveAsTable("f1_processed.results")

# COMMAND ----------

# MAGIC %md
# MAGIC Method 3

# COMMAND ----------

# overwrite_partition(results_final_df, "f1_processed", "results", "race_id")

# COMMAND ----------

merge_condition = "tgt.result_id = src.result_id AND tgt.race_id = src.race_id"
merge_delta_data(results_deduped_df, 'f1_processed', 'results', processed_folder_path, merge_condition, 'race_id')

# COMMAND ----------

dbutils.notebook.exit("Success")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT race_id, driver_id, COUNT(1)
# MAGIC FROM f1_processed.results
# MAGIC GROUP BY race_id, driver_id
# MAGIC ORDER BY race_id DESC