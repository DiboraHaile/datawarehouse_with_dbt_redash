setup:
	docker-compose up -d 
# run airflow container
	make -C airflow/ init
	make -C airflow/ start
# run postgres container
stop:
	make -C airflow/ stop
	docker-compose down

