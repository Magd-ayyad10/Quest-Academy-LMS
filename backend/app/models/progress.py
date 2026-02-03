from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class UserProgress(Base):
    """UserProgress model - The Save File."""
    
    __tablename__ = "user_progress"
    
    progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    quest_id = Column(Integer, ForeignKey("quests.quest_id", ondelete="CASCADE"), nullable=False, index=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    score = Column(Integer, default=0)
    attempts = Column(Integer, default=0)
    completed_at = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint("user_id", "quest_id", name="uq_user_quest_progress"),
    )
    
    # Relationships
    user = relationship("User", back_populates="progress")
    quest = relationship("Quest", back_populates="progress")
    
    def __repr__(self):
        return f"<UserProgress User:{self.user_id} Quest:{self.quest_id}>"
