from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.startup_crud import StartupCreate, StartupOut, StartupUpdate, StartupWithStats, CategoryOut
from app.services.startup_service import StartupService

router = APIRouter()

def get_startup_service(db: Session = Depends(get_db)):
    return StartupService(db)

@router.post("/", response_model=StartupOut, status_code=201)
def create_startup(
    payload: StartupCreate,
    service: StartupService = Depends(get_startup_service),
):
    try:
        return service.create(payload.owner_user_id, payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[StartupOut])
def list_startups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    service: StartupService = Depends(get_startup_service),
):
    return service.list(skip=skip, limit=limit)

@router.get("/my-startups", response_model=List[StartupOut])
def list_my_startups(
    user_id: int = Query(..., description="ID del usuario propietario"),
    service: StartupService = Depends(get_startup_service),
):
    return service.list_by_owner(user_id)

@router.get("/{startup_id}", response_model=StartupOut)
def get_startup(
    startup_id: int,
    service: StartupService = Depends(get_startup_service),
):
    startup = service.get(startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup no encontrada")
    return startup

@router.get("/{startup_id}/with-stats", response_model=StartupWithStats)
def get_startup_with_stats(
    startup_id: int,
    service: StartupService = Depends(get_startup_service),
):
    startup = service.get_with_stats(startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup no encontrada")
    return startup

@router.put("/{startup_id}", response_model=StartupOut)
def update_startup(
    startup_id: int,
    payload: StartupUpdate,
    user_id: int = Query(..., description="ID del usuario propietario"),
    service: StartupService = Depends(get_startup_service),
):
    try:
        return service.update(startup_id, user_id, payload)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{startup_id}", status_code=204)
def delete_startup(
    startup_id: int,
    user_id: int = Query(..., description="ID del usuario propietario"),
    service: StartupService = Depends(get_startup_service),
):
    try:
        service.delete(startup_id, user_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return None

# Endpoint para obtener categorías
@router.get("/categories/list", response_model=List[CategoryOut])
def list_categories(
    service: StartupService = Depends(get_startup_service),
):
    try:
        return service.list_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar categorías: {str(e)}")