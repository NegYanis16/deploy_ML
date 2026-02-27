from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib
import os
from app.config import logger, MODEL_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Phase de démarrage
    
    # 1. Créer les tables si elles n'existent pas
    try:
        logger.info("Vérification et création des tables de base de données...")
        from app.core.database import Base, engine
        from app.models import EmployeeData, Prediction
        
        Base.metadata.create_all(bind=engine)
        logger.info("Tables de base de données vérifiées/créées avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de la création des tables: {e}")
    
    # 2. Charger le modèle ML
    if os.path.exists(MODEL_PATH):
        try:
            app.state.model = joblib.load(MODEL_PATH)
            logger.info("Modèle chargé en mémoire avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle : {e}")
            app.state.model = None
    else:
        logger.warning(f"Fichier modèle introuvable au chemin {MODEL_PATH}")
        app.state.model = None
    
    yield # L'API est prete a recevoir des requetes
    
    # Phase d'arrêt
    app.state.model = None