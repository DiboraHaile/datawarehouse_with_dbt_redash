from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from data_ingester import main
import os
from dotenv import load_dotenv


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
# Load environment variables from .env file
load_dotenv()
PG_HOST = os.getenv('POSTGRES_HOST')
PG_USER = os.getenv('POSTGRES_USER')
PG_PASSWORD = os.getenv('POSTGRES_PASSWORD')
PG_PORT = os.getenv('POSTGRES_PORT')
PG_DATABASE = os.getenv('POSTGRES_DB')
PATH = os.getenv('ABSOLUTE_PATH_PROJ')


def ingester_callable(**kwargs):
    op_kwargs=dict(
                user=PG_USER,
                password=PG_PASSWORD,
                host=PG_HOST,
                port=PG_PORT,
                db=PG_DATABASE,
                file_path=f"{PATH}/data/*.csv"
            )
    main(**op_kwargs)


default_args = {
    'owner': 'dibora',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 6),
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

print(f"hello {PG_HOST}")
# Using BashOperator to execute a bash command
with local_workflow:
    get_env_task = BashOperator(
            task_id="get_env",
            bash_command="echo $POSTGRES_HOST ",
        ),
    ingest_task = PythonOperator(
            task_id="ingest",
            python_callable=ingester_callable,

        )

get_env_task >> ingest_task
# task1 = DockerOperator(
#     task_id='task_1',
#     image='ingester-ingester:latest',
#     container_name="ingester-ingester-1",
#     network_mode="postgres_db_default",
#     command='python3 data_ingester.py',
#     docker_url='unix://var/run/docker.sock',
#     dag=dag,
# )
