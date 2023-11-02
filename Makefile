setup:
# create a custom network
# docker create network custom-network
	make -C redash/ setup
	make -C airflow/ init

start:
	docker-compose up -d 
# run airflow container
	make -C airflow/ init
	make -C airflow/ start
# run postgres container
stop:

	make -C airflow/ stop