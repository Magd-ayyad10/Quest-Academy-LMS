from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.zone import Zone
from app.models.world import World
from app.models.teacher import Teacher
from app.schemas.zone import ZoneCreate, ZoneResponse, ZoneUpdate, ZoneWithQuests
from app.utils.dependencies import get_current_teacher

router = APIRouter(prefix="/api/zones", tags=["Zones (Modules)"])


@router.get("/world/{world_id}", response_model=List[ZoneWithQuests])
async def get_zones_by_world(
    world_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all zones for a specific world with their quests.
    """
    zones = db.query(Zone).filter(Zone.world_id == world_id).order_by(Zone.order_index).all()
    return zones


@router.get("/{zone_id}", response_model=ZoneWithQuests)
async def get_zone_by_id(
    zone_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a zone by ID with its quests.
    """
    zone = db.query(Zone).filter(Zone.zone_id == zone_id).first()
    
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zone not found"
        )
    
    return zone


@router.post("/", response_model=ZoneResponse, status_code=status.HTTP_201_CREATED)
async def create_zone(
    zone_data: ZoneCreate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Create a new zone (teacher only).
    """
    # Verify teacher owns the world
    world = db.query(World).filter(World.world_id == zone_data.world_id).first()
    
    if not world:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="World not found"
        )
    
    if world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to add zones to this world"
        )
    
    new_zone = Zone(
        world_id=zone_data.world_id,
        title=zone_data.title,
        description=zone_data.description,
        order_index=zone_data.order_index,
        is_locked=zone_data.is_locked,
        unlock_requirement_xp=zone_data.unlock_requirement_xp
    )
    
    db.add(new_zone)
    db.commit()
    db.refresh(new_zone)
    
    return new_zone


@router.put("/{zone_id}", response_model=ZoneResponse)
async def update_zone(
    zone_id: int,
    zone_update: ZoneUpdate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Update a zone (teacher only).
    """
    zone = db.query(Zone).filter(Zone.zone_id == zone_id).first()
    
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zone not found"
        )
    
    if zone.world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to edit this zone"
        )
    
    if zone_update.title is not None:
        zone.title = zone_update.title
    if zone_update.description is not None:
        zone.description = zone_update.description
    if zone_update.order_index is not None:
        zone.order_index = zone_update.order_index
    if zone_update.is_locked is not None:
        zone.is_locked = zone_update.is_locked
    if zone_update.unlock_requirement_xp is not None:
        zone.unlock_requirement_xp = zone_update.unlock_requirement_xp
    
    db.commit()
    db.refresh(zone)
    
    return zone


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_zone(
    zone_id: int,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Delete a zone (teacher only).
    """
    zone = db.query(Zone).filter(Zone.zone_id == zone_id).first()
    
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zone not found"
        )
    
    if zone.world.teacher_id != current_teacher.teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this zone"
        )
    
    db.delete(zone)
    db.commit()
    
    return None
