from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class CommentBase(BaseModel):
    content: str = Field(min_length=1)
    startup_id: int


class CommentCreate(CommentBase):
    # Example para Swagger
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "content": "Gran startup, muy buen equipo",
                    "startup_id": 1,
                }
            ]
        }
    )


class CommentUpdate(BaseModel):
    content: str = Field(min_length=1)
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"content": "Actualizando el comentario con más detalle"}
            ]
        }
    )


class CommentOut(CommentBase):
    comment_id: int
    user_id: int
    created_date: datetime
    modified_date: datetime | None = None

    # Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)
