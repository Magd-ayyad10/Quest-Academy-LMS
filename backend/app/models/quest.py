from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Quest(Base):
    """Quest model - The Lessons within Zones."""
    
    __tablename__ = "quests"
    
    quest_id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("zones.zone_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content_url = Column(Text)
    xp_reward = Column(Integer, default=0, nullable=False)
    gold_reward = Column(Integer, default=10, nullable=False)
    ai_narrative_prompt = Column(Text)
    order_index = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    zone = relationship("Zone", back_populates="quests")
    monsters = relationship("Monster", back_populates="quest", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="quest", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="quest", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Quest {self.title}>"
