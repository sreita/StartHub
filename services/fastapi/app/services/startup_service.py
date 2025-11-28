from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.startup import Startup
from app.schemas.startup_crud import StartupCreate, StartupUpdate, StartupOut, StartupWithStats
from app.repositories.startup_repository import StartupRepository


class StartupService:
    def __init__(self, db: Session):
        self.repository = StartupRepository(db)

    def create(self, user_id: int, payload: StartupCreate) -> StartupOut:
        startup_data = payload.model_dump()
        startup_data['owner_user_id'] = user_id

        startup = Startup(**startup_data)
        created_startup = self.repository.create(startup)
        return self._enrich_startup_out(created_startup)

    def get(self, startup_id: int) -> Optional[StartupOut]:
        startup = self.repository.get_by_id(startup_id)
        if startup:
            return self._enrich_startup_out(startup)
        return None

    def get_with_stats(self, startup_id: int) -> Optional[StartupWithStats]:
        result = self.repository.get_with_stats(startup_id)
        if result:
            startup, total_comentarios, total_votos = result
            startup_out = self._enrich_startup_with_stats(startup, total_comentarios, total_votos)
            return startup_out
        return None

    def list(self, skip: int = 0, limit: int = 100) -> List[StartupOut]:
        startups = self.repository.get_all(skip, limit)
        return [self._enrich_startup_out(startup) for startup in startups]

    def list_by_owner(self, owner_user_id: int) -> List[StartupOut]:
        startups = self.repository.get_by_owner(owner_user_id)
        return [self._enrich_startup_out(startup) for startup in startups]

    def update(self, startup_id: int, user_id: int, payload: StartupUpdate) -> StartupOut:
        startup = self.repository.get_by_id(startup_id)
        if not startup:
            raise ValueError("Startup no encontrada")

        if startup.owner_user_id != user_id:
            raise PermissionError("No tienes permisos para editar esta startup")

        update_data = payload.model_dump(exclude_unset=True)
        updated_startup = self.repository.update(startup_id, update_data)
        if not updated_startup:
            raise ValueError("Error al actualizar la startup")

        return self._enrich_startup_out(updated_startup)

    def delete(self, startup_id: int, user_id: int) -> None:
        startup = self.repository.get_by_id(startup_id)
        if not startup:
            raise ValueError("Startup no encontrada")

        if startup.owner_user_id != user_id:
            raise PermissionError("No tienes permisos para eliminar esta startup")

        if not self.repository.delete(startup_id):
            raise ValueError("Error al eliminar la startup")

    # ESTOS MÉTODOS DEBEN ESTAR DENTRO DE LA CLASE
    def _enrich_startup_out(self, startup: Startup) -> StartupOut:
        """Enriquece el objeto Startup con category_name y owner_name antes de convertirlo a StartupOut"""
        startup_dict = {
            "startup_id": startup.startup_id,
            "name": startup.name,
            "description": startup.description,
            "category_id": startup.category_id,
            "owner_user_id": startup.owner_user_id,
            "created_date": startup.created_date,
            "category_name": getattr(startup, 'category_name', None),
            "owner_name": getattr(startup, 'owner_name', f"Usuario {startup.owner_user_id}")
        }
        return StartupOut(**startup_dict)

    def _enrich_startup_with_stats(self, startup: Startup, total_comentarios: int, total_votos: int) -> StartupWithStats:
        """Enriquece el objeto Startup con estadísticas, category_name y owner_name"""
        startup_dict = {
            "startup_id": startup.startup_id,
            "name": startup.name,
            "description": startup.description,
            "category_id": startup.category_id,
            "owner_user_id": startup.owner_user_id,
            "created_date": startup.created_date,
            "category_name": getattr(startup, 'category_name', None),
            "owner_name": getattr(startup, 'owner_name', f"Usuario {startup.owner_user_id}"),
            "total_comentarios": total_comentarios,
            "total_votos": total_votos
        }
        return StartupWithStats(**startup_dict)