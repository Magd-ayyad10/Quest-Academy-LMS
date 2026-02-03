from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.progress import UserProgress
from app.models.user import User
from app.schemas.progress import ProgressResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/progress", tags=["Progress (Save File)"])


@router.get("/", response_model=List[ProgressResponse])
async def get_my_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all progress entries for the current user.
    """
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.user_id
    ).all()
    
    return progress


@router.get("/completed", response_model=List[ProgressResponse])
async def get_completed_quests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all completed quests for the current user.
    """
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.user_id,
        UserProgress.is_completed == True
    ).all()
    
    return progress


@router.get("/world/{world_id}", response_model=List[ProgressResponse])
async def get_progress_for_world(
    world_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get progress for all quests in a specific world.
    """
    # Join through quests -> zones -> world
    from app.models.quest import Quest
    from app.models.zone import Zone
    
    progress = db.query(UserProgress).join(Quest).join(Zone).filter(
        UserProgress.user_id == current_user.user_id,
        Zone.world_id == world_id
    ).all()
    
    return progress


@router.get("/stats")
async def get_progress_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get aggregated progress statistics for the current user.
    """
    total_quests = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.user_id
    ).count()
    
    completed_quests = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.user_id,
        UserProgress.is_completed == True
    ).count()
    
    # Calculate average score
    from sqlalchemy import func
    avg_score = db.query(func.avg(UserProgress.score)).filter(
        UserProgress.user_id == current_user.user_id,
        UserProgress.is_completed == True
    ).scalar() or 0
    
    return {
        "total_quests_attempted": total_quests,
        "quests_completed": completed_quests,
        "completion_rate": (completed_quests / total_quests * 100) if total_quests > 0 else 0,
        "average_score": round(float(avg_score), 2)
    }


@router.get("/transcript")
async def get_transcript(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed transcript of progress per world.
    """
    from app.models.world import World
    from app.models.quest import Quest
    from app.models.zone import Zone
    from sqlalchemy import func

    # Get all published worlds
    worlds = db.query(World).filter(World.is_published == True).all()
    transcript = []

    for world in worlds:
        # Total quests in this world
        total_quests = db.query(Quest).join(Zone).filter(Zone.world_id == world.world_id).count()
        
        if total_quests == 0:
            continue

        # Completed quests by user in this world
        completed_count = db.query(UserProgress).join(Quest).join(Zone).filter(
            UserProgress.user_id == current_user.user_id,
            UserProgress.is_completed == True,
            Zone.world_id == world.world_id
        ).count()
        
        # Average score
        avg_score = db.query(func.avg(UserProgress.score)).join(Quest).join(Zone).filter(
            UserProgress.user_id == current_user.user_id,
            UserProgress.is_completed == True,
            Zone.world_id == world.world_id
        ).scalar() or 0

        percent = (completed_count / total_quests) * 100
        
        transcript.append({
            "world_id": world.world_id,
            "title": world.title,
            "total_quests": total_quests,
            "completed_quests": completed_count,
            "progress_percent": round(percent, 1),
            "average_grade": round(float(avg_score), 1),
            "certificate_eligible": percent == 100,
            "certificate_url": f"/api/certificates/{world.world_id}" if percent == 100 else None
        })

    return transcript
