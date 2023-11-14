
FROM ubuntu

RUN apt-get update -qq && apt-get install python3-pip -qq

RUN pip install python-dotenv pandas psycopg2-binary
WORKDIR /src/
COPY . .



