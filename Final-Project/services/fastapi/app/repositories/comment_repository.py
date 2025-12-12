from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.comment import Comment
from app.models.user import User  # NUEVA IMPORTACIÓN


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, user_id: int, content: str, startup_id: int) -> Comment:
        comment = Comment(user_id=user_id, content=content, startup_id=startup_id)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def list_by_startup(self, startup_id: int, *, skip: int = 0, limit: int = 50):
        stmt = (
            select(Comment, User.first_name, User.last_name)  # MODIFICADO: incluir nombre y apellido
            .join(User, Comment.user_id == User.user_id)      # NUEVO: JOIN con User
            .where(Comment.startup_id == startup_id)
            .order_by(Comment.created_date.desc())
            .offset(skip)
            .limit(limit)
        )
        results = self.db.execute(stmt).all()

        # Convertir resultados a formato adecuado
        comments_with_users = []
        for comment, first_name, last_name in results:
            comment_dict = {
                "comment_id": comment.comment_id,
                "content": comment.content,
                "created_date": comment.created_date,
                "modified_date": comment.modified_date,
                "user_id": comment.user_id,
                "startup_id": comment.startup_id,
                "user_name": f"{first_name} {last_name}"  # Combinar nombre y apellido
            }
            comments_with_users.append(comment_dict)

        return comments_with_users

    def list_all(self, *, skip: int = 0, limit: int = 50):
        stmt = (
            select(Comment, User.first_name, User.last_name)  # MODIFICADO
            .join(User, Comment.user_id == User.user_id)      # NUEVO: JOIN con User
            .order_by(Comment.created_date.desc())
            .offset(skip)
            .limit(limit)
        )
        results = self.db.execute(stmt).all()

        # Convertir resultados a formato adecuado
        comments_with_users = []
        for comment, first_name, last_name in results:
            comment_dict = {
                "comment_id": comment.comment_id,
                "content": comment.content,
                "created_date": comment.created_date,
                "modified_date": comment.modified_date,
                "user_id": comment.user_id,
                "startup_id": comment.startup_id,
                "user_name": f"{first_name} {last_name}"  # Combinar nombre y apellido
            }
            comments_with_users.append(comment_dict)

        return comments_with_users

    def get(self, comment_id: int) -> Comment | None:
        return self.db.get(Comment, comment_id)

    def update(self, comment: Comment, content: str) -> Comment:
        from datetime import datetime, timezone

        comment.content = content
        comment.modified_date = datetime.now(timezone.utc).replace(tzinfo=None)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment: Comment) -> None:
        self.db.delete(comment)
        self.db.commit()