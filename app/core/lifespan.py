from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib
import os

# Chemin vers le modele (relatif a la racine du projet)
MODEL_PATH = "services/model.joblib"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Phase de demarrage
    if os.path.exists(MODEL_PATH):
        try:
            app.state.model = joblib.load(MODEL_PATH)
            print("Modele charge en memoire avec succes.")
        except Exception as e:
            print(f"Erreur lors du chargement du modele : {e}")
            app.state.model = None
    else:
        print(f"Attention : Fichier modele introuvable au chemin {MODEL_PATH}")
        app.state.model = None
    
    yield # L'API est prete a recevoir des requetes
    
    # Phase d'arret
    app.state.model = None