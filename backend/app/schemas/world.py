from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class WorldBase(BaseModel):
    """Base world schema."""
    title: str
    description: Optional[str] = None
    difficulty_level: str = "Easy"
    theme_prompt: Optional[str] = None


class WorldCreate(WorldBase):
    """Schema for creating a world."""
    thumbnail_url: Optional[str] = None
    is_published: bool = False
    required_class: Optional[str] = "All"


class WorldUpdate(BaseModel):
    """Schema for updating a world."""
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty_level: Optional[str] = None
    theme_prompt: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_published: Optional[bool] = None


class WorldResponse(WorldBase):
    """Schema for world response."""
    world_id: int
    teacher_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    is_published: bool
    required_class: Optional[str] = "All"
    created_at: datetime
    zones_count: int = 0
    
    class Config:
        from_attributes = True


class ZoneSummary(BaseModel):
    """Brief zone info for world details."""
    zone_id: int
    title: str
    order_index: int
    is_locked: bool
    
    class Config:
        from_attributes = True


class WorldWithZones(WorldResponse):
    """World with its zones."""
    zones: List[ZoneSummary] = []
    
    class Config:
        from_attributes = True
