from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
class Input(BaseModel):
    text:str
@app.post("/predict")
def predict(data:Input):
    return {"result":data.text}    