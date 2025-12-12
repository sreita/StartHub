from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255))
    password_hash = Column(String(255))
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_enabled = Column(Boolean, default=False)
