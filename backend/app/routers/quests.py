from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.quest import Quest
from app.models.zone import Zone
from app.models.user import User
from app.models.teacher import Teacher
from app.models.progress import UserProgress
from app.schemas.quest import QuestCreate, QuestResponse, QuestUpdate, QuestWithDetails
from app.utils.dependencies import get_current_teacher, get_current_user
from app.services.game_service import GameService

router = APIRouter(prefix="/api/quests", tags=["Quests (Lessons)"])


@router.get("/zone/{zone_id}", response_model=List[QuestResponse])
async def get_quests_by_zone(
    zone_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all quests for a specific zone.
    """
    quests = db.query(Quest).filter(Quest.zone_id == zone_id).order_by(Quest.order_index).all()
    return quests


@router.get("/{quest_id}", response_model=QuestWithDetails)
async def get_quest_by_id(
    quest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a quest by ID with its monsters and assignments.
    """
    quest = db.query(Quest).filter(Quest.quest_id == quest_id).first()
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found"
        )
    
    # Check completion status
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.user_id,
        UserProgress.quest_id == quest_id,
        UserProgress.is_completed == True
    ).first()
    
    # Inject status into response (assigning attribute to ORM object or dict)
    # Since QuestWithDetails expects attributes, we can set it on the object
    # Python allows setting dynamic attributes on instances in some cases, 
    # but strictly speaking we should probably let Pydantic handle it from a dict or similar.
    # However, setting it on the instance usually works for Pydantic 'from_attributes'.
    quest.is_completed = True if progress else False
    
    return quest


@router.post("/", response_model=QuestResponse, status_code=status.HTTP_201_CREATED)
async def create_quest(
    quest_data: QuestCreate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Create a new quest (teacher only).
    """
    zone = db.query(Zone).filter(Zone.zone_id == quest_data.zone_id).first()
    
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zone not found"
        )
    
    if zone.world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to add quests to this zone"
        )
    
    new_quest = Quest(
        zone_id=quest_data.zone_id,
        title=quest_data.title,
        content_url=quest_data.content_url,
        xp_reward=quest_data.xp_reward,
        gold_reward=quest_data.gold_reward,
        ai_narrative_prompt=quest_data.ai_narrative_prompt,
        order_index=quest_data.order_index
    )
    
    db.add(new_quest)
    db.commit()
    db.refresh(new_quest)
    
    return new_quest


@router.put("/{quest_id}", response_model=QuestResponse)
async def update_quest(
    quest_id: int,
    quest_update: QuestUpdate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Update a quest (teacher only).
    """
    quest = db.query(Quest).filter(Quest.quest_id == quest_id).first()
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found"
        )
    
    if quest.zone.world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this quest"
        )
    
    if quest_update.title is not None:
        quest.title = quest_update.title
    if quest_update.content_url is not None:
        quest.content_url = quest_update.content_url
    if quest_update.xp_reward is not None:
        quest.xp_reward = quest_update.xp_reward
    if quest_update.gold_reward is not None:
        quest.gold_reward = quest_update.gold_reward
    if quest_update.ai_narrative_prompt is not None:
        quest.ai_narrative_prompt = quest_update.ai_narrative_prompt
    if quest_update.order_index is not None:
        quest.order_index = quest_update.order_index
    
    db.commit()
    db.refresh(quest)
    
    return quest


@router.delete("/{quest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quest(
    quest_id: int,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Delete a quest (teacher only).
    """
    quest = db.query(Quest).filter(Quest.quest_id == quest_id).first()
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found"
        )
    
    if quest.zone.world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this quest"
        )
    
    db.delete(quest)
    db.commit()
    
    return None


@router.post("/{quest_id}/complete")
async def complete_quest(
    quest_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a quest as completed and receive rewards.
    """
    quest = db.query(Quest).filter(Quest.quest_id == quest_id).first()
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found"
        )
    
    result = GameService.complete_quest(db, current_user, quest)
    
    # Check for achievements
    new_achievements = GameService.check_and_award_achievements(db, current_user)
    
    result["new_achievements"] = [a.name for a in new_achievements]
    
    return result
