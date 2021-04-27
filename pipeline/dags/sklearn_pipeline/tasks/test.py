import json
import logging

from sklearn import *

from shared.database import Database
from shared.registry import Registry


def test(**context):

    logging.basicConfig(level=logging.INFO)

    database = Database()
    registry = Registry()

    try:

        target_col = context['dag_run'].conf.get('target_col')
        project_id = context['dag_run'].conf.get('project_id')
        experiment_id = context['dag_run'].conf.get('experiment_id')

        model = registry.get_model(path=f"{project_id}-{experiment_id}", key='model')
        dataset = registry.get_dataset(path=f"{project_id}-{experiment_id}", key='test')
        metrics = registry.get_model(path=f"{project_id}-{experiment_id}", key='metrics')

        dataset.drop(dataset.columns[0], axis=1, inplace=True)
        calculated_metrics = dict()
        for metric, func in metrics.items():
            calculated_metrics[metric] = func(dataset[f"{target_col}"], model.predict(dataset.drop(f"{target_col}", axis=1)))

    except Exception as exc:

        logging.error(msg=exc)
        status = 'test-failed'
        calculated_metrics = {}
        query = f"UPDATE experiment SET status = '{status}', metrics = '{json.dumps(calculated_metrics)}' WHERE id = {experiment_id}"
        database.write(query=query)
        raise exc

    else:

        status = 'tested'
        query = f"UPDATE experiment SET status = '{status}', metrics = '{json.dumps(calculated_metrics)}' WHERE id = {experiment_id}"
        database.write(query=query)
        return True
