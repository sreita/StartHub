from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from pydantic.config import ConfigDict


class StartupBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = None


class StartupCreate(StartupBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Mi Nueva Startup",
                    "description": "Una descripción innovadora",
                    "category_id": 1,
                }
            ]
        }
    )


class StartupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Nombre Actualizado",
                    "description": "Descripción",
                    "category_id": 2,
                }
            ]
        }
    )


class StartupOut(StartupBase):
    startup_id: int
    owner_user_id: int
    created_date: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class StartupWithStats(StartupOut):
    total_votos: int = 0
    total_comentarios: int = 0