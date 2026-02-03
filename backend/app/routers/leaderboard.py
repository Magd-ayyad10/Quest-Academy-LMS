from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.database import get_db
from app.models.leaderboard import LeaderboardEntry
from app.models.user import User
from app.schemas.leaderboard import LeaderboardEntryResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/leaderboard", tags=["Leaderboard (Hall of Fame)"])


@router.get("/", response_model=List[LeaderboardEntryResponse])
async def get_global_leaderboard(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get the global leaderboard (all worlds).
    """
    entries = db.query(LeaderboardEntry, User).join(User).filter(
        LeaderboardEntry.world_id == None  # Global leaderboard
    ).order_by(desc(LeaderboardEntry.total_xp)).offset(offset).limit(limit).all()
    
    result = []
    for entry, user in entries:
        result.append(LeaderboardEntryResponse(
            entry_id=entry.entry_id,
            user_id=entry.user_id,
            username=user.username,
            avatar_class=user.avatar_class,
            world_id=entry.world_id,
            total_xp=entry.total_xp,
            total_gold=entry.total_gold,
            quests_completed=entry.quests_completed,
            monsters_defeated=entry.monsters_defeated,
            achievements_unlocked=entry.achievements_unlocked,
            rank_position=entry.rank_position,
            period_start=entry.period_start,
            period_end=entry.period_end
        ))
    
    return result


@router.get("/world/{world_id}", response_model=List[LeaderboardEntryResponse])
async def get_world_leaderboard(
    world_id: int,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get the leaderboard for a specific world.
    """
    entries = db.query(LeaderboardEntry, User).join(User).filter(
        LeaderboardEntry.world_id == world_id
    ).order_by(desc(LeaderboardEntry.total_xp)).offset(offset).limit(limit).all()
    
    result = []
    for entry, user in entries:
        result.append(LeaderboardEntryResponse(
            entry_id=entry.entry_id,
            user_id=entry.user_id,
            username=user.username,
            avatar_class=user.avatar_class,
            world_id=entry.world_id,
            total_xp=entry.total_xp,
            total_gold=entry.total_gold,
            quests_completed=entry.quests_completed,
            monsters_defeated=entry.monsters_defeated,
            achievements_unlocked=entry.achievements_unlocked,
            rank_position=entry.rank_position,
            period_start=entry.period_start,
            period_end=entry.period_end
        ))
    
    return result


@router.get("/my-rank")
async def get_my_rank(
    world_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's rank on the leaderboard.
    """
    entry = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.user_id == current_user.user_id,
        LeaderboardEntry.world_id == world_id
    ).first()
    
    if not entry:
        # Calculate rank dynamically if no entry exists
        users_above = db.query(User).filter(
            User.current_xp > current_user.current_xp
        ).count()
        
        return {
            "rank": users_above + 1,
            "total_xp": current_user.current_xp,
            "total_gold": current_user.gold,
            "message": "Rank calculated dynamically"
        }
    
    return {
        "rank": entry.rank_position,
        "total_xp": entry.total_xp,
        "total_gold": entry.total_gold,
        "quests_completed": entry.quests_completed,
        "monsters_defeated": entry.monsters_defeated,
        "achievements_unlocked": entry.achievements_unlocked
    }

