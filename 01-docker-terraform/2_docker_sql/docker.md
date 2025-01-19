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
```

----
----
----
----
----
----
----
----

# Running Postgres and pgAdmin together

## Create a network (both containers need visibility to each other)
```bash
docker network create pg-network
```

## Run Postgres (change the path)
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ./ny_taxi_postgres_data:/var/lib/postgresql/data:rw \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```

## Run pgAdmin
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

## Error: Container already in use
If you encounter this error, delete the existing container before re-creating it:
```bash
docker rm pg-database
docker rm pgadmin-2
```

## Delete all stopped containers
```bash
docker container prune
```

---

# Convert the notebook to script
```bash
jupyter nbconvert --to=script upload-data.ipynb
```

## Docker-compose for simplification
Instead of running commands in two terminals, use Docker-compose.

## Example ingestion script:
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}
```

## Build Docker image
```bash
docker build -t taxi_ingest:v001 .
```

## Check exit status
- `0` indicates success.
- Non-zero values indicate failure.
```bash
echo $?
```

## Python library for accessing Postgres
`psycopg2` is required and needs to be installed.

## Run the script with Docker Compose
```bash
docker-compose up -d
docker-compose down
```

## Run the ingestion script with Docker
Ensure the container is on the same network as Postgres/pgAdmin.
```bash
docker run -it \
  --network=2_docker_sql_default \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

## Verify Docker network
List all networks:
```bash
docker network ls
```
Inspect a specific network:
```bash
docker network inspect 2_docker_sql_default
```

![Texto alternativo](../../images/personal/port_forwarding.png "Título opcional")

---

# Serve files with Python
Open a server on port 8000 to serve all files in the current directory:
```bash
python -m http.server
```

## Check network configuration
```bash
ipconfig  # On Windows
ifconfig  # On Linux/Mac
```
---

## Docker runs
```bash
docker run hello-world  
docker run -it ubuntu bash 
docker run -it python:3.9
docker run -it --entrypoint=bash python:3.9
```

## Dockerfile example for executing python file with pandas
```bash
FROM python:3.9

RUN pip install pandas

WORKDIR /app

COPY pipeline.py pipeline.py

ENTRYPOINT ["python","pipeline.py"]
```

Building docker image and running it
```bash
docker build -t test:pandas .
docker run -it test:pandas 2022-01-01
```
