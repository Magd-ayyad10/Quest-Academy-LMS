from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class AIGradingLog(Base):
    """
    Log of AI grading operations for assignments.
    Stores the user email explicitly as requested.
    """
    __tablename__ = "ai_grading_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.submission_id"), nullable=False, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    # Store user email explicitly for quick list/notification access as requested
    user_email = Column(String(255), nullable=False, index=True)
    
    # AI Grading Details
    score_awarded = Column(Integer, nullable=False)
    feedback_text = Column(Text, nullable=True)
    status_verdict = Column(String(50), nullable=False) # approved, rejected
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    submission = relationship("Submission")
    assignment = relationship("Assignment")
    user = relationship("User")
