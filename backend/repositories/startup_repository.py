from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from backend.models.startup import Startup
from backend.models.comment import Comment
from backend.models.vote import Vote


class StartupRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, startup: Startup) -> Startup:
        self.db.add(startup)
        self.db.commit()
        self.db.refresh(startup)
        return startup

    def get_by_id(self, startup_id: int) -> Optional[Startup]:
        return self.db.query(Startup).filter(Startup.startup_id == startup_id).first()

    def get_by_owner(self, owner_user_id: int) -> List[Startup]:
        return self.db.query(Startup).filter(Startup.owner_user_id == owner_user_id).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Startup]:
        return self.db.query(Startup).offset(skip).limit(limit).all()

    def update(self, startup_id: int, update_data: dict) -> Optional[Startup]:
        startup = self.get_by_id(startup_id)
        if startup:
            for key, value in update_data.items():
                setattr(startup, key, value)
            self.db.commit()
            self.db.refresh(startup)
        return startup

    def delete(self, startup_id: int) -> bool:
        startup = self.get_by_id(startup_id)
        if startup:
            self.db.delete(startup)
            self.db.commit()
            return True
        return False

    def get_with_stats(self, startup_id: int) -> Optional[tuple]:
        """Obtiene startup con estadísticas de votos y comentarios"""
        result = self.db.query(
            Startup,
            func.count(Comment.comment_id).label('total_comentarios'),
            func.count(Vote.vote_id).label('total_votos')
        ).outerjoin(Comment, Comment.startup_id == Startup.startup_id)\
         .outerjoin(Vote, Vote.startup_id == Startup.startup_id)\
         .filter(Startup.startup_id == startup_id)\
         .group_by(Startup.startup_id)\
         .first()
        
        return result

    def exists(self, startup_id: int) -> bool:
        return self.db.query(Startup).filter(Startup.startup_id == startup_id).first() is not None