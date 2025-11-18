from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.router import api_router
from backend.db.session import ping_db
from backend.core.config import get_settings

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

# CORS
settings = get_settings()
cors_raw = settings.cors_origins or "*"
origins = [o.strip() for o in cors_raw.split(",") if o.strip()] or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    return ping_db()
