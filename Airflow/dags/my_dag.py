from airflow import DAG

from datetime import datetime
from airflow.operators.dummy import DummyOperator

with DAG("my_dag", 
start_date=datetime(2022, 10, 9),
schedule_interval='@daily', 
catchup=False) as dag:
    task_a = DummyOperator(
        task_id="task_a"
    )