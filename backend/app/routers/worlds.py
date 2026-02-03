from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.world import World
from app.models.teacher import Teacher
from app.schemas.world import WorldCreate, WorldResponse, WorldUpdate, WorldWithZones
from app.utils.dependencies import get_current_teacher

router = APIRouter(prefix="/api/worlds", tags=["Worlds (Courses)"])


@router.get("/", response_model=List[WorldResponse])
async def get_all_worlds(
    skip: int = 0,
    limit: int = 100,
    published_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get all worlds (courses). By default, returns only published worlds.
    """
    query = db.query(World)
    
    if published_only:
        query = query.filter(World.is_published == True)
    
    worlds = query.offset(skip).limit(limit).all()
    
    # Manually populate zones_count since it's not a DB column
    for world in worlds:
        world.zones_count = len(world.zones)
        
    return worlds


@router.get("/{world_id}", response_model=WorldWithZones)
async def get_world_by_id(
    world_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a world by ID with its zones.
    """
    world = db.query(World).filter(World.world_id == world_id).first()
    
    if not world:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="World not found"
        )
    
    return world


@router.post("/", response_model=WorldResponse, status_code=status.HTTP_201_CREATED)
async def create_world(
    world_data: WorldCreate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Create a new world (teacher only).
    """
    new_world = World(
        teacher_id=current_teacher.teacher_id,
        title=world_data.title,
        description=world_data.description,
        difficulty_level=world_data.difficulty_level,
        theme_prompt=world_data.theme_prompt,
        thumbnail_url=world_data.thumbnail_url,
        is_published=world_data.is_published
    )
    
    db.add(new_world)
    db.commit()
    db.refresh(new_world)
    
    return new_world


@router.put("/{world_id}", response_model=WorldResponse)
async def update_world(
    world_id: int,
    world_update: WorldUpdate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Update a world (teacher only, must own the world).
    """
    world = db.query(World).filter(World.world_id == world_id).first()
    
    if not world:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="World not found"
        )
    
    if world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this world"
        )
    
    if world_update.title is not None:
        world.title = world_update.title
    if world_update.description is not None:
        world.description = world_update.description
    if world_update.difficulty_level is not None:
        world.difficulty_level = world_update.difficulty_level
    if world_update.theme_prompt is not None:
        world.theme_prompt = world_update.theme_prompt
    if world_update.thumbnail_url is not None:
        world.thumbnail_url = world_update.thumbnail_url
    if world_update.is_published is not None:
        world.is_published = world_update.is_published
    
    db.commit()
    db.refresh(world)
    
    return world


@router.delete("/{world_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_world(
    world_id: int,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Delete a world (teacher only, must own the world).
    """
    world = db.query(World).filter(World.world_id == world_id).first()
    
    if not world:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="World not found"
        )
    
    if world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this world"
        )
    
    db.delete(world)
    db.commit()
    
    return None
