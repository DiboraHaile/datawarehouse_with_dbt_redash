# First-time build can take upto 10 mins.

FROM apache/airflow:2.7.2

ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update -qq && apt-get install python3-pip -qq
# git gcc g++ -qqq

USER airflow
# COPY requirements.txt .
RUN pip install psycopg2-binary pandas 

# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

# SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]
WORKDIR ${AIRFLOW_HOME}
# COPY ingester/ ingester/


# RUN chmod +x *.py
# EXPORT DOCKER_HOST=unix:///var/run/docker.sock
# CMD ["python3","data_ingester.py"]


