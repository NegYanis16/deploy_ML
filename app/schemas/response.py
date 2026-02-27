from pydantic import BaseModel
from typing import List

class PredictResponse(BaseModel):
    prediction: int

class BatchPredictResponse(BaseModel):
    """Réponse pour une prédiction batch"""
    total_employees: int
    predictions: List[dict]