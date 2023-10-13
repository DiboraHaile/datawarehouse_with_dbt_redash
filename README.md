# datawarehouse_with_dbt_redash
A Data warehouse that is built with postgres database that uses airflow to ingest real time data into it. DBT is used as a transformation tool to organize sql queries and redash is used to visualize insights extracted from the data.

## Roadmap
- [x] Get data source
- [x] Write a parser in python
- [x] Ingest data to postgres
- [ ] Dockerize postgres database
- [ ] Dockerize redash
- [ ] Setup DBT
- [ ] Create DBT models
- [ ] Create visualizations on redash using the models
- [ ] Automate the ingestion
- [ ] Dockerize airflow
- [ ] Dockerize ingesting script
- [ ] Clean up the documentation


## The data source for this project 
The data taken for this project came from [Neuma](https://open-traffic.epfl.ch/) 
You can read further about the data [here](data/README.md)

## Data schema
Data is ingested to a postgres database with the name of traffic_stream_record
there are two tables in these database named trajectory and record. You can find the schemas of these two tables on [here](https://dbdiagram.io/d/traffic_stream_record-65253c0bffbf5169f066488a)