from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AssignmentBase(BaseModel):
    """Base assignment schema."""
    title: str
    description: Optional[str] = None
    max_score: int = 100
    xp_reward: int = 0
    gold_reward: int = 0
    required_class: Optional[str] = "All"


class AssignmentCreate(AssignmentBase):
    """Schema for creating an assignment."""
    quest_id: int
    due_date: Optional[datetime] = None


class AssignmentUpdate(BaseModel):
    """Schema for updating an assignment."""
    title: Optional[str] = None
    description: Optional[str] = None
    max_score: Optional[int] = None
    xp_reward: Optional[int] = None
    gold_reward: Optional[int] = None
    due_date: Optional[datetime] = None
    required_class: Optional[str] = None


class AssignmentResponse(AssignmentBase):
    """Schema for assignment response."""
    assignment_id: int
    quest_id: int
    due_date: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
