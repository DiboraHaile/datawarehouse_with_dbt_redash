## Starting the airflow container
### Steps
- Create an environment file ```.env``` in this directory
- The content inside should look like the following
  ```
    AIRFLOW_UID=501
    AIRFLOW_GID=0
    _PIP_ADDITIONAL_REQUIREMENTS=apache-airflow-providers-docker==2.1.0rc2
    ABSOLUTE_PATH_PROJ=enter the absolute path of your project
    DBT_LOC=location of your .dbt file

  ```
- Then initialize airflow metadata database
  ```
    make init
  ```
- Run the container using airflow start
  ```
    make start
  ```
- To stop the container use
  ```
    make stop
  ```