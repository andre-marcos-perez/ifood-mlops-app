import pymysql


class Database(object):

    def __init__(self):
        self._host = 'localhost'
        self._port = 3306
        self._user = 'root'
        self._password = 'root'
        self._database = 'ifood_mlops_app_db'
        self._connection = self._connect()

    def _connect(self) -> pymysql.Connection:
        try:
            return pymysql.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                database=self._database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5
            )
        except Exception as exc:
            raise exc

    def read(self, query: str) -> dict:
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query=query)
                data = cursor.fetchall()
        except Exception as exc:
            raise exc
        else:
            return data

    def write(self, query: str) -> int:
        written_row_id = None
        try:
            with self._connection.cursor() as cursor:
                if isinstance(query, str):
                    cursor.execute(query=query)
                    written_row_id = cursor.lastrowid
                else:
                    raise TypeError('Query data type {type} is not allowed'.format(type=type(query)))
            self._connection.commit()
        except Exception as exc:
            raise exc
        else:
            return written_row_id
