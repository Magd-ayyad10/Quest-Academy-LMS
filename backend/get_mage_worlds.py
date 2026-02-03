from app.database import SessionLocal
from app.models import World
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_mage_worlds():
    db = SessionLocal()
    try:
        # Filter for Mage worlds. 
        # Note: The User might have string "Mage" or "mage".
        mage_worlds = db.query(World).filter(World.required_class == "Mage").all()
        
        print(f"Found {len(mage_worlds)} Mage worlds:")
        for w in mage_worlds:
            print(f"ID: {w.world_id} | Title: {w.title} | Description: {w.description}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    get_mage_worlds()
