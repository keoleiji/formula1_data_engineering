-- Databricks notebook source
-- MAGIC %md
-- MAGIC Create Bronze Tables
-- MAGIC 1. drivers.json
-- MAGIC 2. results.json Bronze folder path - abfss://bronze@databricksucextdlbrazil.dfs.core.windows.net/

-- COMMAND ----------

drop table if exists formula1_dev.bronze.drivers;

create table if not exists formula1_dev.bronze.drivers
(
  driverId int,
  driverRef string,
  number int,
  code string,
  name struct<forename:string, surname:string>,
  dob date,
  nationality string,
  url string
)
using json
options (path "abfss://bronze@databricksucextdlbrazil.dfs.core.windows.net/drivers.json")

-- COMMAND ----------

drop table if exists formula1_dev.bronze.results;

create table if not exists formula1_dev.bronze.results
(
  resultId int,
  raceId int,
  driverId int,
  constructorId int,
  number int,
  grid int,
  position int,
  positionText string,
  positionOrder int,
  points int,
  laps int,
  time string,
  milliseconds int,
  fastestLap int,
  rank int,
  fastestLapTime string,
  fastestLapSpeed double,
  statusId string
)
using json
options (path "abfss://bronze@databricksucextdlbrazil.dfs.core.windows.net/results.json")

-- COMMAND ----------

