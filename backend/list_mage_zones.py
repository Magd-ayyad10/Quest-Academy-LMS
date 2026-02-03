from app.database import SessionLocal
from app.models import World, Zone
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def list_mage_zones():
    db = SessionLocal()
    try:
        mage_worlds = db.query(World).filter(World.required_class == "Mage").all()
        print(f"Found {len(mage_worlds)} Mage worlds.")
        
        for w in mage_worlds:
            print(f"\nWorld: {w.title} (ID: {w.world_id})")
            zones = db.query(Zone).filter(Zone.world_id == w.world_id).order_by(Zone.order_index).all()
            for z in zones:
                print(f"  - Zone: {z.title} (ID: {z.zone_id})")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_mage_zones()
