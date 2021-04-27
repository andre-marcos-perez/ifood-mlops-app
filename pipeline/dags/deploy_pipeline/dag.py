from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from deploy_pipeline.tasks.setup import setup
from deploy_pipeline.tasks.deploy import deploy

dag = DAG(
    dag_id='deploy-pipeline',
    description='Machine learning model deployment pipeline',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1)
)

setup = PythonOperator(
    task_id='setup',
    python_callable=setup,
    op_kwargs=None,
    provide_context=True,
    dag=dag
)

deploy = PythonOperator(
    task_id='deploy',
    python_callable=deploy,
    op_kwargs=None,
    provide_context=False,
    dag=dag
)

setup >> deploy
