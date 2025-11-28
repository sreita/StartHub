from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class SearchSortBy(str, Enum):
    RELEVANCIA = "relevancia"
    VOTOS_ASC = "votos_asc"
    VOTOS_DESC = "votos_desc"
    COMENTARIOS_ASC = "comentarios_asc"
    COMENTARIOS_DESC = "comentarios_desc"

class StartupSearchFilters(BaseModel):
    categorias: Optional[list[int]] = None
    min_votos: Optional[int] = None
    min_comentarios: Optional[int] = None

class StartupSearchRequest(BaseModel):
    query: Optional[str] = None
    filters: Optional[StartupSearchFilters] = None
    sort_by: SearchSortBy = SearchSortBy.RELEVANCIA
    skip: int = 0
    limit: int = 50

class StartupSearchResult(BaseModel):
    startup_id: int
    name: str
    description: str
    owner_user_id: int
    category_id: Optional[int]
    total_votos: int = 0
    total_comentarios: int = 0
    relevance_score: Optional[float] = None

class SearchResponse(BaseModel):
    results: List[StartupSearchResult]
    total: int
    page: int
    total_pages: int

class AutocompleteResult(BaseModel):
    startup_id: int
    name: str
    description: str