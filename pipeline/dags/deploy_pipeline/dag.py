from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from deploy_pipeline.tasks.start import start
from deploy_pipeline.tasks.deploy import deploy
from deploy_pipeline.tasks.finish import finish

dag = DAG(
    dag_id='deploy-pipeline',
    description='Machine learning model deployment pipeline',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1)
)

start = PythonOperator(
    task_id='start',
    python_callable=start,
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

finish = PythonOperator(
    task_id='finish',
    python_callable=finish,
    op_kwargs=None,
    provide_context=True,
    dag=dag
)

start >> deploy >> finish
