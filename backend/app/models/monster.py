from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Monster(Base):
    """Monster model - The Quizzes that guard Quests."""
    
    __tablename__ = "monsters"
    
    monster_id = Column(Integer, primary_key=True, index=True)
    quest_id = Column(Integer, ForeignKey("quests.quest_id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    question_text = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    wrong_options = Column(ARRAY(Text), nullable=False)
    damage_per_wrong_answer = Column(Integer, default=10, nullable=False)
    monster_hp = Column(Integer, default=100)
    monster_image_url = Column(Text)
    
    # RPG Mechanics
    entry_cost = Column(Integer, default=0, nullable=False)
    pass_reward = Column(Integer, default=30, nullable=False)
    fail_penalty = Column(Integer, default=5, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    quest = relationship("Quest", back_populates="monsters")
    questions = relationship("QuizQuestion", back_populates="monster", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Monster {self.name}>"
