from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, func
import enum
from app.db.base import Base


class VoteType(str, enum.Enum):
    upvote = "upvote"
    downvote = "downvote"


class Vote(Base):
    __tablename__ = "Vote"

    vote_id = Column(Integer, primary_key=True, index=True)
    vote_type = Column(Enum(VoteType), nullable=False, index=True)
    created_date = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("User.user_id", ondelete="CASCADE"), nullable=False, index=True)
    startup_id = Column(Integer, ForeignKey("Startup.startup_id", ondelete="CASCADE"), nullable=False, index=True)
