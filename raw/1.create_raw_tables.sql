-- Databricks notebook source
CREATE DATABASE IF NOT EXISTS f1_raw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### Create circuits table

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.circuits;
CREATE TABLE IF NOT EXISTS f1_raw.circuits (
  circuitId INT,
  circuitRef STRING,
  name STRING,
  location STRING,
  country STRING,
  lat DOUBLE,
  lng DOUBLE,
  alt INT
)
USING csv
OPTIONS (path "/mnt/formula1dlbrazil/raw-bronze/circuits.csv", header true)

-- COMMAND ----------

SELECT * FROM f1_raw.circuits

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### Create races table

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.races;
CREATE TABLE IF NOT EXISTS f1_raw.races (
  raceId INT,
  year INT,
  round INT,
  circuitId INT,
  name STRING,
  date DATE,
  time STRING
) USING csv
OPTIONS (
  path "/mnt/formula1dlbrazil/raw-bronze/races.csv",
  header true
)

-- COMMAND ----------

SELECT * FROM f1_raw.races

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### Create constructor table

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.constructors;
CREATE TABLE IF NOT EXISTS f1_raw.constructors (
  constructorId INT,
  constructorRef STRING,
  name STRING,
  nationality STRING
) USING json
OPTIONS (
  path "/mnt/formula1dlbrazil/raw-bronze/constructors.json",
  header true
)

-- COMMAND ----------

SELECT * FROM f1_raw.constructors

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### Create drivers table

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.drivers;
CREATE TABLE IF NOT EXISTS f1_raw.drivers (
  driverId INT,
  driverRef STRING,
  number INT,
  code STRING,
  name STRUCT<forename: STRING, surname: STRING>,
  dob DATE,
  nationality STRING
) USING json
OPTIONS (
  path "/mnt/formula1dlbrazil/raw-bronze/drivers.json",
  header true
)

-- COMMAND ----------

SELECT * FROM f1_raw.drivers

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.results;
CREATE TABLE IF NOT EXISTS f1_raw.results (
  resultId INT,
  raceId INT,
  driverId INT,
  constructorId INT,
  number INT,
  grid INT,
  position INT,
  positionText STRING,
  positionOrder INT,
  points INT,
  laps INT,
  time STRING,
  milliseconds INT,
  fastestLap INT,
  rank INT,
  fastestLapTime STRING,
  fastestLapSpeed FLOAT,
  statusId STRING
) USING json
OPTIONS (
  path "/mnt/formula1dlbrazil/raw-bronze/results.json",
  header true
)

-- COMMAND ----------

SELECT * FROM f1_raw.results

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### Create pit stops file

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.pit_stops;
CREATE TABLE IF NOT EXISTS f1_raw.pit_stops (
  driverId INT,
  duration STRING,
  lap INT,
  milliseconds INT,
  raceId INT,
  stop INT,
  time STRING
) USING json
OPTIONS (
  path "/mnt/formula1dlbrazil/raw-bronze/pit_stops.json",
  multiLine true
)

-- COMMAND ----------

SELECT * FROM f1_raw.pit_stops

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### Create lap times table

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.lap_times;
CREATE TABLE IF NOT EXISTS f1_raw.lap_times (
  driverId INT,
  lap INT,
  position INT,
  time STRING,
  raceId INT,
  milliseconds INT
) USING csv
OPTIONS (
  path "/mnt/formula1dlbrazil/raw-bronze/lap_times",
  header true
)

-- COMMAND ----------

SELECT * FROM f1_raw.lap_times

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### Create qualifying table

-- COMMAND ----------

DROP TABLE IF EXISTS f1_raw.qualifying;
CREATE TABLE IF NOT EXISTS f1_raw.qualifying (
  position INT,
  driverId INT,
  constructorId INT,
  number INT,
  q1 STRING,
  q2 STRING,
  q3 STRING,
  raceId INT
) USING json
OPTIONS (
  path "/mnt/formula1dlbrazil/raw-bronze/qualifying",
  multiLine true
)

-- COMMAND ----------

SELECT * FROM f1_raw.qualifying

-- COMMAND ----------

DESC EXTENDED f1_raw.qualifying;

-- COMMAND ----------

