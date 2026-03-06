from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.core.database import Base


class Prediction(Base):
    """
    Table pour stocker les prédictions (outputs).
    """
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=True)  # Optionnel, lien vers EmployeeData
    
    # Résultat de la prédiction
    prediction = Column(Integer)  # 0 = Reste, 1 = Part
    probability = Column(Float)  # Probabilité de départ
    risk_level = Column(String(20))  # High ou Low
    
    # Métadonnées
    created_at = Column(DateTime, default=datetime.utcnow)
    batch_id = Column(String(100), nullable=True)  # Pour regrouper les prédictions batch