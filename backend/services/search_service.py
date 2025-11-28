from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, case
from sqlalchemy.sql import expression
from typing import List, Optional, Dict, Any
import re

from backend.models.startup import Startup
from backend.models.comment import Comment
from backend.models.vote import Vote
from backend.schemas.search import StartupSearchRequest, StartupSearchResult, SearchSortBy

class SearchService:
    def __init__(self, db: Session):
        self.db = db

    def _calculate_relevance(self, text: str, search_term: str) -> float:
        """Calcula un puntaje de relevancia basado en coincidencias"""
        if not search_term or not text:
            return 0.0
        
        search_term = search_term.lower().strip()
        text_lower = text.lower()
        
        # Si el término es muy corto (1-2 caracteres), solo coincidencia al INICIO de palabra
        if len(search_term) <= 2:
            words = text_lower.split()
            # Solo dar puntaje si está al INICIO de una palabra
            for word in words:
                if word.startswith(search_term):
                    return 0.8  # Buen score solo si inicia palabra
            return 0.0  # Cero si no inicia palabra
        
        # PARA TÉRMINOS DE 3+ CARACTERES
        
        # 1. Coincidencia EXACTA (máxima prioridad)
        if search_term == text_lower:
            return 1.0
        
        # 2. Coincidencia al INICIO de palabra
        words = text_lower.split()
        for word in words:
            if word.startswith(search_term):
                return 0.9
        
        # 3. Coincidencia de PALABRA COMPLETA
        if search_term in words:
            return 0.8
        
        # 4. Coincidencia de MÚLTIPLES PALABRAS (si el search_term tiene espacios)
        search_words = search_term.split()
        if len(search_words) > 1:
            matches = 0
            for s_word in search_words:
                if any(s_word in word for word in words):
                    matches += 1
            if matches > 0:
                return 0.4 + (matches / len(search_words)) * 0.3
        
        # 5. Coincidencia de SUBCADENA (último recurso)
        if search_term in text_lower:
            return 0.3
        
        return 0.0

    def _build_base_query(self):
        """Construye query base con joins para estadísticas"""
        # Subquery para contar comentarios por startup
        comentarios_subq = self.db.query(
            Comment.startup_id,
            func.count(Comment.comment_id).label('total_comentarios')
        ).group_by(Comment.startup_id).subquery()

        # Subquery para contar votos por startup
        votos_subq = self.db.query(
            Vote.startup_id,
            func.count(Vote.vote_id).label('total_votos')
        ).group_by(Vote.startup_id).subquery()

        # Query principal con joins
        query = self.db.query(
            Startup,
            func.coalesce(comentarios_subq.c.total_comentarios, 0).label('total_comentarios'),
            func.coalesce(votos_subq.c.total_votos, 0).label('total_votos')
        ).outerjoin(
            comentarios_subq, Startup.startup_id == comentarios_subq.c.startup_id
        ).outerjoin(
            votos_subq, Startup.startup_id == votos_subq.c.startup_id
        )

        return query

    def search_startups(self, search_request: StartupSearchRequest) -> Dict[str, Any]:
        """Búsqueda principal con todos los filtros y ordenamientos"""
        query = self._build_base_query()
        
        # Aplicar búsqueda de texto con fuzzy matching
        if search_request.query and search_request.query.strip():
            search_term = search_request.query.strip()
            search_pattern = f"%{search_term}%"
        
            # Filtro básico con LIKE - pero SOLO para búsquedas de 2+ caracteres
            if len(search_term) >= 2:
                query = query.filter(
                    or_(
                        Startup.name.ilike(search_pattern),
                        Startup.description.ilike(search_pattern)
                    )
                )
            else:
                # Para 1 carácter, buscar solo al INICIO de palabras
                query = query.filter(
                    or_(
                        Startup.name.ilike(search_term + "%"),  # "f%" - solo inicio
                        Startup.description.ilike(search_term + "%")
                    )
                )
        
        # Aplicar filtros
        if search_request.filters:
            filters = search_request.filters
            
            if filters.categorias:
                query = query.filter(Startup.category_id.in_(filters.categorias))
            
            if filters.min_votos is not None:
                query = query.filter(expression.column('total_votos') >= filters.min_votos)
            
            if filters.min_comentarios is not None:
                query = query.filter(expression.column('total_comentarios') >= filters.min_comentarios)
        
        # Sort
        sort_mappings = {
            SearchSortBy.VOTOS_ASC: expression.column('total_votos').asc(),
            SearchSortBy.VOTOS_DESC: expression.column('total_votos').desc(),
            SearchSortBy.COMENTARIOS_ASC: expression.column('total_comentarios').asc(),
            SearchSortBy.COMENTARIOS_DESC: expression.column('total_comentarios').desc(),
        }
    
        # Aplicar sort
        if search_request.sort_by in sort_mappings:
            query = query.order_by(sort_mappings[search_request.sort_by])
        else:  # relevancia por defecto
            if search_request.query and search_request.query.strip():
                search_term = search_request.query.strip()
                search_pattern = f"%{search_term}%"
                query = query.order_by(
                Startup.name.ilike(search_pattern).desc(),
                Startup.description.ilike(search_pattern).desc(),
                expression.column('total_votos').desc()
                )
            else:
                query = query.order_by(expression.column('total_votos').desc())
        
        # Obtener total para paginación
        total = query.count()
        
        # Aplicar paginación
        results = query.offset(search_request.skip).limit(search_request.limit).all()
        
        # Procesar resultados con relevancia 
        processed_results = []
        for startup, total_comentarios, total_votos in results:
            relevance_score = 0.0
            if search_request.query:
                relevance_score = max(
                    self._calculate_relevance(startup.name, search_request.query),
                    self._calculate_relevance(startup.description or "", search_request.query)
                )
            
            # SOLO agregar si tiene relevancia > 0 O si no hay query de búsqueda
            if not search_request.query or relevance_score > 0:
                processed_results.append(StartupSearchResult(
                    startup_id=startup.startup_id,
                    name=startup.name,
                    description=startup.description or "",
                    owner_user_id=startup.owner_user_id,
                    category_id=startup.category_id,
                    total_votos=total_votos,
                    total_comentarios=total_comentarios,
                    relevance_score=relevance_score
                ))
        
        # ORDENAR por relevancia si es búsqueda con query
        if search_request.query and search_request.sort_by == SearchSortBy.RELEVANCIA:
            processed_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return {
            "results": processed_results,
            "total": len(processed_results),  # Usar el count real después de filtrar por relevancia
            "page": (search_request.skip // search_request.limit) + 1,
            "total_pages": (len(processed_results) + search_request.limit - 1) // search_request.limit if search_request.limit > 0 else 1
        }

    def autocomplete(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Autocompletado rápido de nombres de startups"""
        if not query or len(query.strip()) < 2:
            return []
        
        search_term = query.strip()
        search_pattern = f"%{search_term}%"
        
        startups = self.db.query(Startup).filter(
            Startup.name.ilike(search_pattern)
        ).order_by(Startup.name).limit(limit).all()
        
        return [{
            "startup_id": startup.startup_id,
            "name": startup.name,
            "description": startup.description or ""
        } for startup in startups]