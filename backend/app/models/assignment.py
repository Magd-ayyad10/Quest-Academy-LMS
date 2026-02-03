from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Assignment(Base):
    """Assignment model - The Bounties (manual tasks)."""
    
    __tablename__ = "assignments"
    
    assignment_id = Column(Integer, primary_key=True, index=True)
    quest_id = Column(Integer, ForeignKey("quests.quest_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    max_score = Column(Integer, default=100, nullable=False)
    xp_reward = Column(Integer, default=0, nullable=False)
    gold_reward = Column(Integer, default=0, nullable=False)
    due_date = Column(DateTime)
    required_class = Column(String(50), default="All", nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    quest = relationship("Quest", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Assignment {self.title}>"
