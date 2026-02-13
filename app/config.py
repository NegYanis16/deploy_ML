import os
import sys
from dotenv import load_dotenv
from loguru import logger

# Charger les variables d'environnement
load_dotenv()

# Variables d'environnement
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MODEL_PATH = os.getenv("MODEL_PATH", "./models")

# Configuration du logger
def setup_logger():
    """
    Configure le logger pour l'application.
    """
    logger.remove()
    logger.add(
        sys.stdout,
        level=LOG_LEVEL,
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    )

setup_logger()
