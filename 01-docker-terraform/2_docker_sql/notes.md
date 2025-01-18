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


