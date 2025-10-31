# Databricks notebook source
# MAGIC %run "../includes/configuration"

# COMMAND ----------

# MAGIC %run "../includes/common_functions"

# COMMAND ----------

dbutils.widgets.text("p_file_date", "2021-03-21")
v_file_date = dbutils.widgets.get("p_file_date")

# COMMAND ----------

constructors = spark.read.format("delta").load(f"{processed_folder_path}/constructors") \
    .withColumnRenamed("name", "team")

# COMMAND ----------

circuits = spark.read.format("delta").load(f"{processed_folder_path}/circuits") \
    .withColumnRenamed("location", "circuit_location")

# COMMAND ----------

races = spark.read.format("delta").load(f"{processed_folder_path}/races") \
    .withColumnRenamed("name", "race_name") \
    .withColumnRenamed("race_timestamp", "race_date")

# COMMAND ----------

drivers = spark.read.format("delta").load(f"{processed_folder_path}/drivers") \
    .withColumnRenamed("number", "driver_number") \
    .withColumnRenamed("name", "driver_name") \
    .withColumnRenamed("nationality", "driver_nationality")

# COMMAND ----------

results = spark.read.format("delta").load(f"{processed_folder_path}/results") \
    .filter(f"file_date = '{v_file_date}'") \
    .withColumnRenamed("time", "race_time") \
    .withColumnRenamed("race_id", "result_race_id") \
    .withColumnRenamed("file_date", "result_file_date")

# COMMAND ----------

races_circuits = races.join(circuits, races.circuit_id == circuits.circuit_id, "inner") \
  .select(races.race_id, races.race_year, races.race_name, races.race_date, circuits.circuit_location)

# COMMAND ----------

race_results = results.join(races_circuits, results.result_race_id == races_circuits.race_id) \
    .join(drivers, results.driver_id == drivers.driver_id) \
    .join(constructors, results.constructor_id == constructors.constructor_id)

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

# COMMAND ----------

final_race_results = race_results.select("race_id", "race_year", "race_name", "race_date", "circuit_location", "driver_name", "driver_number", "driver_nationality", "team", "grid", "fastest_lap", "race_time", "points", "position", "result_file_date") \
    .withColumn("created_date", current_timestamp()) \
    .withColumnRenamed("result_file_date", "file_date")

# COMMAND ----------

from pyspark.sql.functions import desc

# COMMAND ----------

# final_race_results.write.mode("overwrite").parquet(f"{presentation_folder_path}/race_results")

# COMMAND ----------

# final_race_results.write.mode("overwrite").format("parquet").saveAsTable("f1_presentation.race_results")

# COMMAND ----------

# overwrite_partition(final_race_results, "f1_presentation", "race_results", "race_id")

# COMMAND ----------

merge_condition = "tgt.race_id = src.race_id and tgt.driver_name = src.driver_name"
merge_delta_data(final_race_results, 'f1_presentation', 'race_results', presentation_folder_path, merge_condition, 'race_id')