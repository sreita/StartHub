from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, echo=settings.app_debug, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ping_db() -> dict:
    try:
        with engine.connect() as conn:
            result = conn.exec_driver_sql("SELECT 1").scalar()
            return {"ok": True, "result": int(result)}
    except Exception as e:
        return {"ok": False, "error": str(e)}
