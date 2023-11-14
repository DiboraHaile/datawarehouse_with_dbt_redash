## Ingester
This folder contains scripts to ingest the neuma data to the postgres database. There is a docker file that will be used to build the image for the ingester.
- Create ```.env``` file 
  It should look something like this
  ```
    POSTGRES_HOST=pgdatabase
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_PORT=5432
    POSTGRES_DB=traffic_stream_record
  ```
### To run the ingester 
- Create custom network and run the postgres container on that network
- Build the image
  ```
    docker build -t ingester:v1 .
  ```
- Run the container
  ```
    docker run --network=network_name -it ingester:v1 bash 
  ```