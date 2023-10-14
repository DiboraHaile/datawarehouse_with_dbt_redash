from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'dibora',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ingest_data',
    default_args=default_args,
    description='This script ingests data to postgres db',
    schedule_interval=timedelta(days=1),
)


# Using BashOperator to execute a bash command
bash_task = BashOperator(
    task_id='bash_task_to_run_ingester',
    bash_command='python3 data_ingester.py --file_path="../data/20181029_d8_0800_0830.csv"',
    dag=dag,
)

