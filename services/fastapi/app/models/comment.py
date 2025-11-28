from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from app.db.base import Base


class Comment(Base):
    __tablename__ = "Comment"

    comment_id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_date = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    modified_date = Column(DateTime(timezone=False), nullable=True)
    user_id = Column(Integer, ForeignKey("User.user_id", ondelete="CASCADE"), nullable=False, index=True)
    startup_id = Column(Integer, ForeignKey("Startup.startup_id", ondelete="CASCADE"), nullable=False, index=True)
