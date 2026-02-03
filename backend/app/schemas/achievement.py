from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from app.schemas.item import ItemRarity


class AchievementType(str, Enum):
    """Enum for achievement types."""
    QUEST = "quest"
    COMBAT = "combat"
    SOCIAL = "social"
    COLLECTION = "collection"
    MASTERY = "mastery"


class AchievementResponse(BaseModel):
    """Schema for achievement response."""
    achievement_id: int
    name: str
    description: str
    achievement_type: AchievementType
    icon_url: Optional[str] = None
    requirement_value: int
    requirement_description: Optional[str] = None
    xp_reward: int
    gold_reward: int
    title_reward: Optional[str] = None
    rarity: ItemRarity
    
    class Config:
        from_attributes = True


class UserAchievementResponse(BaseModel):
    """Schema for user achievement response."""
    user_achievement_id: int
    user_id: int
    achievement: AchievementResponse
    unlocked_at: datetime
    
    class Config:
        from_attributes = True
