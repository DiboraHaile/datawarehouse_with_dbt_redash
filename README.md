# datawarehouse_with_dbt_redash
A Data warehouse that is built with postgres database that uses airflow to ingest real time data into it. DBT is used as a transformation tool to organize sql queries and redash is used to visualize insights extracted from the data.

## Roadmap
- [ ] Get data source
- [ ] Write a parser in python
- [ ] setup airflow docker container
- [ ] Create a scheduled dag
- [ ] Create a MYSQL/SQL docker container
- [ ] Write a python script that ingests the parsed data to the database
- [ ] Make the two containers communicate

## The data source for this project 
The data taken for this project came from [Neuma](https://open-traffic.epfl.ch/) 
You can read further about the data [here](data/README.md)
