from functools import lru_cache
from pathlib import Path
import os
from typing import Any

try:  # pydantic ValidationError import (v2)
    from pydantic import ValidationError  # type: ignore
except Exception:  # pragma: no cover
    ValidationError = Exception  # fallback to avoid import errors

# Ruta al directorio backend
BACKEND_DIR = Path(__file__).resolve().parents[1]

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore

    class Settings(BaseSettings):
        # database_url may be omitted; fallback to in-memory SQLite for tests/CI/local dev when absent.
        database_url: str | None = None
        app_debug: bool = False
        cors_origins: str = "*"  # Comma-separated list or "*"

        # Pydantic Settings v2 config
        model_config = SettingsConfigDict(
            env_file=str(BACKEND_DIR / ".env"),
            env_file_encoding="utf-8",
        )

    @lru_cache
    def get_settings() -> "Settings":  # noqa: F821
        s = Settings()
        if not s.database_url:
            # Fallback: ephemeral in-memory DB. Suitable for tests/CI.
            object.__setattr__(s, "database_url", "sqlite+pysqlite:///:memory:")
        return s

except ModuleNotFoundError:
    from pydantic import BaseModel

    class Settings(BaseModel):
        database_url: str
        app_debug: bool = False
        cors_origins: str = "*"

    _cached: Settings | None = None

    def get_settings() -> Settings:
        global _cached
        if _cached is None:
            db_url = os.getenv("DATABASE_URL")
            if not db_url:
                raise RuntimeError(
                    "DATABASE_URL no definido. Cree backend/.env o instale 'pydantic-settings'."
                )
            debug = os.getenv("APP_DEBUG", "false").lower() == "true"
            cors = os.getenv("CORS_ORIGINS", "*")
            _cached = Settings(database_url=db_url, app_debug=debug, cors_origins=cors)
        return _cached