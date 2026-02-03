from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class SubmissionStatus(str, enum.Enum):
    """Enum for submission status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Submission(Base):
    """Submission model - The Contract Fulfillment."""
    
    __tablename__ = "submissions"
    
    submission_id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    submission_url = Column(Text)
    submission_text = Column(Text)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.PENDING, nullable=False)
    teacher_feedback = Column(Text)
    grade_awarded = Column(Integer)
    submitted_at = Column(DateTime, server_default=func.now())
    graded_at = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint("user_id", "assignment_id", name="uq_user_assignment_submission"),
    )
    
    # Relationships
    assignment = relationship("Assignment", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
    
    @property
    def username(self):
        return self.user.username if self.user else "Unknown Hero"

    def __repr__(self):
        return f"<Submission {self.submission_id} - {self.status}>"
