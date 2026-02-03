from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Zone(Base):
    """Zone model - The Modules within Worlds."""
    
    __tablename__ = "zones"
    
    zone_id = Column(Integer, primary_key=True, index=True)
    world_id = Column(Integer, ForeignKey("worlds.world_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    order_index = Column(Integer, default=0, nullable=False)
    is_locked = Column(Boolean, default=True, nullable=False)
    unlock_requirement_xp = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    world = relationship("World", back_populates="zones")
    quests = relationship("Quest", back_populates="zone", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Zone {self.title}>"
