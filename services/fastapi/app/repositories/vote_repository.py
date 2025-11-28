from sqlalchemy.orm import Session
from sqlalchemy import select, func, case
from app.models.vote import Vote, VoteType


class VoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, *, user_id: int, startup_id: int, vote_type: VoteType) -> tuple[Vote, bool]:
        """Upsert del voto. Retorna (voto, creado_bool)."""
        stmt = select(Vote).where(Vote.user_id == user_id, Vote.startup_id == startup_id)
        existing = self.db.execute(stmt).scalar_one_or_none()
        if existing:
            existing.vote_type = vote_type
            self.db.commit()
            self.db.refresh(existing)
            return existing, False
        vote = Vote(user_id=user_id, startup_id=startup_id, vote_type=vote_type)
        self.db.add(vote)
        self.db.commit()
        self.db.refresh(vote)
        return vote, True

    def count_for_startup(self, startup_id: int) -> tuple[int, int]:
        up_case = case((Vote.vote_type == VoteType.upvote, 1), else_=0)
        down_case = case((Vote.vote_type == VoteType.downvote, 1), else_=0)
        stmt = select(func.sum(up_case), func.sum(down_case)).where(Vote.startup_id == startup_id)
        upvotes, downvotes = self.db.execute(stmt).one()
        return int(upvotes or 0), int(downvotes or 0)

    def delete(self, *, user_id: int, startup_id: int) -> bool:
        stmt = select(Vote).where(Vote.user_id == user_id, Vote.startup_id == startup_id)
        existing = self.db.execute(stmt).scalar_one_or_none()
        if not existing:
            return False
        self.db.delete(existing)
        self.db.commit()
        return True
