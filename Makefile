setup:
# create a custom network
# docker create network custom-network
	make -C airflow/ init

start:
	make -C airflow/ start
	docker-compose -f dbt_transformation/docker-compose.yaml up
	docker-compose -f postgres_db/docker-compose.yaml up

# run airflow container

# run postgres container
stop:
	make -C airflow/ stop
	docker-compose down -f postgres/docker-compose.yaml 

