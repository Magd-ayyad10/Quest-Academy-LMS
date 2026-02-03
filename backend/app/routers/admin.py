from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List

from app.database import get_db
from app.models import User, Teacher, World, Quest, Zone, Monster, Item, UserActivity, UserInventory, LeaderboardEntry
from app.schemas.admin import AdminDashboardData, SystemStats, AdminUserView, AdminWorldView, GlobalActivityView
from app.schemas.user import UserCreate
from app.schemas.teacher import TeacherCreate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/dashboard", response_model=AdminDashboardData)
def get_admin_dashboard_data(db: Session = Depends(get_db)):
    """Get comprehensive system stats for admin dashboard."""
    
    # 1. System Stats
    stats = SystemStats(
        total_users=db.query(User).count(),
        total_teachers=db.query(Teacher).count(),
        total_worlds=db.query(World).count(),
        total_quests=db.query(Quest).count(),
        total_monsters=db.query(Monster).count(),
        total_items=db.query(Item).count()
    )
    
    # 2. Users (Limit 50 for overview)
    users = db.query(User).order_by(User.created_at.desc()).limit(50).all()
    user_views = [
        AdminUserView(
            user_id=u.user_id,
            username=u.username,
            email=u.email,
            avatar_class=u.avatar_class,
            level=u.level,
            current_xp=u.current_xp,
            gold=u.gold,
            created_at=u.created_at
        ) for u in users
    ]
    
    # 3. Worlds with counts
    worlds = db.query(World).order_by(World.created_at.desc()).all()
    world_views = []
    for w in worlds:
        z_count = db.query(Zone).filter(Zone.world_id == w.world_id).count()
        q_count = db.query(Quest).join(Zone).filter(Zone.world_id == w.world_id).count()
        
        world_views.append(AdminWorldView(
            world_id=w.world_id,
            title=w.title,
            description=w.description,
            is_published=w.is_published,
            teacher_id=w.teacher_id,
            zone_count=z_count,
            quest_count=q_count,
            created_at=w.created_at
        ))
        
    # 4. Global Activity (Recent 50)
    activities = db.query(UserActivity, User).join(User).order_by(UserActivity.created_at.desc()).limit(50).all()
    activity_views = [
        GlobalActivityView(
            id=a.id,
            username=u.username,
            activity_type=str(a.activity_type), 
            title=a.title,
            xp_earned=a.xp_earned,
            created_at=a.created_at
        ) for a, u in activities
    ]
    
    return AdminDashboardData(
        stats=stats,
        recent_users=user_views,
        recent_worlds=world_views,
        recent_activity=activity_views
    )

@router.get("/users", response_model=List[AdminUserView])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.user_id).all()
    return [
        AdminUserView(
            user_id=u.user_id,
            username=u.username,
            email=u.email,
            avatar_class=u.avatar_class,
            level=u.level,
            current_xp=u.current_xp,
            gold=u.gold,
            created_at=u.created_at
        ) for u in users
    ]

# ============ USER CRUD ============

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Admin create user."""
    # Check existing
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=AuthService.get_password_hash(user_data.password),
        avatar_class=user_data.avatar_class or "Novice"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully", "user_id": user.user_id}

@router.put("/users/{user_id}")
def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    """Admin update user."""
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if "username" in user_data:
        user.username = user_data["username"]
    if "email" in user_data:
        user.email = user_data["email"]
    if "level" in user_data:
        user.level = user_data["level"]
    if "current_xp" in user_data:
        user.current_xp = user_data["current_xp"]
    if "gold" in user_data:
        user.gold = user_data["gold"]
    if "avatar_class" in user_data:
        user.avatar_class = user_data["avatar_class"]
    
    db.commit()
    return {"message": "User updated"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user."""
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

# ============ TEACHER CRUD ============

@router.get("/teachers")
def get_all_teachers(db: Session = Depends(get_db)):
    """Get all teachers."""
    teachers = db.query(Teacher).order_by(Teacher.teacher_id).all()
    return [{
        "teacher_id": t.teacher_id,
        "username": t.username,
        "email": t.email,
        "bio": t.bio,
        "specialization": t.specialization,
        "created_at": t.created_at
    } for t in teachers]

@router.post("/teachers", status_code=status.HTTP_201_CREATED)
def create_teacher(teacher_data: TeacherCreate, db: Session = Depends(get_db)):
    """Admin create teacher."""
    existing = db.query(Teacher).filter(Teacher.email == teacher_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    teacher = Teacher(
        username=teacher_data.username,
        email=teacher_data.email,
        password_hash=AuthService.get_password_hash(teacher_data.password),
        bio=teacher_data.bio,
        specialization=teacher_data.specialization
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return {"message": "Teacher created successfully", "teacher_id": teacher.teacher_id}

@router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    """Delete a teacher."""
    teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
        
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted"}

# ============ WORLD CRUD ============

from app.schemas.world import WorldCreate

@router.post("/worlds", status_code=status.HTTP_201_CREATED)
def create_world(world_data: WorldCreate, db: Session = Depends(get_db)):
    """Admin create world."""
    world = World(
        title=world_data.title,
        description=world_data.description,
        difficulty_level=world_data.difficulty_level,
        theme_prompt=world_data.theme_prompt,
        thumbnail_url=world_data.thumbnail_url,
        is_published=world_data.is_published,
        required_class=world_data.required_class,
        teacher_id=1 # Default to admin/first user for now as owner
    )
    db.add(world)
    db.commit()
    db.refresh(world)
    return {"message": "World created successfully", "world_id": world.world_id}

@router.put("/worlds/{world_id}")
def update_world(world_id: int, world_data: dict, db: Session = Depends(get_db)):
    """Admin update world."""
    world = db.query(World).filter(World.world_id == world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    
    if "title" in world_data:
        world.title = world_data["title"]
    if "description" in world_data:
        world.description = world_data["description"]
    if "difficulty_level" in world_data:
        world.difficulty_level = world_data["difficulty_level"]
    if "is_published" in world_data:
        world.is_published = world_data["is_published"]
    if "teacher_id" in world_data:
        world.teacher_id = world_data["teacher_id"]
    
    db.commit()
    return {"message": "World updated"}

@router.delete("/worlds/{world_id}")
def delete_world(world_id: int, db: Session = Depends(get_db)):
    """Delete a world."""
    world = db.query(World).filter(World.world_id == world_id).first()
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
        
    db.delete(world)
    db.commit()
    return {"message": "World deleted"}

# ============ SHOP/ITEMS CRUD ============

@router.get("/items")
def get_all_items(db: Session = Depends(get_db)):
    """Get all shop items."""
    items = db.query(Item).order_by(Item.item_id).all()
    return [{
        "item_id": i.item_id,
        "name": i.name,
        "description": i.description,
        "item_type": str(i.item_type),
        "rarity": str(i.rarity),
        "price": i.price,
        "hp_bonus": i.hp_bonus,
        "xp_multiplier": float(i.xp_multiplier) if i.xp_multiplier else 1.0,
        "gold_multiplier": float(i.gold_multiplier) if i.gold_multiplier else 1.0,
        "icon": i.icon
    } for i in items]

@router.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item_data: dict, db: Session = Depends(get_db)):
    """Admin create shop item."""
    item = Item(
        name=item_data.get("name"),
        description=item_data.get("description"),
        item_type=item_data.get("item_type", "consumable"),
        rarity=item_data.get("rarity", "common"),
        price=item_data.get("price", 100),
        hp_bonus=item_data.get("hp_bonus", 0),
        xp_multiplier=item_data.get("xp_multiplier", 1.0),
        gold_multiplier=item_data.get("gold_multiplier", 1.0),
        icon=item_data.get("icon", "📦")
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"message": "Item created successfully", "item_id": item.item_id}

@router.put("/items/{item_id}")
def update_item(item_id: int, item_data: dict, db: Session = Depends(get_db)):
    """Admin update shop item."""
    item = db.query(Item).filter(Item.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if "name" in item_data:
        item.name = item_data["name"]
    if "description" in item_data:
        item.description = item_data["description"]
    if "price" in item_data:
        item.price = item_data["price"]
    if "hp_bonus" in item_data:
        item.hp_bonus = item_data["hp_bonus"]
    if "xp_multiplier" in item_data:
        item.xp_multiplier = item_data["xp_multiplier"]
    if "gold_multiplier" in item_data:
        item.gold_multiplier = item_data["gold_multiplier"]
    
    db.commit()
    return {"message": "Item updated"}

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a shop item."""
    item = db.query(Item).filter(Item.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}

# ============ LEADERBOARD MANAGEMENT ============

@router.get("/leaderboard")
def get_leaderboard_admin(db: Session = Depends(get_db)):
    """Get full leaderboard data for admin."""
    entries = db.query(LeaderboardEntry, User).join(User).order_by(desc(LeaderboardEntry.total_xp)).limit(100).all()
    return [{
        "entry_id": e.entry_id,
        "user_id": e.user_id,
        "username": u.username,
        "total_xp": e.total_xp,
        "total_gold": e.total_gold,
        "quests_completed": e.quests_completed,
        "monsters_defeated": e.monsters_defeated,
        "achievements_unlocked": e.achievements_unlocked,
        "rank_position": e.rank_position
    } for e, u in entries]

@router.post("/leaderboard/recalculate")
def recalculate_leaderboard(db: Session = Depends(get_db)):
    """Recalculate and update all leaderboard positions."""
    # Get all users ordered by XP
    users = db.query(User).order_by(desc(User.current_xp)).all()
    
    for rank, user in enumerate(users, 1):
        # Find or create leaderboard entry
        entry = db.query(LeaderboardEntry).filter(
            LeaderboardEntry.user_id == user.user_id,
            LeaderboardEntry.world_id == None  # Global leaderboard
        ).first()
        
        if not entry:
            entry = LeaderboardEntry(user_id=user.user_id)
            db.add(entry)
        
        entry.total_xp = user.current_xp
        entry.total_gold = user.gold
        entry.rank_position = rank
    
    db.commit()
    return {"message": f"Leaderboard recalculated for {len(users)} users"}

# ============ INVENTORY MANAGEMENT ============

@router.get("/inventory")
def get_all_user_inventories(db: Session = Depends(get_db)):
    """Get all user inventories."""
    inventories = db.query(UserInventory, User, Item).join(User).join(Item).all()
    return [{
        "inventory_id": inv.inventory_id,
        "user_id": inv.user_id,
        "username": u.username,
        "item_id": inv.item_id,
        "item_name": i.name,
        "quantity": inv.quantity,
        "is_equipped": inv.is_equipped
    } for inv, u, i in inventories]

@router.post("/inventory/grant")
def grant_item_to_user(data: dict, db: Session = Depends(get_db)):
    """Grant an item to a user."""
    user_id = data.get("user_id")
    item_id = data.get("item_id")
    quantity = data.get("quantity", 1)
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    item = db.query(Item).filter(Item.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if user already has this item
    existing = db.query(UserInventory).filter(
        UserInventory.user_id == user_id,
        UserInventory.item_id == item_id
    ).first()
    
    if existing:
        existing.quantity += quantity
    else:
        new_inv = UserInventory(user_id=user_id, item_id=item_id, quantity=quantity)
        db.add(new_inv)
    
    db.commit()
    return {"message": f"Granted {quantity}x {item.name} to {user.username}"}

@router.delete("/inventory/{inventory_id}")
def remove_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    """Remove an inventory entry."""
    inv = db.query(UserInventory).filter(UserInventory.inventory_id == inventory_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    
    db.delete(inv)
    db.commit()
    return {"message": "Inventory item removed"}

