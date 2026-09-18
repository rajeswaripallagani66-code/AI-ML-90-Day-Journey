from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "ML API Day 4 - Docker working!"}

@app.get("/predict")
def predict():
    return {"prediction": "success"}