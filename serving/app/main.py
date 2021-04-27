import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from database import Database
from registry import Registry

app = FastAPI()


class Prediction(BaseModel):
    model: str
    features: dict


@app.post("/predictions")
async def predict(prediction: Prediction):

    database = Database()
    registry = Registry()

    prediction_dict = prediction.dict()
    print(prediction_dict)

    query = f"SELECT id FROM project WHERE name = '{prediction_dict['model']}'"
    project_id = database.read(query=query)[0]['id']

    query = f"SELECT id FROM experiment WHERE id = '{project_id}' AND status = 'deployed'"
    experiment_id = database.read(query=query)[0]['id']

    model = registry.get_model(path=f"{project_id}-{experiment_id}", key='model')
    predicted = model.predict(pd.DataFrame(prediction_dict['features']))

    return predicted
