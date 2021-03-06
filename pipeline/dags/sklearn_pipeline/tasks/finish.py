from shared.database import Database


def finish(**context):

    experiment_id = context['dag_run'].conf.get('experiment_id')

    database = Database()
    query = f"UPDATE experiment SET status = 'finished' WHERE id = {experiment_id}"
    database.write(query=query)

    return True
