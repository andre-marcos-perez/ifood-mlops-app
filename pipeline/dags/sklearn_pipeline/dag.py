from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from sklearn_pipeline.tasks.train import train
from sklearn_pipeline.tasks.start import start
from sklearn_pipeline.tasks.finish import finish

dag = DAG(
    dag_id='sklearn-pipeline',
    description='Machine learning pipeline with scikit-learn engine',
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

train = PythonOperator(
    task_id='train',
    python_callable=train,
    op_kwargs=None,
    provide_context=True,
    dag=dag
)

finish = PythonOperator(
    task_id='finish',
    python_callable=finish,
    op_kwargs=None,
    provide_context=True,
    dag=dag
)

start >> train >> finish
