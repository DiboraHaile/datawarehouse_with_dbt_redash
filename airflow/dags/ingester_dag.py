from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow import DAG
import os
from dotenv import load_dotenv
from docker.types import Mount
import logging

logging.getLogger().setLevel(logging.DEBUG)

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
# Load environment variables from .env file
load_dotenv()
PATH = os.getenv('ABSOLUTE_PATH_PROJ')


default_args = {
    'owner': 'dibora',
    'depends_on_past': False,
    'start_date': datetime(2023,11,13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

local_workflow = DAG(
    dag_id = 'local_ingestion_dag',
    default_args=default_args,
    description='This script ingests data to postgres db',
    schedule_interval=timedelta(days=1),
)


ingester_task = DockerOperator(
    task_id="ingest_data",
    api_version='1.37',
    docker_url='TCP://docker-socket-proxy:2375',
    image="ingester:v1",
    network_mode="airflow_default",
    tty=True,
    dag=local_workflow,
    mount_tmp_dir = False,
    mounts=[
        Mount(
            target='/src/data/', 
            source=f'{PATH}/data/', 
            type="bind"
            )], 
    command="bash -c 'python3 data_ingester.py'"
    )   

run_dbt_task = DockerOperator(
    task_id="update_dbt_model",
    api_version='1.37',
    docker_url='TCP://docker-socket-proxy:2375',
    image="dbt_image:v1",
    network_mode="airflow_default",
    tty=True,
    dag=local_workflow,
    mount_tmp_dir = False,
    mounts=[
        Mount(
            target='/usr/app/', 
            source=f'{PATH}/dbt_transformation/', 
            type="bind"
            ),
        Mount(
            target='/root/.dbt/',
            source=f'{PATH}/dbt_transformation/profiles.yml',
            type="bind"
        )
        ],      
        command="bash -c 'dbt build && dbt run'",
        # command="bash -c 'dbt docs generate'"
        
        )
logging.info(f"DAG and DockerOperator configured successfully for {local_workflow.dag_id}")

ingester_task >> run_dbt_task
