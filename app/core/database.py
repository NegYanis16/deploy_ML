from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL, logger

# Base pour les modèles ORM
Base = declarative_base()


# Création du moteur de connexion uniquement si DATABASE_URL est défini
engine = None
SessionLocal = None
if DATABASE_URL:
    logger.info("Initialisation de la connexion à la base de données")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Connexion à la base de données établie")
else:
    logger.warning("DATABASE_URL non défini : la connexion à la base de données n'est pas initialisée.")


def get_db():
    """
    Générateur de session pour FastAPI.
    Retourne None si DATABASE_URL n'est pas défini (pas de DB disponible).
    """
    if SessionLocal is None:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()