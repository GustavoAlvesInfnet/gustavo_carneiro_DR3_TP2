from fastapi import FastAPI
import pandas as pd
import json
from pydantic import BaseModel

class GreetingModel(BaseModel):
    texts: str

app = FastAPI()

items = []

# uvicorn api:app --reload

@app.get("/")
def read_root():
    df = pd.read_csv("../data/enem.csv")
    #transforma o csv em json
    enemJson = df.to_json(orient='records')
    #transforma o json em dicionário
    enemJson = json.loads(enemJson)
    
    return enemJson


@app.get("/items/{item_id}")
def read_item(item_id: int):
    df = pd.read_csv("../data/enem.csv")
    
    #transforma o csv em json
    enemJson = df.to_json(orient='records')

    #transforma o json em dicionário
    enemJson = json.loads(enemJson)
    
    return enemJson[item_id]


#post
@app.post("/items/post/")
def send_data(data: GreetingModel):
    print(data.texts)
    return {"status": 200}
