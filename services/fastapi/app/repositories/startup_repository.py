from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.models.startup import Startup
from app.models.comment import Comment
from app.models.vote import Vote
from app.models.category import Category
from app.models.user import User  # IMPORTAR USER


class StartupRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, startup: Startup) -> Startup:
        self.db.add(startup)
        self.db.commit()
        self.db.refresh(startup)
        return startup

    def get_by_id(self, startup_id: int) -> Optional[Startup]:
        result = self.db.query(
            Startup,
            Category.name.label('category_name'),
            User.first_name,
            User.last_name
        )\
            .join(Category, Startup.category_id == Category.category_id)\
            .join(User, Startup.owner_user_id == User.user_id)\
            .filter(Startup.startup_id == startup_id)\
            .first()

        if result:
            startup, category_name, first_name, last_name = result
            # Asignar el nombre de la categoría y del usuario al objeto startup
            setattr(startup, 'category_name', category_name)
            setattr(startup, 'owner_name', f"{first_name} {last_name}")
            return startup
        return None

    def get_by_owner(self, owner_user_id: int) -> List[Startup]:
        results = self.db.query(
            Startup,
            Category.name.label('category_name'),
            User.first_name,
            User.last_name
        )\
            .join(Category, Startup.category_id == Category.category_id)\
            .join(User, Startup.owner_user_id == User.user_id)\
            .filter(Startup.owner_user_id == owner_user_id)\
            .all()

        startups = []
        for startup, category_name, first_name, last_name in results:
            setattr(startup, 'category_name', category_name)
            setattr(startup, 'owner_name', f"{first_name} {last_name}")
            startups.append(startup)
        return startups

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Startup]:
        results = self.db.query(
            Startup,
            Category.name.label('category_name'),
            User.first_name,
            User.last_name
        )\
            .join(Category, Startup.category_id == Category.category_id)\
            .join(User, Startup.owner_user_id == User.user_id)\
            .offset(skip).limit(limit)\
            .all()

        startups = []
        for startup, category_name, first_name, last_name in results:
            setattr(startup, 'category_name', category_name)
            setattr(startup, 'owner_name', f"{first_name} {last_name}")
            startups.append(startup)
        return startups

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
            Category.name.label('category_name'),
            User.first_name,
            User.last_name,
            func.count(Comment.comment_id).label('total_comentarios'),
            func.count(Vote.vote_id).label('total_votos')
        )\
         .join(Category, Startup.category_id == Category.category_id)\
         .join(User, Startup.owner_user_id == User.user_id)\
         .outerjoin(Comment, Comment.startup_id == Startup.startup_id)\
         .outerjoin(Vote, Vote.startup_id == Startup.startup_id)\
         .filter(Startup.startup_id == startup_id)\
         .group_by(Startup.startup_id, Category.name, User.first_name, User.last_name)\
         .first()

        if result:
            startup, category_name, first_name, last_name, total_comentarios, total_votos = result
            setattr(startup, 'category_name', category_name)
            setattr(startup, 'owner_name', f"{first_name} {last_name}")
            return (startup, total_comentarios, total_votos)
        return None

    def exists(self, startup_id: int) -> bool:
        return self.db.query(Startup).filter(Startup.startup_id == startup_id).first() is not None

    def get_categories(self) -> List[Category]:
        return self.db.query(Category).all()