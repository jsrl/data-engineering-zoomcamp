#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types


# In[2]:


spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()


# In[3]:


spark.version


# In[15]:


get_ipython().system('wget -P /home/jsrl/notebooks/data/raw/fhv/ https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz')


# In[4]:


df = pd.read_csv('/home/jsrl/notebooks/data/raw/fhv/fhv_tripdata_2019-10.csv.gz', nrows=400)


# In[5]:


spark.createDataFrame(df).schema


# In[9]:


schema = types.StructType([ \
    types.StructField('dispatching_base_num', types.StringType(), True), \
    types.StructField('pickup_datetime', types.TimestampType(), True), \
    types.StructField('dropOff_datetime', types.TimestampType(), True), \
    types.StructField('PUlocationID', types.LongType(), True), \
    types.StructField('DOlocationID', types.LongType(), True), \
    types.StructField('SR_Flag', types.DoubleType(), True), \
    types.StructField('Affiliated_base_number', types.StringType(), True)])


# In[10]:


fhv_spark_df = spark.read \
    .option("header", True) \
    .schema(schema) \
    .csv('/home/jsrl/notebooks/data/raw/fhv/fhv_tripdata_2019-10.csv.gz')


# In[11]:


fhv_spark_df.repartition(6).write.parquet('/home/jsrl/notebooks/data/pq/hw5/')


# In[12]:


#Question 2
get_ipython().system('ls -lh /home/jsrl/notebooks/data/pq/hw5/')


# In[13]:


fhv_parquet_df = spark.read.parquet('/home/jsrl/notebooks/data/pq/hw5/')


# In[14]:


fhv_parquet_df.createOrReplaceTempView('homework5')


# In[16]:


#Question 3
spark.sql("""
SELECT COUNT(*)
FROM homework5
WHERE cast(pickup_datetime as date) = '2019-10-15'
""").show()


# In[18]:


#Question 4
spark.sql("""
SELECT pickup_datetime
,dropOff_datetime
,(unix_timestamp(dropOff_datetime) - unix_timestamp(pickup_datetime)) /3600 as hours
FROM homework5
ORDER BY hours desc
""").show()


# In[19]:


lookup_spark_df = spark.read.parquet('/home/jsrl/notebooks/zones/')


# In[21]:


lookup_spark_df.createOrReplaceTempView('lookup')


# In[23]:


spark.sql("""
SELECT count(*) as cnt
,PUlocationID
,Borough
,zone
FROM homework5 inner join lookup
on PUlocationID = LocationID
GROUP BY PUlocationID, Borough, zone
ORDER BY cnt asc
""").show()

