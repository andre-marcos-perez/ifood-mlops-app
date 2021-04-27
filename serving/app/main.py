import json
import typing
from datetime import datetime

import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, Header

from models import Models
from database import Database
from registry import Registry


class Prediction(BaseModel):

    model: str
    features: typing.Dict[str, typing.Any]

    class Config:
        schema_extra = {
            "example": {
                "model": "iris",
                "features": {"sepal-length": 5.7, "sepal-width": 3.8, "petal-length": 1.7, "petal-width": 0.3},
            }
        }


class Predicted(BaseModel):

    id: int
    prediction: typing.Any
    timestamp: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "prediction": 0,
                "timestamp": "2021-04-27T04:59:48Z"
            }
        }


app = FastAPI(title='Serving API')


@app.post("/predictions", response_model=Predicted)
def predict(prediction: Prediction, x_api_key: str = Header(None)) -> typing.Dict[str, typing.Union[str, typing.Any]]:

    """
    Generate predictions using memory loaded models
    """

    models = Models()
    database = Database()
    prediction_dict = prediction.dict()

    model_name = prediction_dict["model"]
    model_object = models.in_memory_models[model_name]["model_object"]
    predicted = model_object.predict(pd.DataFrame(prediction_dict['features'], index=[0]))

    project_id = models.in_memory_models[model_name]["project_id"]
    experiment_id = models.in_memory_models[model_name]["experiment_id"]
    query = f"" \
            f"INSERT INTO serving (project_id, experiment_id, payload, api_key) " \
            f"VALUES ('{project_id}', '{experiment_id}', '{json.dumps(predicted.tolist()[0])}', '{x_api_key}')"
    prediction_id = database.write(query)

    payload = dict()
    payload.update({'id': prediction_id})
    payload.update({'prediction': predicted.tolist()[0]})
    payload.update({'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')})

    return payload


@app.post("/models")
def update_models_in_memory() -> typing.Dict[str, typing.Union[bool, typing.Any]]:

    """
    Dumps deployed models into memory to speed up inference process
    """

    models = Models()
    database = Database()
    registry = Registry()

    try:

        query = f"" \
                f"SELECT e.id as 'experiment_id', e.project_id as 'project_id', p.name as 'model_name' " \
                f"FROM experiment e, project p " \
                f"WHERE e.status = 'deployed' AND e.project_id = p.id"
        models_metadata = database.read(query=query)

        for model_metadata in models_metadata:
            model_name = model_metadata['model_name']
            project_id = model_metadata['project_id']
            experiment_id = model_metadata['experiment_id']
            model_object = registry.get_model(path=f"{project_id}-{experiment_id}", key='model')
            models.in_memory_models.update({f"{model_name}": {'model_object': model_object, 'project_id': project_id, 'experiment_id': experiment_id}})

    except Exception as exc:
        raise exc

    else:
        payload = dict()
        payload.update({"status": True})
        return payload
