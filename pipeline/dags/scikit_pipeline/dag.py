from datetime import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

dag = DAG(
    dag_id='scikit-pipeline',
    description='Machine learning pipeline with scikit-learn engine',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1)
)

train = DummyOperator(
    task_id='train',
    dag=dag
)

test = DummyOperator(
    task_id='test',
    dag=dag
)

train >> test
