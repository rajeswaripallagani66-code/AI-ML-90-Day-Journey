from pydantic import BaseModel
from typing import List

class SensorFeatures(BaseModel):
    features: List[float]

class PredictionOut(BaseModel):
    prediction: int
    probability: float
    