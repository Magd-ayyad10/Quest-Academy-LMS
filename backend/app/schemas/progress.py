from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProgressResponse(BaseModel):
    """Schema for user progress response."""
    progress_id: int
    user_id: int
    quest_id: int
    is_completed: bool
    score: int
    attempts: int
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProgressUpdate(BaseModel):
    """Schema for updating progress."""
    is_completed: Optional[bool] = None
    score: Optional[int] = None
