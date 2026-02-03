from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ItemType(str, Enum):
    """Enum for item types."""
    WEAPON = "WEAPON"
    ARMOR = "ARMOR"
    CONSUMABLE = "CONSUMABLE"
    COSMETIC = "COSMETIC"
    BOOST = "BOOST"


class ItemRarity(str, Enum):
    """Enum for item rarity."""
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"
    EPIC = "EPIC"
    LEGENDARY = "LEGENDARY"


class ItemResponse(BaseModel):
    """Schema for item response."""
    item_id: int
    name: str
    description: Optional[str] = None
    item_type: ItemType
    rarity: ItemRarity
    price: int
    hp_bonus: int
    xp_multiplier: float
    gold_multiplier: float
    icon: Optional[str] = None
    
    class Config:
        from_attributes = True


class InventoryResponse(BaseModel):
    """Schema for user inventory response."""
    inventory_id: int
    user_id: int
    item: ItemResponse
    quantity: int
    is_equipped: bool
    acquired_at: datetime
    
    class Config:
        from_attributes = True


class PurchaseRequest(BaseModel):
    """Schema for purchasing an item."""
    item_id: int
    quantity: int = 1


class EquipRequest(BaseModel):
    """Schema for equipping/unequipping an item."""
    item_id: int
    equip: bool = True
