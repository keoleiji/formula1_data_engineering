# Databricks notebook source
# MAGIC %md
# MAGIC Upsert using merge

# COMMAND ----------

# MAGIC %sql 
# MAGIC create database if not exists f1_demo
# MAGIC location '/mnt/formula1dlbrazil/demo'

# COMMAND ----------

# MAGIC %md
# MAGIC 1. Update Delta Table
# MAGIC 2. Delete From Delta Table

# COMMAND ----------

results_df = spark.read \
.option("inferSchema", True) \
.json("/mnt/formula1dlbrazil/raw-bronze/2021-03-28/results.json")

# COMMAND ----------

results_df.write.format("delta").mode("overwrite").saveAsTable("f1_demo.results_managed")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.results_managed;

# COMMAND ----------

results_df.write.format("delta").mode("overwrite").save("/mnt/formula1dlbrazil/demo/results_external")

# COMMAND ----------

# MAGIC %sql
# MAGIC create table f1_demo.results_external
# MAGIC using delta
# MAGIC location '/mnt/formula1dlbrazil/demo/results_external'

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.results_external

# COMMAND ----------

results_external_df = spark.read.format("delta").load("/mnt/formula1dlbrazil/demo/results_external")

# COMMAND ----------

display(results_external_df)

# COMMAND ----------

results_df.write.format("delta").mode("overwrite").partitionBy("constructorId").saveAsTable("f1_demo.results_partition")

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW PARTITIONS f1_demo.results_partition

# COMMAND ----------

# MAGIC %md
# MAGIC 1. Update Delta Table
# MAGIC 2. Delete From Delta Table

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.results_managed;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE f1_demo.results_managed
# MAGIC   SET points = 11 - position
# MAGIC   WHERE position <= 10

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.results_managed;

# COMMAND ----------

from delta.tables import DeltaTable

deltaTable = DeltaTable.forPath(spark, "/mnt/formula1dlbrazil/demo/results_managed")

deltaTable.update("position <= 10", { "points": "21 - position" })

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.results_managed;

# COMMAND ----------

from delta.tables import DeltaTable

deltaTable = DeltaTable.forPath(spark, "/mnt/formula1dlbrazil/demo/results_managed")

deltaTable.delete("points = 0")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_demo.results_managed;

# COMMAND ----------

# MAGIC %md
# MAGIC Upsert using merge

# COMMAND ----------

drivers_day1_df = spark.read \
    .option("inferSchema", True) \
    .json("/mnt/formula1dlbrazil/raw-bronze/2021-03-28/drivers.json") \
    .filter("driverId <= 10") \
    .select("driverId", "dob", "name.forename", "name.surname")

# COMMAND ----------

display(drivers_day1_df)

# COMMAND ----------

drivers_day1_df.createOrReplaceTempView("drivers_day1")

# COMMAND ----------

from pyspark.sql.functions import upper

drivers_day2_df = spark.read \
    .option("inferSchema", True) \
    .json("/mnt/formula1dlbrazil/raw-bronze/2021-03-28/drivers.json") \
    .filter("driverId BETWEEN 6 AND 15") \
    .select("driverId", "dob", upper("name.forename").alias("forename"), upper("name.surname").alias("surname"))

# COMMAND ----------

drivers_day2_df.createOrReplaceTempView("drivers_day2")

# COMMAND ----------

display(drivers_day2_df)

# COMMAND ----------

from pyspark.sql.functions import upper

drivers_day3_df = spark.read \
.option("inferSchema", True) \
.json("/mnt/formula1dlbrazil/raw-bronze/2021-03-28/drivers.json") \
.filter("driverId BETWEEN 1 AND 5 OR driverId BETWEEN 16 AND 20") \
.select("driverId", "dob", upper("name.forename").alias("forename"), upper("name.surname").alias("surname"))

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS f1_demo.drivers_merge (
# MAGIC   driverId INT,
# MAGIC   dob DATE,
# MAGIC   forename STRING,
# MAGIC   surname STRING,
# MAGIC   createdDate DATE,
# MAGIC   updatedDate DATE
# MAGIC )
# MAGIC USING DELTA

# COMMAND ----------

# MAGIC %md
# MAGIC Day 1

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO f1_demo.drivers_merge tgt
# MAGIC USING drivers_day1 upd
# MAGIC ON tgt.driverId = upd.driverId
# MAGIC WHEN MATCHED THEN
# MAGIC   UPDATE SET
# MAGIC     tgt.dob = upd.dob,
# MAGIC     tgt.forename = upd.forename,
# MAGIC     tgt.surname = upd.surname,
# MAGIC     tgt.updatedDate = current_timestamp
# MAGIC WHEN NOT MATCHED
# MAGIC   THEN INSERT (driverId, dob, forename, surname, createdDate) VALUES (driverId, dob, forename, surname, current_timestamp)

# COMMAND ----------

# MAGIC %sql SELECT * FROM f1_demo.drivers_merge;

# COMMAND ----------

# MAGIC %md
# MAGIC Day 2

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO f1_demo.drivers_merge tgt
# MAGIC USING drivers_day2 upd
# MAGIC ON tgt.driverId = upd.driverId
# MAGIC WHEN MATCHED THEN
# MAGIC   UPDATE SET
# MAGIC     tgt.dob = upd.dob,
# MAGIC     tgt.forename = upd.forename,
# MAGIC     tgt.surname = upd.surname,
# MAGIC     tgt.updatedDate = current_timestamp
# MAGIC WHEN NOT MATCHED
# MAGIC   THEN INSERT (driverId, dob, forename, surname, createdDate) VALUES (driverId, dob, forename, surname, current_timestamp)

# COMMAND ----------

# MAGIC %sql SELECT * FROM f1_demo.drivers_merge;

# COMMAND ----------

# MAGIC %md
# MAGIC Day 3

# COMMAND ----------

from pyspark.sql.functions import current_timestamp
from delta.tables import DeltaTable

deltaTable = DeltaTable.forPath(spark, "/mnt/formula1dlbrazil/demo/drivers_merge")

deltaTable.alias("tgt").merge(
    drivers_day3_df.alias("upd"),
    "tgt.driverId = upd.driverId") \
        .whenMatchedUpdate(set = { "dob": "upd.dob", "forename": "upd.forename", "surname": "upd.surname", "updatedDate": "current_timestamp()"}) \
        .whenNotMatchedInsert(values = {
            "driverId": "upd.driverId",
            "dob": "upd.dob",
            "forename": "upd.forename",
            "surname": "upd.surname",
            "createdDate": "current_timestamp()",
        }
    ) \
    .execute()

# COMMAND ----------

# MAGIC %sql SELECT * FROM f1_demo.drivers_merge;