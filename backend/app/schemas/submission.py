from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class SubmissionStatus(str, Enum):
    """Enum for submission status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class SubmissionBase(BaseModel):
    """Base submission schema."""
    submission_url: Optional[str] = None
    submission_text: Optional[str] = None


class SubmissionCreate(SubmissionBase):
    """Schema for creating a submission."""
    assignment_id: int


class SubmissionGrade(BaseModel):
    """Schema for grading a submission (teacher only)."""
    status: SubmissionStatus
    grade_awarded: int
    teacher_feedback: Optional[str] = None


class SubmissionResponse(SubmissionBase):
    """Schema for submission response."""
    submission_id: int
    assignment_id: int
    user_id: int
    username: Optional[str] = None
    status: SubmissionStatus
    grade_awarded: Optional[int] = None
    teacher_feedback: Optional[str] = None
    submitted_at: datetime
    graded_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
