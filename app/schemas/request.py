from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    feature_1: float = Field(..., description="Premiere caracteristique")
    feature_2: float = Field(..., description="Deuxieme caracteristique")
    feature_3: float = Field(..., description="Troisieme caracteristique")
    feature_4: float = Field(..., description="Quatrieme caracteristique")

    # Fournit un exemple concret pour la documentation Swagger générée automatiquement
    model_config = {
        "json_schema_extra": {
            "example": {
                "feature_1": 5.1,
                "feature_2": 3.5,
                "feature_3": 1.4,
                "feature_4": 0.2
            }
        }
    }