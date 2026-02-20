from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.api.routes import router

app = FastAPI(
    title="Futurisys ML API",
    description="API de prediction ML pour la production",
    version="1.0.0",
    lifespan=lifespan
)

# Ajout des routes definies dans le dossier api
app.include_router(router)