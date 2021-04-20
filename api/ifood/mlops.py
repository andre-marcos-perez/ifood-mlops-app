import json

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


def run_experiment(project_id: int, engine: str, model: object) -> int:

    _ENGINES = ['scikit']
    if engine not in _ENGINES:
        raise Exception(f'Engine not registered, must be one of the following: {",".join(_ENGINES)}')

    database = Database()
    query = f"INSERT INTO experiment (project_id, engine) VALUES ('{project_id}', '{engine}')"
    experiment_id = database.write(query=query)

    registry = Registry()
    registry.put_model(path=f"{project_id}-{experiment_id}", model=model)
    hyper_params = json.dumps(model.__dict__)

    pipeline = Pipeline()
    triggered = pipeline.trigger_dag(dag_id=f'{engine}-pipeline', data={'conf': {'experiment_id': experiment_id}})

    if triggered:
        query = f"UPDATE experiment SET status = 'submitted', hyperparams = '{hyper_params}' WHERE id = {experiment_id}"
        database.write(query=query)
    else:
        query = f"UPDATE experiment SET status = 'failed' WHERE id = {experiment_id}"
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
    return database.read(query=query)


def deploy_experiment(experiment_id: int) -> int:
    pass


if __name__ == '__main__':

    from sklearn import *

    pid = create_project(name='success')

    eid = run_experiment(project_id=pid, engine='scikit', model=linear_model.LogisticRegression())
    print(eid)

    eids = get_experiment(experiment_id=1)
    print(eids)
