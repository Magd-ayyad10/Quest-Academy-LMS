from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class QuizQuestion(Base):
    """
    QuizQuestion model - Individual questions for Monster Battles.
    Replaces the single-question logic in the Monster table.
    """
    __tablename__ = "quiz_questions"

    question_id = Column(Integer, primary_key=True, index=True)
    monster_id = Column(Integer, ForeignKey("monsters.monster_id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    wrong_answers = Column(JSON, nullable=False) # Stores array of strings
    xp_value = Column(Integer, default=10)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship
    monster = relationship("Monster", back_populates="questions")
