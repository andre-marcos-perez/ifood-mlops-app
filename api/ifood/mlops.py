import pandas as pd

from api.database import Database
from api.pipeline import Pipeline
from api.registry import Registry


def create_project(name: str) -> int:
    query = f"INSERT INTO project (name) VALUES ('{name}')"
    database = Database()
    return database.write(query=query)


def get_projects() -> dict:
    query = "SELECT * FROM project"
    database = Database()
    return database.read(query=query)


def run_experiment(project_id: int, engine: str, model: object, target_col: str, train_data: pd.DataFrame, test_data: pd.DataFrame, metrics: dict) -> int:

    _ENGINES = ['sklearn']
    if engine not in _ENGINES:
        raise Exception(f'Engine not registered, must be one of the following: {",".join(_ENGINES)}')

    database = Database()
    query = f"INSERT INTO experiment (project_id, engine) VALUES ('{project_id}', '{engine}')"
    experiment_id = database.write(query=query)

    registry = Registry()
    registry.put_model(path=f"{project_id}-{experiment_id}", key='pre-model', model=model)
    registry.put_metrics(path=f"{project_id}-{experiment_id}", key='metrics', metrics=metrics)
    registry.put_dataset(path=f"{project_id}-{experiment_id}", key='test', dataset=test_data)
    registry.put_dataset(path=f"{project_id}-{experiment_id}", key='train', dataset=train_data)

    pipeline = Pipeline()
    conf = {'experiment_id': experiment_id, 'project_id': project_id, 'target_col': target_col}
    triggered = pipeline.trigger_dag(dag_id=f'{engine}-pipeline', data=dict(conf=conf))

    if triggered:
        query = f"UPDATE experiment SET status = 'submitted' WHERE id = {experiment_id}"
        database.write(query=query)
    else:
        query = f"UPDATE experiment SET status = 'submission-failed' WHERE id = {experiment_id}"
        database.write(query=query)
        raise Exception('Pipeline failed to run experiment')

    return experiment_id


def get_experiments() -> dict:
    query = "SELECT * FROM experiment"
    database = Database()
    return database.read(query=query)


def get_experiment(experiment_id: int) -> dict:
    query = f"SELECT * FROM experiment WHERE id = {experiment_id}"
    database = Database()
    return database.read(query=query)[0]


def get_experiment_model(experiment_id: int) -> object:
    database = Database()
    query = f"SELECT project_id FROM experiment WHERE id = {experiment_id}"
    project_id = database.read(query=query)[0]['project_id']
    registry = Registry()
    return registry.get_model(path=f"{project_id}-{experiment_id}", key='model')


def get_experiment_features(experiment_id: int) -> pd.DataFrame:
    database = Database()
    query = f"SELECT project_id FROM experiment WHERE id = {experiment_id}"
    project_id = database.read(query=query)[0]['project_id']
    registry = Registry()
    return registry.get_dataset(path=f"{project_id}-{experiment_id}", key='features')


def get_experiment_target(experiment_id: int) -> pd.DataFrame:
    database = Database()
    query = f"SELECT project_id FROM experiment WHERE id = {experiment_id}"
    project_id = database.read(query=query)[0]['project_id']
    registry = Registry()
    return registry.get_dataset(path=f"{project_id}-{experiment_id}", key='target')


def deploy_experiment(experiment_id: int) -> bool:
    database = Database()
    query = f"SELECT project_id FROM experiment WHERE id = {experiment_id}"
    project_id = database.read(query=query)[0]['project_id']
    query = f"UPDATE experiment SET status = 'rolled-back' WHERE project_id = '{project_id}' AND status = 'deployed'"
    database.write(query=query)
    query = f"UPDATE experiment SET status = 'deployed' WHERE id = {experiment_id}"
    database.write(query=query)
    return True


def get_deployments():
    query = f"SELECT * FROM experiment WHERE status = 'deployed'"
    database = Database()
    return database.read(query=query)


def get_predictions(project_id: int):
    database = Database()
    query = f"SELECT * FROM serving WHERE project_id = {project_id}"
    return database.read(query=query)


def get_prediction(prediction_id: int):
    database = Database()
    query = f"SELECT * FROM serving WHERE id = {prediction_id}"
    return database.read(query=query)[0]
