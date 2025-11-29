from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.startup_crud import CategoryOut
from app.models.category import Category

router = APIRouter()

@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar categorías: {str(e)}")