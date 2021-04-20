import pickle
from pathlib import Path


class Registry(object):

    def __init__(self):
        self._base_dir = '/opt/registry'

    def put_model(self, path: str, model: object):
        dir = Path(f"{self._base_dir}/{path}")
        dir.mkdir(parents=True)
        pickle.dump(model, file=open(file=f"{self._base_dir}/{path}/model.pickle", mode='wb'))
