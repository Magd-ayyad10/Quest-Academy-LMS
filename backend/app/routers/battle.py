from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import get_db
from app.models.monster import Monster
from app.models.quiz_question import QuizQuestion
from app.models.progress import UserProgress
from app.models.user import User
from app.utils.dependencies import get_current_user
from app.services.game_service import GameService
from app.schemas.battle import BattleAttackRequest, BattleAttackResponse, BattleStateResponse

router = APIRouter(prefix="/api/battle", tags=["Battle System"])

@router.get("/{monster_id}", response_model=BattleStateResponse)
async def get_battle_state(
    monster_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the state of a battle against a monster.
    Includes shuffled questions.
    """
    monster = db.query(Monster).filter(Monster.monster_id == monster_id).first()
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found")

    # Get User Battle Progress (Score)
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.user_id,
        UserProgress.quest_id == monster.quest_id
    ).first()
    
    current_score = progress.score if progress else 0
    monster_hp_pct = max(0, 100 - current_score)

    # Format Questions
    # We mix correct + wrong answers into "options"
    questions_data = []
    for q in monster.questions:
        options = q.wrong_answers + [q.correct_answer]
        random.shuffle(options)
        questions_data.append({
            "question_id": q.question_id,
            "question_text": q.question_text,
            "options": options
        })
    
    return {
        "monster_id": monster.monster_id,
        "monster_name": monster.name,
        "monster_image_url": monster.monster_image_url,
        "description": monster.description,
        "monster_hp_pct": monster_hp_pct,
        "player_hp": current_user.hp_current,
        "questions": questions_data
    }

@router.post("/attack", response_model=BattleAttackResponse)
async def attack_monster(
    attack_data: BattleAttackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit an answer to attack the monster.
    """
    try:
        result = GameService.submit_battle_answer(
            db, 
            current_user, 
            attack_data.question_id, 
            attack_data.answer
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
