import json
import typing
from datetime import datetime

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from database import Database
from registry import Registry

app = FastAPI()


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


@app.post("/predictions", response_model=Predicted)
async def predict(prediction: Prediction) -> typing.Dict[str, typing.Union[str, typing.Any]]:

    database = Database()
    registry = Registry()

    prediction_dict = prediction.dict()

    query = f"SELECT id FROM project WHERE name = '{prediction_dict['model']}'"
    project_id = database.read(query=query)[0]['id']

    query = f"SELECT id FROM experiment WHERE id = '{project_id}' AND status = 'deployed'"
    experiment_id = database.read(query=query)[0]['id']

    model = registry.get_model(path=f"{project_id}-{experiment_id}", key='model')
    predicted = model.predict(pd.DataFrame(prediction_dict['features'], index=[0]))
    predicted = {'prediction': predicted.tolist()[0]}

    query = f"INSERT INTO serving (project_id, experiment_id, payload) VALUES ('{project_id}', '{experiment_id}', '{json.dumps(predicted)}')"
    prediction_id = database.write(query)

    payload = dict()
    payload.update({'id': prediction_id})
    payload.update(predicted)
    payload.update({'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')})

    return payload
