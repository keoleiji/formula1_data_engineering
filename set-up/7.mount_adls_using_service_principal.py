# Databricks notebook source
# MAGIC %md
# MAGIC #### Mount Azure Data Lake using Service Principal
# MAGIC
# MAGIC ##### Steps to follow
# MAGIC 1. Get client_id, tenant_id and client_secret frrom key vault
# MAGIC 2. Set Spark Config with App/ Client Id, Directory/ Tenant Id & Secret
# MAGIC 3. Call file system utility mount to mount the storage
# MAGIC 4. Explore other file system utilities related to mount (list all mounts, unmount)

# COMMAND ----------

client_id = dbutils.secrets.get(scope = "formula1-scope", key = "formula1dlbrazil-demo-client-id")
tenant_id = dbutils.secrets.get(scope = "formula1-scope", key = "formula1dlbrazil-demo-tenant-id")
client_secret = dbutils.secrets.get(scope = "formula1-scope", key = "formula1dlbrazil-demo-client-secret")

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": client_id,
          "fs.azure.account.oauth2.client.secret": client_secret,
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"}

# COMMAND ----------

dbutils.fs.mount(
  source = "abfss://demo@formula1dlbrazil.dfs.core.windows.net/",
  mount_point = "/mnt/formula1dlbrazil/demo",
  extra_configs = configs)

# COMMAND ----------

display(dbutils.fs.ls("/mnt/formula1dlbrazil/demo"))

# COMMAND ----------

display(spark.read.csv("/mnt/formula1dlbrazil/demo/circuits.csv"))

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

dbutils.fs.unmount("/mnt/formula1dlbrazil/demo")
display(dbutils.fs.mounts())