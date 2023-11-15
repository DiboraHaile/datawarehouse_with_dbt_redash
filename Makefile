setup:
# initialize airflow 
	make -C airflow/ init
# build the ingester image
	sudo docker build -t ingester:v1 -f ./src/Dockerfile src/
# build the dbt image
	sudo docker build -t dbt_image:v1 -f ./dbt_transformation/Dockerfile dbt_transformation/
# initialize redash 
	make -C redash/ init

start:
# start postgres container
	docker-compose -f postgres_db/docker-compose.yaml up
# start airflow container
	make -C airflow/ start
# start redash container
	make -C redash/ start

stop:
	make -C airflow/ stop
	make -C redash/ stop
	docker-compose -f postgres/docker-compose.yaml down 

