from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.db.session import ping_db
from app.core.config import get_settings

app = FastAPI(
    title="StartHub Backend - Comentarios y Votos",
    version="1.0.0",
    description=(
        "API para gestionar comentarios y votos de Startups. "
        "Endpoints documentados automáticamente en /docs (Swagger UI)."
    ),
    contact={
        "name": "StartHub",
        "url": "https://example.com",
    },
)

# CORS - Usa solo la configuración del settings
settings = get_settings()
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8081",
    "http://127.0.0.1:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    return ping_db()