from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.achievement import Achievement, UserAchievement
from app.models.user import User
from app.schemas.achievement import AchievementResponse, UserAchievementResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/achievements", tags=["Achievements (Trophies)"])


@router.get("/", response_model=List[AchievementResponse])
async def get_all_achievements(
    db: Session = Depends(get_db)
):
    """
    Get all available achievements.
    """
    achievements = db.query(Achievement).all()
    return achievements


@router.get("/my", response_model=List[UserAchievementResponse])
async def get_my_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's unlocked achievements.
    """
    user_achievements = db.query(UserAchievement).filter(
        UserAchievement.user_id == current_user.user_id
    ).all()
    
    return user_achievements


@router.get("/progress")
async def get_achievement_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get progress towards all achievements.
    """
    from app.models.progress import UserProgress
    
    # Get all achievements
    all_achievements = db.query(Achievement).all()
    
    # Get user's unlocked achievement IDs
    unlocked_ids = [ua.achievement_id for ua in current_user.achievements]
    
    # Count user stats
    quests_completed = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.user_id,
        UserProgress.is_completed == True
    ).count()
    
    perfect_scores = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.user_id,
        UserProgress.score == 100
    ).count()
    
    items_owned = len(current_user.inventory)
    
    progress_list = []
    
    for achievement in all_achievements:
        is_unlocked = achievement.achievement_id in unlocked_ids
        current_value = 0
        
        # Calculate current value based on achievement type
        if achievement.achievement_type.value == "quest":
            current_value = quests_completed
        elif achievement.achievement_type.value == "combat":
            if "perfect" in achievement.name.lower():
                current_value = perfect_scores
            else:
                current_value = quests_completed  # Simplified
        elif achievement.achievement_type.value == "collection":
            if "gold" in achievement.name.lower():
                current_value = current_user.gold
            else:
                current_value = items_owned
        
        progress_list.append({
            "achievement_id": achievement.achievement_id,
            "name": achievement.name,
            "description": achievement.description,
            "is_unlocked": is_unlocked,
            "current_value": current_value,
            "required_value": achievement.requirement_value,
            "progress_percent": min(100, (current_value / achievement.requirement_value * 100)) if achievement.requirement_value > 0 else 0
        })
    
    return {
        "total_achievements": len(all_achievements),
        "unlocked_count": len(unlocked_ids),
        "achievements": progress_list
    }
