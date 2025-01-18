## Docker Overview

Delivers software in packages called **containers**.  
Key feature: **Isolation**.  

### Docker Image
A snapshot of the container.

#### Benefits:
- **Reproducibility**
- Local experiments
- Integration tests (CI/CD: Github Actions, Jenkins, etc.)
- Running pipelines on the cloud (AWS Batch, Kubernetes jobs)
- Spark
- Serverless (AWS Lambda, Google Functions)

---

### Common Docker Commands

#### Running a simple container:
```bash
docker run hello-world
docker run -it ubuntu bash # -it: interactive terminal, 'ubuntu' is the image, 'bash' is the command

docker run -it python:3.9 # Tag specifies a specific version
docker run -it --entrypoint=bash python:3.9 # Overrides the entrypoint to run bash

pip install pandas
python
# Then you can run:
import pandas
```

### Dockerfile Example
```bash
FROM python:3.9.1

RUN apt-get update && apt-get install -y wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]
```

```bash
docker build -t test:pandas . # Builds an image named 'test' with the tag 'pandas'
docker run -it test:pandas    # Runs the built image interactively
```

----
----
----
----
----
----
----
----

# Ingesting NY Taxi Data to Postgres

## Docker-compose: A Way of Running Multiple Composer Images

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ./ny_taxi_postgres_data:/var/lib/postgresql/data:rw \
  -p 5432:5432 \
  postgres:13
```

## Using pgcli: Postgres Client for Python

```bash
pgcli -h localhost -U root -d ny_taxi
\dt
```

## Python Code for Ingesting Data

### Importing Libraries
```python
import pandas as pd
from sqlalchemy import create_engine
from time import time
```

### Checking Pandas Version
```python
print(pd.__version__)
```

### Reading Data
```python
df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)
```

### Converting Dates from String to Datetime
```python
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
```

### Creating Connection to Postgres
```python
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()
```

### Printing Table Schema
```python
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
```

### Creating Table with 0 Rows
```python
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
```

### Inserting Data into the Table
```python
%time df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
```

## Defining DataFrame Iterator for Chunked Ingestion

### Creating an Iterator
```python
df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)
```

### Creating Table with 0 Rows
```python
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
```

### Inserting Data Chunk by Chunk
```python
while True: 
    t_start = time()

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

    t_end = time()

    print('inserted another chunk, took %.3f second' % (t_end - t_start))

