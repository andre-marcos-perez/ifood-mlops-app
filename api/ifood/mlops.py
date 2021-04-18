from api.database import Database


def _get_database():
    return Database(host='localhost', port=3306, user='root', password='root', database='ifood_mlops_app_db')


def create_project(name: str) -> int:
    query = f"INSERT INTO project (name) VALUES ('{name}')"
    database = _get_database()
    return database.write(query=query)


def get_projects() -> dict:
    query = "SELECT * FROM project"
    database = _get_database()
    return database.read(query=query)


if __name__ == '__main__':

    projects = get_projects()
    print(projects)

    project_id = create_project(name='credit-score')

    projects = get_projects()
    print(projects)
