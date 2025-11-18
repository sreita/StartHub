from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect

from backend.core.config import get_settings
from backend.db.session import get_db

router = APIRouter()


@router.post("/bootstrap", tags=["dev"])
def bootstrap_dev(db: Session = Depends(get_db)):
    settings = get_settings()
    if not settings.app_debug:
        # No exponer en producción
        raise HTTPException(status_code=404, detail="Not found")

    # Verificar tablas requeridas; si no existen, instruir migraciones
    inspector = inspect(db.bind)
    missing = [t for t in ("User", "Startup") if not inspector.has_table(t)]
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Tablas faltantes {missing}. Ejecuta migraciones: 'alembic -c backend/alembic.ini upgrade head'",
        )

    # Insertar datos mínimos si no existen
    with db.begin():
        u = db.execute(text("SELECT user_id FROM `User` WHERE user_id=1")).fetchone()
        if not u:
            db.execute(text(
                "INSERT INTO `User` (user_id, email, password_hash, first_name, last_name, is_enabled) "
                "VALUES (1,'dev@example.com','hash','Dev','User',1)"
            ))

        s = db.execute(text("SELECT startup_id FROM Startup WHERE startup_id=1")).fetchone()
        if not s:
            db.execute(text(
                "INSERT INTO Startup (startup_id, name, description, owner_user_id, category_id) "
                "VALUES (1,'Demo','Desc',1,NULL)"
            ))

    return {"ok": True, "seeded": ["User(1)", "Startup(1)"]}
