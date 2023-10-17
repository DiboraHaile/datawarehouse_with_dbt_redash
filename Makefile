setup:
# create a custom network
# docker create network custom-network
	make -C redash/ setup
	make -C airflow/ init

start:
	docker-compose up -d 
	make -C redash/ start
	make -C airflow/ start


stop:
	docker-compose down
	make -C airflow/ stop
	make -C redash/ stop

