from app.database import SessionLocal, engine, Base
from app.models.item import Item, ItemType, ItemRarity
from app.models.user import User
from sqlalchemy import text
import time

def reseed():
    db = SessionLocal()
    try:
        print("Dropping tables...")
        with engine.connect() as conn:
            # Postgres specific CASCADE just in case, or order matters
            conn.execute(text("DROP TABLE IF EXISTS user_inventory CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS items CASCADE"))
            conn.commit()
        print("Tables dropped.")
        
        # Give DB a second
        time.sleep(1)

        # Create tables
        import app.models.item
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created.")

        # Seed Items
        items = [
            Item(name='Potion of Healing', description='Restores 50 HP', price=50, item_type=ItemType.CONSUMABLE, hp_bonus=50, icon='🧪', rarity=ItemRarity.COMMON),
            Item(name='Mana Elixir', description='Restores 50 MP', price=60, item_type=ItemType.CONSUMABLE, hp_bonus=50, icon='💧', rarity=ItemRarity.COMMON),
            Item(name='Sword of Syntax', description='Increases Attack (Cosmetic for now)', price=150, item_type=ItemType.WEAPON, icon='🗡️', rarity=ItemRarity.UNCOMMON),
            Item(name='Shield of Logic', description='Increases Defense (Cosmetic for now)', price=150, item_type=ItemType.ARMOR, icon='🛡️', rarity=ItemRarity.UNCOMMON),
            Item(name='Scroll of Wisdom', description='Grants 100 XP', price=200, item_type=ItemType.CONSUMABLE, xp_multiplier=1.0, icon='📜', rarity=ItemRarity.RARE),
            Item(name='Golden Keyboard', description='Legendary Weapon. Keycaps of gold.', price=1000, item_type=ItemType.WEAPON, icon='⌨️', rarity=ItemRarity.LEGENDARY),
            Item(name='Debuggers Monocle', description='See through bugs.', price=500, item_type=ItemType.ARMOR, icon='🧐', rarity=ItemRarity.EPIC),
            Item(name='Coffee of Haste', description='Boosts productivity.', price=25, item_type=ItemType.CONSUMABLE, hp_bonus=10, icon='☕', rarity=ItemRarity.COMMON),
        ]

        for i in items:
            db.add(i)
        
        db.commit()
        print(f"Seeded {len(items)} items.")

        # Give the admin user some gold if needed
        admin = db.query(User).filter(User.email == "admin@questacademy.edu").first()
        if admin:
            admin.gold = 5000 
            db.commit()
            print(f"Enriched admin {admin.username} with 5000 gold.")

    except Exception as e:
        print(f"Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reseed()
