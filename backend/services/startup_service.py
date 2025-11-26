from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models.startup import Startup
from backend.schemas.startup_crud import StartupCreate, StartupUpdate, StartupOut, StartupWithStats
from backend.repositories.startup_repository import StartupRepository


class StartupService:
    def __init__(self, db: Session):
        self.repository = StartupRepository(db)

    def create(self, user_id: int, payload: StartupCreate) -> StartupOut:
        # Verificar que el usuario existe
        startup_data = payload.model_dump()
        startup_data['owner_user_id'] = user_id
        
        startup = Startup(**startup_data)
        created_startup = self.repository.create(startup)
        return StartupOut.model_validate(created_startup)
    
        #agregar verificación de usuario correspondiente aquí

    def get(self, startup_id: int) -> Optional[StartupOut]:
        startup = self.repository.get_by_id(startup_id)
        if startup:
            return StartupOut.model_validate(startup)
        return None

    def get_with_stats(self, startup_id: int) -> Optional[StartupWithStats]:
        result = self.repository.get_with_stats(startup_id)
        if result:
            startup, total_comentarios, total_votos = result
            startup_out = StartupWithStats.model_validate(startup)
            startup_out.total_comentarios = total_comentarios
            startup_out.total_votos = total_votos
            return startup_out
        return None

    def list(self, skip: int = 0, limit: int = 100) -> List[StartupOut]:
        startups = self.repository.get_all(skip, limit)
        return [StartupOut.model_validate(startup) for startup in startups]

    def list_by_owner(self, owner_user_id: int) -> List[StartupOut]:
        startups = self.repository.get_by_owner(owner_user_id)
        return [StartupOut.model_validate(startup) for startup in startups]

    def update(self, startup_id: int, user_id: int, payload: StartupUpdate) -> StartupOut:
        startup = self.repository.get_by_id(startup_id)
        if not startup:
            raise ValueError("Startup no encontrada")
        
        # Verificar que el usuario es el propietario comentariado para pruebas
        if startup.owner_user_id != user_id:
            raise PermissionError("No tienes permisos para editar esta startup")
        
        update_data = payload.model_dump(exclude_unset=True)
        updated_startup = self.repository.update(startup_id, update_data)
        if not updated_startup:
            raise ValueError("Error al actualizar la startup")
        
        return StartupOut.model_validate(updated_startup)

    def delete(self, startup_id: int, user_id: int) -> None:
        startup = self.repository.get_by_id(startup_id)
        if not startup:
            raise ValueError("Startup no encontrada")
        
        #Verificar que el usuario es el propietario
        if startup.owner_user_id != user_id:
            raise PermissionError("No tienes permisos para eliminar esta startup")
        
        if not self.repository.delete(startup_id):
            raise ValueError("Error al eliminar la startup")