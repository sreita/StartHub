from sqlalchemy.orm import Session
from app.repositories.vote_repository import VoteRepository
from app.schemas.vote import VoteCreate, VoteCount
from app.models.vote import Vote
from sqlalchemy import text


class VoteService:
    def __init__(self, db: Session):
        self.repo = VoteRepository(db)

    def _assert_entities(self, user_id: int, startup_id: int):
        # Validar que existan User y Startup (evita FK silenciosa o 500).
        user_exists = self.repo.db.execute(text("SELECT 1 FROM `User` WHERE user_id=:uid"), {"uid": user_id}).fetchone()
        startup_exists = self.repo.db.execute(text("SELECT 1 FROM Startup WHERE startup_id=:sid"), {"sid": startup_id}).fetchone()
        if not user_exists:
            raise ValueError("User not found")
        if not startup_exists:
            raise ValueError("Startup not found")

    def upsert(self, user_id: int, payload: VoteCreate) -> tuple[Vote, bool]:
        self._assert_entities(user_id, payload.startup_id)
        return self.repo.upsert(user_id=user_id, startup_id=payload.startup_id, vote_type=payload.vote_type)

    def count(self, startup_id: int) -> VoteCount:
        up, down = self.repo.count_for_startup(startup_id)
        return VoteCount(startup_id=startup_id, upvotes=up, downvotes=down)

    def delete(self, user_id: int, startup_id: int) -> None:
        self._assert_entities(user_id, startup_id)
        ok = self.repo.delete(user_id=user_id, startup_id=startup_id)
        if not ok:
            raise ValueError("Vote not found")
    def get_user_votes(self, user_id: int) -> list[Vote]:
        return self.repo.get_by_user(user_id)
