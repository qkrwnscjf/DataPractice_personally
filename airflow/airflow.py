from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 7),
    'retries': 1
}

dag = DAG(
    'stock_pipeline',
    default_args=default_args,
    schedule_interval='@hourly'
)

fetch_stock_task = BashOperator(
    task_id='fetch_stock',
    bash_command='python /opt/airflow/dags/kafka_producer.py',
    dag=dag
)

fetch_stock_task
