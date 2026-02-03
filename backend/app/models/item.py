from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Enum, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class ItemType(str, enum.Enum):
    """Enum for item types."""
    WEAPON = "WEAPON"
    ARMOR = "ARMOR"
    CONSUMABLE = "CONSUMABLE"
    COSMETIC = "COSMETIC"
    BOOST = "BOOST"


class ItemRarity(str, enum.Enum):
    """Enum for item rarity."""
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"
    EPIC = "EPIC"
    LEGENDARY = "LEGENDARY"


class Item(Base):
    """Item model - The Loot in the shop."""
    
    __tablename__ = "items"
    
    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    item_type = Column(Enum(ItemType), nullable=False)
    rarity = Column(Enum(ItemRarity), default=ItemRarity.COMMON, nullable=False)
    price = Column(Integer, default=0, nullable=False)
    
    # Effects
    hp_bonus = Column(Integer, default=0)
    xp_multiplier = Column(Numeric(3, 2), default=1.00)
    gold_multiplier = Column(Numeric(3, 2), default=1.00)
    
    # Visual
    icon = Column(String(10), default="📦")
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    inventory_items = relationship("UserInventory", back_populates="item", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Item {self.name} ({self.rarity})>"


class UserInventory(Base):
    """UserInventory model - The Backpack."""
    
    __tablename__ = "user_inventory"
    
    inventory_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Integer, default=1, nullable=False)
    is_equipped = Column(Boolean, default=False)
    acquired_at = Column(DateTime, server_default=func.now())
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint("user_id", "item_id", name="uq_user_item"),
    )
    
    # Relationships
    user = relationship("User", back_populates="inventory")
    item = relationship("Item", back_populates="inventory_items")
    
    def __repr__(self):
        return f"<UserInventory User:{self.user_id} Item:{self.item_id}>"
