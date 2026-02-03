from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import get_db
from app.models.monster import Monster
from app.models.quest import Quest
from app.models.user import User
from app.models.teacher import Teacher
from app.schemas.monster import (
    MonsterCreate, MonsterResponse, MonsterUpdate, 
    MonsterForBattle, BattleRequest, BattleResult
)
from app.utils.dependencies import get_current_teacher, get_current_user
from app.services.game_service import GameService

router = APIRouter(prefix="/api/monsters", tags=["Monsters (Quizzes)"])


@router.get("/quest/{quest_id}", response_model=List[MonsterResponse])
async def get_monsters_by_quest(
    quest_id: int,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Get all monsters for a quest (teacher only - shows answers).
    """
    monsters = db.query(Monster).filter(Monster.quest_id == quest_id).all()
    return monsters


@router.get("/{monster_id}/battle", response_model=MonsterForBattle)
async def get_monster_for_battle(
    monster_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a monster for battle (hides correct answer, shuffles options).
    """
    monster = db.query(Monster).filter(Monster.monster_id == monster_id).first()
    
    if not monster:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monster not found"
        )
    
    # Combine and shuffle options
    options = [monster.correct_answer] + list(monster.wrong_options)
    random.shuffle(options)
    
    return MonsterForBattle(
        monster_id=monster.monster_id,
        name=monster.name,
        description=monster.description,
        question_text=monster.question_text,
        options=options,
        monster_hp=monster.monster_hp,
        monster_image_url=monster.monster_image_url
    )


@router.post("/{monster_id}/battle", response_model=BattleResult)
async def battle_monster(
    monster_id: int,
    battle_request: BattleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit an answer to battle a monster.
    """
    monster = db.query(Monster).filter(Monster.monster_id == monster_id).first()
    
    if not monster:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monster not found"
        )
    
    # Check if player has HP
    if current_user.hp_current <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have no HP left! Rest at the inn to heal."
        )
    
    result = GameService.process_battle_answer(
        db, current_user, monster, battle_request.selected_answer
    )
    
    # Check for achievements after battle
    if result["monster_defeated"]:
        new_achievements = GameService.check_and_award_achievements(db, current_user)
        result["new_achievements"] = [a.name for a in new_achievements]
    else:
        result["new_achievements"] = []
    
    return BattleResult(**result)


@router.post("/", response_model=MonsterResponse, status_code=status.HTTP_201_CREATED)
async def create_monster(
    monster_data: MonsterCreate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Create a new monster (teacher only).
    """
    quest = db.query(Quest).filter(Quest.quest_id == monster_data.quest_id).first()
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found"
        )
    
    if quest.zone.world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to add monsters to this quest"
        )
    
    new_monster = Monster(
        quest_id=monster_data.quest_id,
        name=monster_data.name,
        description=monster_data.description,
        question_text=monster_data.question_text,
        correct_answer=monster_data.correct_answer,
        wrong_options=monster_data.wrong_options,
        damage_per_wrong_answer=monster_data.damage_per_wrong_answer,
        monster_hp=monster_data.monster_hp,
        monster_image_url=monster_data.monster_image_url
    )
    
    db.add(new_monster)
    db.commit()
    db.refresh(new_monster)
    
    return new_monster


@router.put("/{monster_id}", response_model=MonsterResponse)
async def update_monster(
    monster_id: int,
    monster_update: MonsterUpdate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Update a monster (teacher only).
    """
    monster = db.query(Monster).filter(Monster.monster_id == monster_id).first()
    
    if not monster:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monster not found"
        )
    
    if monster.quest.zone.world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this monster"
        )
    
    if monster_update.name is not None:
        monster.name = monster_update.name
    if monster_update.description is not None:
        monster.description = monster_update.description
    if monster_update.question_text is not None:
        monster.question_text = monster_update.question_text
    if monster_update.correct_answer is not None:
        monster.correct_answer = monster_update.correct_answer
    if monster_update.wrong_options is not None:
        monster.wrong_options = monster_update.wrong_options
    if monster_update.damage_per_wrong_answer is not None:
        monster.damage_per_wrong_answer = monster_update.damage_per_wrong_answer
    if monster_update.monster_hp is not None:
        monster.monster_hp = monster_update.monster_hp
    if monster_update.monster_image_url is not None:
        monster.monster_image_url = monster_update.monster_image_url
    
    db.commit()
    db.refresh(monster)
    
    return monster


@router.delete("/{monster_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_monster(
    monster_id: int,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Delete a monster (teacher only).
    """
    monster = db.query(Monster).filter(Monster.monster_id == monster_id).first()
    
    if not monster:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monster not found"
        )
    
    if monster.quest.zone.world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this monster"
        )
    
    db.delete(monster)
    db.commit()
    
    return None
