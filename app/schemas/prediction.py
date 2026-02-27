from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    feature_1 = Column(Float, nullable=False)
    feature_2 = Column(Float, nullable=False)
    feature_3 = Column(Float, nullable=False)
    feature_4 = Column(Float, nullable=False)
    prediction = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())