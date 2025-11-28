from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.db.session import get_db
from backend.models.startup import Startup
from backend.schemas.search import (
    StartupSearchRequest, 
    StartupSearchFilters, 
    SearchResponse,
    StartupSearchResult,
    SearchSortBy,
    AutocompleteResult
)
from backend.services.search_service import SearchService

router = APIRouter()

def get_search_service(db: Session = Depends(get_db)):
    return SearchService(db)

@router.get("/search", response_model=SearchResponse)
def search_startups(
    q: Optional[str] = Query(None, description="Término de búsqueda"),
    categorias: Optional[str] = Query(None, description="Filtrar por categorías"),
    min_votos: Optional[int] = Query(None, ge=0, description="Mínimo número de votos"),
    min_comentarios: Optional[int] = Query(None, ge=0, description="Mínimo número de comentarios"),
    sort_by: SearchSortBy = Query(SearchSortBy.RELEVANCIA, description="Criterio de ordenamiento"),
    page: int = Query(1, ge=1, description="Página"),
    limit: int = Query(50, ge=1, le=100, description="Resultados por página"),
    service: SearchService = Depends(get_search_service)
):
    print(f"🔍 DEBUG: categorias parameter = {categorias} (type: {type(categorias)})")  # ← DEBUG    
    """Búsqueda avanzada de startups con todos los filtros"""
    skip = (page - 1) * limit
    
    categoria_list = None
    if categorias:
        try:
            categoria_list = [int(cat.strip()) for cat in categorias.split(",")]
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de categorías inválido")
        
    filters = StartupSearchFilters(
        categorias=categoria_list,
        min_votos=min_votos,
        min_comentarios=min_comentarios,
    )

    search_request = StartupSearchRequest(
        query=q,
        filters=filters,
        sort_by=sort_by,
        skip=skip,
        limit=limit
    )
    
    return service.search_startups(search_request)

@router.get("/autocomplete", response_model=List[AutocompleteResult])
def autocomplete_startups(
    q: str = Query(..., min_length=2, description="Término para autocompletado"),
    limit: int = Query(10, ge=1, le=20),
    service: SearchService = Depends(get_search_service)
):
    """Autocompletado rápido de nombres de startups"""
    results = service.autocomplete(q, limit)
    return [AutocompleteResult(**result) for result in results]

@router.get("/{startup_id}", response_model=StartupSearchResult)
def get_startup_detail(
    startup_id: int,
    service: SearchService = Depends(get_search_service)
):
    """Obtener detalles completos de una startup"""
    query = service._build_base_query()
    result = query.filter(Startup.startup_id == startup_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Startup no encontrada")
    
    startup, total_comentarios, total_votos = result
    
    return StartupSearchResult(
        startup_id=startup.startup_id,
        name=startup.name,
        description=startup.description or "",
        owner_user_id=startup.owner_user_id,
        category_id=startup.category_id,
        total_votos=total_votos,
        total_comentarios=total_comentarios
    )