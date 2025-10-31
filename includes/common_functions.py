# Databricks notebook source
from pyspark.sql.functions import current_timestamp, lit

def add_ingestion_date(input_df):
    output_df = input_df.withColumn('ingestion_date', current_timestamp())
    return output_df

# COMMAND ----------

def re_arrange_partition_column(input_df, partition_col):
    cols = []
    for col in input_df.schema.names:
        if col != partition_col:
            cols.append(col)
    cols.append(partition_col)
    output_df = input_df.select(cols)
    return output_df

# COMMAND ----------

def overwrite_partition(input_df, db_name, table_name, partition_col):
    output_df = re_arrange_partition_column(input_df, partition_col)

    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

    if (spark._jsparkSession.catalog().tableExists(f"{db_name}.{table_name}")):
        output_df.write.mode("overwrite").insertInto(f"{db_name}.{table_name}")
    else:
        output_df.write.mode("overwrite").partitionBy(partition_col).format("parquet").saveAsTable(f"{db_name}.{table_name}")

# COMMAND ----------

def df_column_to_list(input_df, column_name):
    df_row_list = input_df.select(column_name) \
                .distinct() \
                .collect()
    df_row_list = [row[column_name] for row in df_row_list]
    return df_row_list

# COMMAND ----------

def merge_delta_data(input_df, db_name, table_name, folder_path, merge_condition, partition_col):
    spark.conf.set("spark.sql.legacy.allowCreatingManagedTableUsingNonemptyLocation", "true")
    from delta.tables import DeltaTable
    if (spark._jsparkSession.catalog().tableExists(f"{db_name}.{table_name}")):
        deltaTable = DeltaTable.forPath(spark, f"{folder_path}/{table_name}")
        deltaTable.alias("tgt").merge(
            input_df.alias("src"),
            merge_condition
        ) \
        .whenMatchedUpdateAll() \
        .whenNotMatchedInsertAll() \
        .execute()
    else:
        input_df.write.mode("overwrite").partitionBy(partition_col).format("delta").saveAsTable(f"{db_name}.{table_name}")