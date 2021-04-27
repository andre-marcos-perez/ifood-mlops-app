from shared.database import Database


def setup(**context):

    experiment_id = context['dag_run'].conf.get('experiment_id')

    database = Database()

    query = f"SELECT project_id FROM experiment WHERE id = {experiment_id}"
    project_id = database.read(query=query)[0]['project_id']

    query = f"UPDATE experiment SET status = 'rolled-back' WHERE project_id = '{project_id}' AND status = 'deployed'"
    database.write(query=query)

    query = f"UPDATE experiment SET status = 'deployed' WHERE id = {experiment_id}"
    database.write(query=query)

    return True
