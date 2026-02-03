from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class TeacherBase(BaseModel):
    """Base teacher schema."""
    username: str
    email: EmailStr


class TeacherCreate(TeacherBase):
    """Schema for teacher registration."""
    password: str
    bio: Optional[str] = None
    specialization: Optional[str] = None


class TeacherUpdate(BaseModel):
    """Schema for updating teacher profile."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    specialization: Optional[str] = None


class TeacherResponse(TeacherBase):
    """Schema for teacher response."""
    teacher_id: int
    bio: Optional[str] = None
    specialization: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
