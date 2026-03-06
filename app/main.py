from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.routes.routes import router

app = FastAPI(
    title="Futurisys ML API",
    description="API de prediction ML pour la production",
    version="1.0.0",
    lifespan=lifespan
)

# Ajout des routes
app.include_router(router)