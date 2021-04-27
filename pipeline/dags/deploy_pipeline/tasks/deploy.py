import logging

import requests


def deploy():

    logging.basicConfig(level=logging.INFO)

    try:
        response = requests.post(url='http://localhost:8000/models')
        response.raise_for_status()
    except Exception as exc:
        raise exc
    else:
        logging.info(response.text)
        return True
