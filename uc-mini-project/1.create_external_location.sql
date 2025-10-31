-- Databricks notebook source
CREATE EXTERNAL LOCATION IF NOT EXISTS `databricksucextdl_bronze`
URL 'abfss://bronze@databricksucextdlbrazil.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL `databrickscourse-ext-storage-credential`)

-- COMMAND ----------

DESC EXTERNAL LOCATION databricksucextdl_bronze

-- COMMAND ----------

-- MAGIC %fs
-- MAGIC ls "abfss://bronze@databricksucextdlbrazil.dfs.core.windows.net/"

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `databricksucextdl_silver`
URL 'abfss://silver@databricksucextdlbrazil.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL `databrickscourse-ext-storage-credential`)

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `databricksucextdl_gold`
URL 'abfss://gold@databricksucextdlbrazil.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL `databrickscourse-ext-storage-credential`)