import json

import requests


class Pipeline(object):

    def __init__(self):
        self._base_url = 'http://localhost:8080/api/experimental/dags'
        self._suff_url = 'dag_runs'

    def trigger_dag(self, dag_id: str, data: dict) -> bool:

        url = f'{self._base_url}/{dag_id}/{self._suff_url}'
        headers = {'Cache-Control': 'no-cache', 'Content-Type': 'application/json'}

        try:
            response = requests.post(url=url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
        except Exception as exc:
            raise exc
        else:
            return True
