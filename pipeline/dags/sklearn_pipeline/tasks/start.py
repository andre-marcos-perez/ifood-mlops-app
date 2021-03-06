from shared.database import Database


def start(**context):

    experiment_id = context['dag_run'].conf.get('experiment_id')

    database = Database()
    query = f"UPDATE experiment SET status = 'queued' WHERE id = {experiment_id}"
    database.write(query=query)

    return True
