from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class World(Base):
    """World model - The Courses of Quest Academy."""
    
    __tablename__ = "worlds"
    
    world_id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id", ondelete="CASCADE"), index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    difficulty_level = Column(String(50), default="Easy", nullable=False)
    theme_prompt = Column(Text)
    thumbnail_url = Column(Text)
    icon = Column(String(10), default="🌍")  # Emoji icon for the world
    is_published = Column(Boolean, default=False)
    required_class = Column(String(50), default="All", nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    teacher = relationship("Teacher", back_populates="worlds")
    zones = relationship("Zone", back_populates="world", cascade="all, delete-orphan")
    leaderboard_entries = relationship("LeaderboardEntry", back_populates="world", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<World {self.title}>"
