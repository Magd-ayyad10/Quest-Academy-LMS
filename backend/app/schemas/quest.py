from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class QuestBase(BaseModel):
    """Base quest schema."""
    title: str
    content_url: Optional[str] = None
    xp_reward: int = 0
    gold_reward: int = 0


class QuestCreate(QuestBase):
    """Schema for creating a quest."""
    zone_id: int
    ai_narrative_prompt: Optional[str] = None
    order_index: int = 0


class QuestUpdate(BaseModel):
    """Schema for updating a quest."""
    title: Optional[str] = None
    content_url: Optional[str] = None
    xp_reward: Optional[int] = None
    gold_reward: Optional[int] = None
    ai_narrative_prompt: Optional[str] = None
    order_index: Optional[int] = None


class AssignmentSummary(BaseModel):
    """Brief assignment info for quest details."""
    assignment_id: int
    title: str
    max_score: int
    
    class Config:
        from_attributes = True


class QuestResponse(QuestBase):
    """Schema for quest response."""
    quest_id: int
    zone_id: int
    ai_narrative_prompt: Optional[str] = None
    order_index: int
    created_at: datetime
    monsters: List['MonsterSummary'] = []
    assignments: List[AssignmentSummary] = []
    
    class Config:
        from_attributes = True


class MonsterSummary(BaseModel):
    """Brief monster info for quest details."""
    monster_id: int
    name: str
    monster_hp: int
    
    class Config:
        from_attributes = True


class QuestWithDetails(QuestResponse):
    """Quest with monsters and assignments."""
    monsters: List[MonsterSummary] = []
    assignments: List[AssignmentSummary] = []
    is_completed: bool = False
    
    class Config:
        from_attributes = True
