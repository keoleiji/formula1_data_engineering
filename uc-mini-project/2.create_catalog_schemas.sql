-- Databricks notebook source
-- MAGIC %md
-- MAGIC Create Catalogs and Schemas required for the project
-- MAGIC 1. Catalog - formula1dev (without managed location)
-- MAGIC 2. Schemas - bronze, silver and gold (with managed location)

-- COMMAND ----------

create catalog if not exists formula1_dev;

-- COMMAND ----------

use catalog formula1_dev;

-- COMMAND ----------

create schema if not exists bronze
managed location "abfss://bronze@databricksucextdlbrazil.dfs.core.windows.net/"

-- COMMAND ----------

create schema if not exists silver
managed location "abfss://silver@databricksucextdlbrazil.dfs.core.windows.net/"

-- COMMAND ----------

create schema if not exists gold
managed location "abfss://gold@databricksucextdlbrazil.dfs.core.windows.net/"

-- COMMAND ----------

show schemas

-- COMMAND ----------

