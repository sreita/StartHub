from sqlalchemy import Column, Integer, String, ForeignKey
from backend.db.base import Base


class Startup(Base):
    __tablename__ = "Startup"

    startup_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    owner_user_id = Column(Integer, ForeignKey("User.user_id"))
    category_id = Column(Integer)
