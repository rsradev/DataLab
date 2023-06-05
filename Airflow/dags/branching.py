from airflow.models import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator

import yaml
from datetime import datetime

def _check_accuracy():
    accuracy = 1.16
    if accuracy > 1.15:
        return ['accurate', 'top_accurate']
    return 'inaccurate'
    

default_args = {
    'start_date': datetime(2022, 10, 30)
}


with DAG('ml_dag',
    schedule_interval='@once',  
    default_args = default_args,
    catchup=False) as dag:
    
    training_ml = DummyOperator(task_id="training_ml")
    
    check_accuracy = BranchPythonOperator(
        task_id="check_accuracy",
        python_callable=_check_accuracy
    )

    accurate = DummyOperator(task_id="accurate")
    
    inaccurate = DummyOperator(task_id="inaccurate")

    top_accurate = DummyOperator(task_id="top_accurate")

    publish_ml = DummyOperator(task_id="publish_ml", 
                            trigger_rule="none_failed_or_skipped")


    training_ml >> check_accuracy >> [accurate, inaccurate, top_accurate] >> publish_ml