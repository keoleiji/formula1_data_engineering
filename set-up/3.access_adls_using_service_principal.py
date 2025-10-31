# Databricks notebook source
# MAGIC %md
# MAGIC #### Access Azure Data Lake using Service Principal
# MAGIC
# MAGIC Steps to follow
# MAGIC 1. Register Azure AD Application / Service Principal
# MAGIC 2. Generate a secret / password for the application
# MAGIC 3. Set Spark Config with App/Client Id. Directory/ Tenant Id & Secret
# MAGIC 4. Assign Role 'Storage Blob Data Contributor' to the Data Lake.

# COMMAND ----------

client_id = dbutils.secrets.get(scope = "formula1-scope", key = "formula1dlbrazil-demo-client-id")
tenant_id = dbutils.secrets.get(scope = "formula1-scope", key = "formula1dlbrazil-demo-tenant-id")
client_secret = dbutils.secrets.get(scope = "formula1-scope", key = "formula1dlbrazil-demo-client-secret")

# COMMAND ----------

spark.conf.set("fs.azure.account.auth.type.formula1dlbrazil.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.formula1dlbrazil.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.formula1dlbrazil.dfs.core.windows.net", client_id)
spark.conf.set("fs.azure.account.oauth2.client.secret.formula1dlbrazil.dfs.core.windows.net", client_secret)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.formula1dlbrazil.dfs.core.windows.net", f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")

# COMMAND ----------

display(dbutils.fs.ls("abfss://demo@formula1dlbrazil.dfs.core.windows.net"))

# COMMAND ----------

spark.read.csv("abfss://demo@formula1dlbrazil.dfs.core.windows.net/circuits.csv").show()