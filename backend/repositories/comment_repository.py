from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.models.comment import Comment


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
            select(Comment)
            .where(Comment.startup_id == startup_id)
            .order_by(Comment.created_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.db.execute(stmt).scalars().all()

    def list_all(self, *, skip: int = 0, limit: int = 50):
        stmt = select(Comment).order_by(Comment.created_date.desc()).offset(skip).limit(limit)
        return self.db.execute(stmt).scalars().all()

    def get(self, comment_id: int) -> Comment | None:
        return self.db.get(Comment, comment_id)

    def update(self, comment: Comment, content: str) -> Comment:
        from datetime import datetime, timezone

        comment.content = content
        # Use timezone-aware UTC then store as naive UTC to avoid deprecation
        comment.modified_date = datetime.now(timezone.utc).replace(tzinfo=None)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment: Comment) -> None:
        self.db.delete(comment)
        self.db.commit()
