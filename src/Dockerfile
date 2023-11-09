
FROM ubuntu

RUN apt-get update -qq && apt-get install python3-pip -qq
# git gcc g++ -qqq

# COPY requirements.txt .
RUN pip install python-dotenv pandas psycopg2-binary
WORKDIR /src/
COPY . .


# RUN chmod +x *.py
# EXPORT DOCKER_HOST=unix:///var/run/docker.sock
# CMD ["python3","data_ingester.py"]


