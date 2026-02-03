from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ZoneBase(BaseModel):
    """Base zone schema."""
    title: str
    description: Optional[str] = None
    order_index: int = 0


class ZoneCreate(ZoneBase):
    """Schema for creating a zone."""
    world_id: int
    is_locked: bool = True
    unlock_requirement_xp: int = 0


class ZoneUpdate(BaseModel):
    """Schema for updating a zone."""
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    is_locked: Optional[bool] = None
    unlock_requirement_xp: Optional[int] = None


class ZoneResponse(ZoneBase):
    """Schema for zone response."""
    zone_id: int
    world_id: int
    is_locked: bool
    unlock_requirement_xp: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuestSummary(BaseModel):
    """Brief quest info for zone details."""
    quest_id: int
    title: str
    order_index: int
    xp_reward: int
    gold_reward: int
    
    class Config:
        from_attributes = True


class ZoneWithQuests(ZoneResponse):
    """Zone with its quests."""
    quests: List[QuestSummary] = []
    
    class Config:
        from_attributes = True
