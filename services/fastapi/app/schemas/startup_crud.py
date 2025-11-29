from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from pydantic.config import ConfigDict


class StartupBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    category_id: int
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+')
    website: Optional[str] = Field(None, max_length=255)
    social_media: Optional[str] = Field(None, max_length=255)



class CategoryOut(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
class StartupCreate(StartupBase):
    owner_user_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Mi Nueva Startup",
                    "description": "Una descripción innovadora",
                    "category_id": 1,
                    "email": "contacto@startup.com",
                    "website": "https://startup.com",
                    "social_media": "@startup",
                    "owner_user_id": 1
                }
            ]
        }
    )


class StartupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    category_id: Optional[int] = None
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+')
    website: Optional[str] = Field(None, max_length=255)
    social_media: Optional[str] = Field(None, max_length=255)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Nombre Actualizado",
                    "description": "Descripción actualizada",
                    "category_id": 2,
                    "email": "nuevo@startup.com",
                    "website": "https://nuevo.startup.com",
                    "social_media": "@nuevostartup"
                }
            ]
        }
    )


class StartupOut(StartupBase):
    startup_id: int
    owner_user_id: int
    created_date: Optional[datetime] = None
    category_name: Optional[str] = None
    owner_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class StartupWithStats(StartupOut):
    total_votos: int = 0
    total_comentarios: int = 0