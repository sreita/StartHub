from sqlalchemy.orm import Session
from app.repositories.comment_repository import CommentRepository
from sqlalchemy import text
from app.schemas.comment import CommentCreate, CommentUpdate
from app.models.comment import Comment


class CommentService:
    def __init__(self, db: Session):
        self.repo = CommentRepository(db)

    def _assert_entities(self, user_id: int, startup_id: int):
        user_exists = self.repo.db.execute(text("SELECT 1 FROM `User` WHERE user_id=:uid"), {"uid": user_id}).fetchone()
        startup_exists = self.repo.db.execute(text("SELECT 1 FROM Startup WHERE startup_id=:sid"), {"sid": startup_id}).fetchone()
        if not user_exists:
            raise ValueError("User not found")
        if not startup_exists:
            raise ValueError("Startup not found")

    def create(self, user_id: int, payload: CommentCreate) -> dict:  # MODIFICADO: retornar dict
        self._assert_entities(user_id, payload.startup_id)
        comment = self.repo.create(user_id=user_id, content=payload.content, startup_id=payload.startup_id)

        # Obtener el nombre del usuario para el comentario creado
        user = self.repo.db.execute(
            text("SELECT first_name, last_name FROM `User` WHERE user_id=:uid"),
            {"uid": user_id}
        ).fetchone()

        user_name = f"{user.first_name} {user.last_name}" if user else f"Usuario {user_id}"

        return {
            "comment_id": comment.comment_id,
            "content": comment.content,
            "created_date": comment.created_date,
            "modified_date": comment.modified_date,
            "user_id": comment.user_id,
            "startup_id": comment.startup_id,
            "user_name": user_name
        }

    def list(self, startup_id: int | None, *, skip: int = 0, limit: int = 50):
        if startup_id is None:
            return self.repo.list_all(skip=skip, limit=limit)
        return self.repo.list_by_startup(startup_id, skip=skip, limit=limit)

    def update(self, comment_id: int, user_id: int, payload: CommentUpdate) -> dict:  # MODIFICADO: retornar dict
        comment = self.repo.get(comment_id)
        if not comment:
            raise ValueError("Comment not found")
        if comment.user_id != user_id:
            raise PermissionError("Cannot modify another user's comment")
        self._assert_entities(user_id, comment.startup_id)
        updated_comment = self.repo.update(comment, payload.content)

        # Obtener el nombre del usuario
        user = self.repo.db.execute(
            text("SELECT first_name, last_name FROM `User` WHERE user_id=:uid"),
            {"uid": user_id}
        ).fetchone()

        user_name = f"{user.first_name} {user.last_name}" if user else f"Usuario {user_id}"

        return {
            "comment_id": updated_comment.comment_id,
            "content": updated_comment.content,
            "created_date": updated_comment.created_date,
            "modified_date": updated_comment.modified_date,
            "user_id": updated_comment.user_id,
            "startup_id": updated_comment.startup_id,
            "user_name": user_name
        }

    def delete(self, comment_id: int, user_id: int) -> None:
        comment = self.repo.get(comment_id)
        if not comment:
            raise ValueError("Comment not found")
        if comment.user_id != user_id:
            raise PermissionError("Cannot delete another user's comment")
        self._assert_entities(user_id, comment.startup_id)
        self.repo.delete(comment)