import json
import logging

from sklearn import *

from shared.database import Database
from shared.registry import Registry


def train(**context):

    logging.basicConfig(level=logging.INFO)

    database = Database()
    registry = Registry()

    try:

        target_col = context['dag_run'].conf.get('target_col')
        project_id = context['dag_run'].conf.get('project_id')
        experiment_id = context['dag_run'].conf.get('experiment_id')

        model = registry.get_model(path=f"{project_id}-{experiment_id}", key='model')
        dataset = registry.get_dataset(path=f"{project_id}-{experiment_id}", key='train')

        model.fit(dataset.drop(f"{target_col}", axis=1), dataset[f"{target_col}"])
        registry.put_model(path=f"{project_id}-{experiment_id}", key='model', model=model)

    except Exception as exc:

        logging.error(msg=exc)
        status = 'train-failed'
        hyper_params = {}
        query = f"UPDATE experiment SET status = '{status}', hyperparams = '{json.dumps(hyper_params)}' WHERE id = {experiment_id}"
        database.write(query=query)
        raise exc

    else:

        status = 'trained'
        hyper_params = model.get_params()
        registry.put_model(path=f"{project_id}-{experiment_id}", key='model', model=model)
        query = f"UPDATE experiment SET status = '{status}', hyperparams = '{json.dumps(hyper_params)}' WHERE id = {experiment_id}"
        database.write(query=query)
        return True
