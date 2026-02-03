from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SystemStats(BaseModel):
    total_users: int
    total_teachers: int
    total_worlds: int
    total_quests: int
    total_monsters: int
    total_items: int

class AdminUserView(BaseModel):
    user_id: int
    username: str
    email: str
    avatar_class: str
    level: int
    current_xp: int
    gold: int
    created_at: datetime
    
class AdminWorldView(BaseModel):
    world_id: int
    title: str
    description: Optional[str]
    is_published: bool
    teacher_id: Optional[int]
    zone_count: int
    quest_count: int
    created_at: datetime

class GlobalActivityView(BaseModel):
    id: int
    username: str
    activity_type: str
    title: str
    xp_earned: int
    created_at: datetime

class AdminDashboardData(BaseModel):
    stats: SystemStats
    recent_users: List[AdminUserView]
    recent_worlds: List[AdminWorldView]
    recent_activity: List[GlobalActivityView]
