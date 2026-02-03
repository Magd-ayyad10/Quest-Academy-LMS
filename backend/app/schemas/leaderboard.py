from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class LeaderboardEntryResponse(BaseModel):
    """Schema for leaderboard entry response."""
    entry_id: int
    user_id: int
    username: str
    avatar_class: str
    world_id: Optional[int] = None
    total_xp: int
    total_gold: int
    quests_completed: int
    monsters_defeated: int
    achievements_unlocked: int
    rank_position: Optional[int] = None
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    
    class Config:
        from_attributes = True


class LeaderboardQuery(BaseModel):
    """Schema for querying leaderboard."""
    world_id: Optional[int] = None  # None = global
    limit: int = 10
    offset: int = 0
