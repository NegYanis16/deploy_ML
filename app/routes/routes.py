from fastapi import APIRouter, HTTPException, Request
import numpy as np

# On importe les schemas qu'on va creer juste apres
from app.schemas.request import PredictRequest
from app.schemas.response import PredictResponse

router = APIRouter()

@router.get("/health", tags=["System"])
async def health_check(request: Request):
    model_status = "loaded" if request.app.state.model else "not_loaded"
    return {"status": "ok", "model_status": model_status}

@router.post("/predict", response_model=PredictResponse, tags=["ML"])
async def predict(data: PredictRequest, request: Request):
    model = request.app.state.model
    if not model:
        raise HTTPException(status_code=503, detail="Le modele n'est pas pret.")

    try:
        # Formatage des donnees entrantes en tableau 2D pour Scikit-Learn
        # A adapter selon le nombre exact de features de ton modele
        input_array = [[
            data.feature_1,
            data.feature_2,
            data.feature_3,
            data.feature_4
        ]]

        # Execution de la prediction
        prediction = model.predict(input_array)[0]

        return PredictResponse(prediction=int(prediction))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))