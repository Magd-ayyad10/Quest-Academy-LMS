from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserStats
from app.utils.dependencies import get_current_user
from app.services.game_service import GameService

router = APIRouter(prefix="/api/users", tags=["Users (Heroes)"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user's profile.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the current user's profile.
    """
    if user_update.username:
        # Check if username is taken
        existing = db.query(User).filter(
            User.username == user_update.username,
            User.user_id != current_user.user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = user_update.username
    
    if user_update.email:
        # Check if email is taken
        existing = db.query(User).filter(
            User.email == user_update.email,
            User.user_id != current_user.user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_update.email
    
    if user_update.avatar_class:
        current_user.avatar_class = user_update.avatar_class
    
    if user_update.avatar_url:
        current_user.avatar_url = user_update.avatar_url
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.get("/me/stats", response_model=UserStats)
async def get_current_user_stats(current_user: User = Depends(get_current_user)):
    """
    Get the current user's RPG stats.
    """
    return UserStats(
        level=current_user.level,
        current_xp=current_user.current_xp,
        hp_current=current_user.hp_current,
        hp_max=current_user.hp_max,
        gold=current_user.gold,
        avatar_class=current_user.avatar_class,
        title=current_user.title
    )


@router.post("/me/heal")
async def heal_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fully heal the current user (costs 50 gold).
    """
    heal_cost = 50
    
    if current_user.gold < heal_cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough gold! Need {heal_cost}, have {current_user.gold}"
        )
    
    if current_user.hp_current == current_user.hp_max:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already at full health!"
        )
    
    current_user.gold -= heal_cost
    current_user.hp_current = current_user.hp_max
    db.commit()
    
    return {
        "message": "Fully healed!",
        "hp_current": current_user.hp_current,
        "hp_max": current_user.hp_max,
        "gold_remaining": current_user.gold
    }


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a user's public profile by ID.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
