"""
Engagement API Router - Daily Quests, Streaks, Activity, Weekly Goals
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models import (
    User, DailyQuest, UserDailyQuest, UserStreak, 
    UserActivity, WeeklyGoal, UserProgress, Quest, World, Zone,
    DailyQuestType, ActivityType
)

router = APIRouter(prefix="/api/engagement", tags=["engagement"])


# ============ SCHEMAS ============

class DailyQuestResponse(BaseModel):
    quest_id: int
    title: str
    description: Optional[str]
    quest_type: str
    target_value: int
    xp_reward: int
    gold_reward: int
    icon: str
    current_progress: int = 0
    is_completed: bool = False
    
    class Config:
        from_attributes = True


class StreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[date]
    is_active_today: bool
    
    class Config:
        from_attributes = True


class ActivityResponse(BaseModel):
    id: int
    activity_type: str
    title: str
    description: Optional[str]
    xp_earned: int
    gold_earned: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class WeeklyGoalResponse(BaseModel):
    xp_target: int
    xp_earned: int
    xp_percent: float
    quests_target: int
    quests_completed: int
    quests_percent: float
    battles_target: int
    battles_won: int
    battles_percent: float
    
    class Config:
        from_attributes = True


class SkillProgress(BaseModel):
    world_id: int
    world_title: str
    total_quests: int
    completed_quests: int
    percent: float
    color: str


class ContinueJourneyResponse(BaseModel):
    quest_id: int
    quest_title: str
    zone_title: str
    world_title: str
    world_id: int
    zone_id: int


class DashboardEngagementResponse(BaseModel):
    daily_quests: List[DailyQuestResponse]
    streak: StreakResponse
    recent_activity: List[ActivityResponse]
    weekly_goals: WeeklyGoalResponse
    skills: List[SkillProgress]
    continue_quest: Optional[ContinueJourneyResponse]
    battle_ready: bool
    hp_percent: float


# ============ HELPER FUNCTIONS ============

def get_or_create_streak(db: Session, user_id: int) -> UserStreak:
    """Get or create user streak record."""
    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    if not streak:
        streak = UserStreak(user_id=user_id, current_streak=0, longest_streak=0)
        db.add(streak)
        db.commit()
        db.refresh(streak)
    return streak


def update_streak(db: Session, user_id: int) -> UserStreak:
    """Update user's streak based on activity."""
    streak = get_or_create_streak(db, user_id)
    today = date.today()
    
    if streak.last_activity_date == today:
        # Already logged today
        return streak
    
    if streak.last_activity_date == today - timedelta(days=1):
        # Consecutive day - increment streak
        streak.current_streak += 1
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
    elif streak.last_activity_date is None or streak.last_activity_date < today - timedelta(days=1):
        # Streak broken - reset
        streak.current_streak = 1
        streak.streak_start_date = today
    
    streak.last_activity_date = today
    db.commit()
    db.refresh(streak)
    return streak


def log_activity(db: Session, user_id: int, activity_type: ActivityType, 
                 title: str, description: str = None, xp: int = 0, gold: int = 0, ref_id: int = None):
    """Log a user activity."""
    activity = UserActivity(
        user_id=user_id,
        activity_type=activity_type,
        title=title,
        description=description,
        xp_earned=xp,
        gold_earned=gold,
        reference_id=ref_id
    )
    db.add(activity)
    
    # Update streak
    update_streak(db, user_id)
    
    # Update weekly goals
    update_weekly_progress(db, user_id, activity_type, xp)
    
    db.commit()


def get_or_create_weekly_goal(db: Session, user_id: int) -> WeeklyGoal:
    """Get or create weekly goal for current week."""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Monday
    
    goal = db.query(WeeklyGoal).filter(
        WeeklyGoal.user_id == user_id,
        WeeklyGoal.week_start == week_start
    ).first()
    
    if not goal:
        goal = WeeklyGoal(
            user_id=user_id,
            week_start=week_start,
            xp_target=500,
            quests_target=10,
            battles_target=3
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
    
    return goal


def update_weekly_progress(db: Session, user_id: int, activity_type: ActivityType, xp: int = 0):
    """Update weekly goal progress."""
    goal = get_or_create_weekly_goal(db, user_id)
    
    goal.xp_earned += xp
    
    if activity_type == ActivityType.QUEST_COMPLETE:
        goal.quests_completed += 1
    elif activity_type == ActivityType.BATTLE_WON:
        goal.battles_won += 1
    
    db.commit()


def get_world_color(title: str) -> str:
    """Get theme color for a world."""
    lower = title.lower()
    if 'python' in lower: return '#10b981'
    if 'sql' in lower: return '#3b82f6'
    if 'git' in lower: return '#8b5cf6'
    if 'javascript' in lower or 'js' in lower: return '#f59e0b'
    if 'c++' in lower: return '#3178c6'
    if 'java' in lower: return '#f89820'
    if 'ai' in lower: return '#ef4444'
    return '#8b5cf6'


# ============ ENDPOINTS ============

@router.get("/dashboard", response_model=DashboardEngagementResponse)
async def get_dashboard_engagement(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all engagement data for dashboard."""
    today = date.today()
    
    # 1. Daily Quests
    daily_quests = db.query(DailyQuest).filter(DailyQuest.is_active == True).limit(3).all()
    
    # SEED DEFAULT QUESTS IF NONE EXIST
    if not daily_quests:
        default_quests = [
            DailyQuest(title="Scholar's Path", description="Complete 1 Lesson", quest_type="complete_lesson", target_value=1, xp_reward=50, gold_reward=20, icon="📚"),
            DailyQuest(title="Gladiator", description="Win 1 Battle", quest_type="win_battle", target_value=1, xp_reward=75, gold_reward=30, icon="⚔️"),
            DailyQuest(title="Treasure Hunter", description="Earn 100 XP", quest_type="earn_xp", target_value=100, xp_reward=50, gold_reward=20, icon="⭐")
        ]
        db.add_all(default_quests)
        db.commit()
        daily_quests = db.query(DailyQuest).filter(DailyQuest.is_active == True).limit(3).all()
    
    daily_quest_responses = []
    
    for dq in daily_quests:
        user_progress = db.query(UserDailyQuest).filter(
            UserDailyQuest.user_id == current_user.user_id,
            UserDailyQuest.daily_quest_id == dq.quest_id,
            UserDailyQuest.date == today
        ).first()
        
        daily_quest_responses.append(DailyQuestResponse(
            quest_id=dq.quest_id,
            title=dq.title,
            description=dq.description,
            quest_type=dq.quest_type,
            target_value=dq.target_value,
            xp_reward=dq.xp_reward,
            gold_reward=dq.gold_reward,
            icon=dq.icon,
            current_progress=user_progress.current_progress if user_progress else 0,
            is_completed=user_progress.is_completed if user_progress else False
        ))
    
    # 2. Streak
    streak = update_streak(db, current_user.user_id)
    streak_response = StreakResponse(
        current_streak=streak.current_streak,
        longest_streak=streak.longest_streak,
        last_activity_date=streak.last_activity_date,
        is_active_today=streak.last_activity_date == today
    )
    
    # 3. Recent Activity
    activities = db.query(UserActivity).filter(
        UserActivity.user_id == current_user.user_id
    ).order_by(UserActivity.created_at.desc()).limit(5).all()
    
    activity_responses = [
        ActivityResponse(
            id=a.id,
            activity_type=a.activity_type,
            title=a.title,
            description=a.description,
            xp_earned=a.xp_earned,
            gold_earned=a.gold_earned,
            created_at=a.created_at
        ) for a in activities
    ]
    
    # 4. Weekly Goals
    weekly = get_or_create_weekly_goal(db, current_user.user_id)
    weekly_response = WeeklyGoalResponse(
        xp_target=weekly.xp_target,
        xp_earned=weekly.xp_earned,
        xp_percent=min(100, (weekly.xp_earned / weekly.xp_target) * 100) if weekly.xp_target > 0 else 0,
        quests_target=weekly.quests_target,
        quests_completed=weekly.quests_completed,
        quests_percent=min(100, (weekly.quests_completed / weekly.quests_target) * 100) if weekly.quests_target > 0 else 0,
        battles_target=weekly.battles_target,
        battles_won=weekly.battles_won,
        battles_percent=min(100, (weekly.battles_won / weekly.battles_target) * 100) if weekly.battles_target > 0 else 0
    )
    
    # 5. Skills Progress
    worlds = db.query(World).filter(World.is_published == True).all()
    skills = []
    
    for world in worlds:
        total_quests = db.query(Quest).join(Zone).filter(Zone.world_id == world.world_id).count()
        completed = db.query(UserProgress).join(Quest).join(Zone).filter(
            Zone.world_id == world.world_id,
            UserProgress.user_id == current_user.user_id,
            UserProgress.is_completed == True
        ).count()
        
        skills.append(SkillProgress(
            world_id=world.world_id,
            world_title=world.title,
            total_quests=total_quests,
            completed_quests=completed,
            percent=round((completed / total_quests) * 100, 1) if total_quests > 0 else 0,
            color=get_world_color(world.title)
        ))
    
    # 6. Continue Journey - Find last incomplete quest
    last_progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.user_id
    ).order_by(UserProgress.updated_at.desc()).first()
    
    continue_quest = None
    if last_progress:
        # Find next quest in same zone
        current_quest = db.query(Quest).filter(Quest.quest_id == last_progress.quest_id).first()
        if current_quest:
            next_quest = db.query(Quest).filter(
                Quest.zone_id == current_quest.zone_id,
                Quest.order_index > current_quest.order_index
            ).order_by(Quest.order_index).first()
            
            if next_quest:
                zone = db.query(Zone).filter(Zone.zone_id == next_quest.zone_id).first()
                world = db.query(World).filter(World.world_id == zone.world_id).first() if zone else None
                
                if zone and world:
                    continue_quest = ContinueJourneyResponse(
                        quest_id=next_quest.quest_id,
                        quest_title=next_quest.title,
                        zone_title=zone.title,
                        world_title=world.title,
                        world_id=world.world_id,
                        zone_id=zone.zone_id
                    )
    
    # 7. Battle Ready
    hp_percent = (current_user.hp_current / current_user.hp_max) * 100 if current_user.hp_max > 0 else 100
    battle_ready = hp_percent >= 50
    
    return DashboardEngagementResponse(
        daily_quests=daily_quest_responses,
        streak=streak_response,
        recent_activity=activity_responses,
        weekly_goals=weekly_response,
        skills=skills,
        continue_quest=continue_quest,
        battle_ready=battle_ready,
        hp_percent=hp_percent
    )


@router.get("/leaderboard/mini")
async def get_mini_leaderboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get mini leaderboard (top 5 + current user)."""
    from app.models import LeaderboardEntry
    
    # Get top 5
    top_entries = db.query(LeaderboardEntry, User).join(User).order_by(
        LeaderboardEntry.total_xp.desc()
    ).limit(5).all()
    
    top_5 = []
    for entry, user in top_entries:
        top_5.append({
            "rank": len(top_5) + 1,
            "username": user.username,
            "avatar_class": user.avatar_class,
            "total_xp": entry.total_xp,
            "level": user.level,
            "is_current_user": user.user_id == current_user.user_id
        })
    
    # Get current user's rank if not in top 5
    user_in_top = any(u["is_current_user"] for u in top_5)
    current_rank = None
    
    if not user_in_top:
        user_entry = db.query(LeaderboardEntry).filter(
            LeaderboardEntry.user_id == current_user.user_id
        ).first()
        
        if user_entry:
            rank = db.query(LeaderboardEntry).filter(
                LeaderboardEntry.total_xp > user_entry.total_xp
            ).count() + 1
            
            current_rank = {
                "rank": rank,
                "username": current_user.username,
                "avatar_class": current_user.avatar_class,
                "total_xp": user_entry.total_xp,
                "level": current_user.level,
                "is_current_user": True
            }
    
    return {
        "top_5": top_5,
        "current_user": current_rank
    }


@router.post("/activity/log")
async def log_user_activity(
    activity_type: str,
    title: str,
    xp: int = 0,
    gold: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually log an activity (for internal use)."""
    try:
        act_type = ActivityType(activity_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid activity type")
    
    log_activity(db, current_user.user_id, act_type, title, xp=xp, gold=gold)
    
    return {"status": "logged"}
