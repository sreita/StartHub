from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    
    # We will assume a simple integer ID for the author from the users service.
    # In a real microservices architecture, you might not use a direct foreign key,
    # but this simplifies the initial setup.
    author_id = Column(Integer, nullable=False)
    
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # If you had a local User model, you could define a relationship:
    # author = relationship("User")
