setup:
	docker-compose up -d 
# # run redash container
# 	make -C redash/ setup
# 	make -C redash/ start

# run airflow container
	# make -C airflow/ init
	# make -C airflow/ start
# run postgres container
stop:
	make -C redash/ stop
	make -C airflow/ stop

# redash:
# 	docker-compose -f redash/docker-compose-redash.yml up -d

# pg:
# 	docker-compose -f redash/docker-compose-redash.yml stop