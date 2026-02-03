from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.item import Item, UserInventory
from app.models.user import User
from app.schemas.item import ItemResponse, InventoryResponse, PurchaseRequest, EquipRequest
from app.utils.dependencies import get_current_user
from app.services.game_service import GameService

router = APIRouter(prefix="/api/inventory", tags=["Inventory & Shop"])


@router.get("/shop", response_model=List[ItemResponse])
async def get_shop_items(
    db: Session = Depends(get_db)
):
    """
    Get all items available in the shop.
    """
    items = db.query(Item).all()
    return items


@router.get("/my", response_model=List[InventoryResponse])
async def get_my_inventory(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's inventory.
    """
    inventory = db.query(UserInventory).filter(
        UserInventory.user_id == current_user.user_id
    ).all()
    
    return inventory


@router.get("/equipped", response_model=List[InventoryResponse])
async def get_equipped_items(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current user's equipped items.
    """
    inventory = db.query(UserInventory).filter(
        UserInventory.user_id == current_user.user_id,
        UserInventory.is_equipped == True
    ).all()
    
    return inventory


@router.post("/buy")
async def buy_item(
    purchase: PurchaseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Purchase an item from the shop.
    """
    item = db.query(Item).filter(Item.item_id == purchase.item_id).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    result = GameService.purchase_item(db, current_user, item, purchase.quantity)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result


@router.post("/equip")
async def equip_item(
    equip_request: EquipRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Equip or unequip an item.
    """
    result = GameService.equip_item(
        db, current_user, equip_request.item_id, equip_request.equip
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result


@router.post("/use/{item_id}")
async def use_consumable(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Use a consumable item.
    """
    inventory = db.query(UserInventory).filter(
        UserInventory.user_id == current_user.user_id,
        UserInventory.item_id == item_id
    ).first()
    
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not in inventory"
        )
    
    if inventory.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No items left to use"
        )
    
    item = inventory.item
    
    if item.item_type.value != "consumable":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This item is not consumable"
        )
    
    # Apply consumable effects
    effects = []
    
    if item.hp_bonus > 0:
        old_hp = current_user.hp_current
        current_user.hp_current = min(current_user.hp_max, current_user.hp_current + item.hp_bonus)
        effects.append(f"Healed {current_user.hp_current - old_hp} HP")
    
    # Reduce quantity
    inventory.quantity -= 1
    
    if inventory.quantity <= 0:
        db.delete(inventory)
    
    db.commit()
    
    return {
        "message": f"Used {item.name}",
        "effects": effects,
        "hp_current": current_user.hp_current,
        "hp_max": current_user.hp_max
    }
