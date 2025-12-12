from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Startup(Base):
    __tablename__ = "Startup"

    startup_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    email = Column(String(255))
    website = Column(String(255))
    social_media = Column(String(255))
    created_date = Column(DateTime, default=datetime.utcnow)
    owner_user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("Category.category_id"), nullable=False)

    # Usar relación por cadena para evitar problemas de importación
    category = relationship("Category", backref="startups", lazy="joined")