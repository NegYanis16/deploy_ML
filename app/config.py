import os
from dotenv import load_dotenv
from loguru import logger

# Charger les variables d'environnement
load_dotenv()  # Charge .env depuis la racine du projet
load_dotenv(".env.local", override=True)  # Écrase avec .env.local si présent
# Variables d'environnement
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MODEL_PATH = os.getenv("MODEL_PATH", "models")
DATABASE_URL = os.getenv("DATABASE_URL")
API_LOG_FILE = os.getenv("API_LOG_FILE", "logs/api.log")


# Configuration du logger
format_config = {
    "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
}

logger.add(API_LOG_FILE, rotation="10 MB", retention="7 days", level=LOG_LEVEL, **format_config)