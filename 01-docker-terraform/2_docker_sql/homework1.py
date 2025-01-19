#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
pd.__version__


# In[5]:


get_ipython().system('wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz')
get_ipython().system('gunzip green_tripdata_2019-10.csv.gz')
get_ipython().system('wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv')


# In[6]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()


# In[7]:


green_df = pd.read_csv('green_tripdata_2019-10.csv', nrows=10)


# In[8]:


print(pd.io.sql.get_schema(green_df, name='green_tripdata', con=engine))


# In[11]:


# Insert green taxi data in chunks
from time import time

df_iter = pd.read_csv('green_tripdata_2019-10.csv', iterator=True, chunksize=100000)
while True: 
    t_start = time()

    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    
    df.to_sql(name='green_tripdata', con=engine, if_exists='append')

    t_end = time()

    print('inserted another chunk, took %.3f second' % (t_end - t_start))


# In[12]:


taxi_zone_df = pd.read_csv('taxi_zone_lookup.csv')


# In[13]:


taxi_zone_df.to_sql(name='taxi_zones', con=engine, if_exists='replace')

