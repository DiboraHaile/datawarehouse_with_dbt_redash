# First-time build can take upto 10 mins.

FROM ubuntu:latest

# ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update -qq && apt-get install python3-pip -qq
# git gcc g++ -qqq

# COPY requirements.txt .
RUN pip install psycopg2-binary pandas

# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]
WORKDIR /src
COPY data data
COPY . .

RUN chmod +x /src
CMD ["python3","data_ingester.py"]


