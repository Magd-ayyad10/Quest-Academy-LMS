from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str
    avatar_class: Optional[str] = "Novice"


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_class: Optional[str] = None
    avatar_url: Optional[str] = None


class UserStats(BaseModel):
    """Schema for user RPG stats."""
    level: int
    current_xp: int
    hp_current: int
    hp_max: int
    gold: int
    avatar_class: str
    title: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    user_id: int
    level: int
    current_xp: int
    hp_current: int
    hp_max: int
    gold: int
    avatar_class: str
    avatar_url: Optional[str] = None
    title: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserWithStats(UserResponse):
    """Schema for user with detailed stats."""
    quests_completed: Optional[int] = 0
    achievements_unlocked: Optional[int] = 0
    
    class Config:
        from_attributes = True
