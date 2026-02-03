from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MonsterBase(BaseModel):
    """Base monster schema."""
    name: str
    question_text: str
    correct_answer: str
    wrong_options: List[str]


class MonsterCreate(MonsterBase):
    """Schema for creating a monster."""
    quest_id: int
    description: Optional[str] = None
    damage_per_wrong_answer: int = 10
    monster_hp: int = 100
    monster_image_url: Optional[str] = None


class MonsterUpdate(BaseModel):
    """Schema for updating a monster."""
    name: Optional[str] = None
    description: Optional[str] = None
    question_text: Optional[str] = None
    correct_answer: Optional[str] = None
    wrong_options: Optional[List[str]] = None
    damage_per_wrong_answer: Optional[int] = None
    monster_hp: Optional[int] = None
    monster_image_url: Optional[str] = None


class MonsterResponse(MonsterBase):
    """Schema for monster response."""
    monster_id: int
    quest_id: int
    description: Optional[str] = None
    damage_per_wrong_answer: int
    monster_hp: int
    monster_image_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class MonsterForBattle(BaseModel):
    """Monster info for battle (hides correct answer)."""
    monster_id: int
    name: str
    description: Optional[str] = None
    question_text: str
    options: List[str]  # Shuffled correct + wrong options
    monster_hp: int
    monster_image_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class BattleRequest(BaseModel):
    """Schema for submitting battle answer."""
    monster_id: int
    selected_answer: str


class BattleResult(BaseModel):
    """Schema for battle result."""
    is_correct: bool
    damage_dealt: int  # Damage to monster (if correct)
    damage_received: int  # Damage to player (if wrong)
    monster_defeated: bool
    xp_earned: int
    gold_earned: int
    player_hp_remaining: int
    monster_hp_remaining: int
    message: str
