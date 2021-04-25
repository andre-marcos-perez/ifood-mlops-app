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

        project_id = context['dag_run'].conf.get('project_id')
        experiment_id = context['dag_run'].conf.get('experiment_id')

        model = registry.get_model(path=f"{project_id}-{experiment_id}", key='model')
        target = registry.get_dataset(path=f"{project_id}-{experiment_id}", key='target')
        features = registry.get_dataset(path=f"{project_id}-{experiment_id}", key='features')

        print(model)
        print(type(model))
        print(model.__dict__)

        print(target.head())
        print(features.head())

        model.fit(features, target)

    except Exception as exc:
        logging.error(msg=exc)
        status = 'train-failed'
        hyper_params = {}
    else:
        status = 'trained'
        hyper_params = model.get_params()
        registry.put_model(path=f"{project_id}-{experiment_id}", key='model', model=model)
    finally:
        query = f"UPDATE experiment SET status = '{status}', hyperparams = '{json.dumps(hyper_params)}' WHERE id = {experiment_id}"
        database.write(query=query)

    return True if status == 'trained' else False
