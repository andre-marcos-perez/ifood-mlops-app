import joblib as pickle
from pathlib import Path

import pandas as pd


class Registry(object):

    def __init__(self):
        self._base_dir = '/opt/registry'

    def put_metrics(self, path: str, key: str, metrics: dict):
        directory = Path(f"{self._base_dir}/{path}")
        directory.mkdir(parents=True, exist_ok=True)
        pickle.dump(metrics, filename=f"{self._base_dir}/{path}/{key}.pickle")

    def get_metrics(self, path: str, key: str) -> object:
        metrics = pickle.load(filename=f"{self._base_dir}/{path}/{key}.pickle")
        return metrics

    def put_model(self, path: str, key: str, model: object):
        directory = Path(f"{self._base_dir}/{path}")
        directory.mkdir(parents=True, exist_ok=True)
        pickle.dump(model, filename=f"{self._base_dir}/{path}/{key}.pickle")

    def get_model(self, path: str, key: str) -> object:
        model = pickle.load(filename=f"{self._base_dir}/{path}/{key}.pickle")
        return model

    def put_dataset(self, path: str, key: str, dataset: pd.DataFrame):
        directory = Path(f"{self._base_dir}/{path}")
        directory.mkdir(parents=True, exist_ok=True)
        dataset.to_csv(f"{self._base_dir}/{path}/{key}.csv")

    def get_dataset(self, path: str, key: str) -> pd.DataFrame:
        return pd.read_csv(f"{self._base_dir}/{path}/{key}.csv")
