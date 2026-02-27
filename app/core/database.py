from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import DATABASE_URL, logger

# Base pour les modèles ORM
Base = declarative_base()

# Création du moteur de connexion
logger.info("Initialisation de la connexion à la base de données")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("Connexion à la base de données établie")


def get_db():
    """
    Générateur de session pour FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()