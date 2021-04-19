from api.database import Database
from api.pipeline import Pipeline


def create_project(name: str) -> int:
    query = f"INSERT INTO project (name) VALUES ('{name}')"
    database = Database()
    return database.write(query=query)


def get_projects() -> dict:
    query = "SELECT * FROM project"
    database = Database()
    return database.read(query=query)


def run_experiment(project_id: int, engine: str) -> int:

    _ENGINES = ['scikit']

    if engine not in _ENGINES:
        raise Exception(f'Engine not registered, must be one of the following: {",".join(_ENGINES)}')

    database = Database()
    query = f"INSERT INTO experiment (project_id, engine) VALUES ('{project_id}', '{engine}')"
    experiment_id = database.write(query=query)

    pipeline = Pipeline()
    triggered = pipeline.trigger_dag(dag_id='{engine}_pipeline', data={'conf': {'experiment_id': experiment_id}})

    if triggered:
        query = f"UPDATE experiment SET status = 'queued' WHERE id = {experiment_id}"
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
