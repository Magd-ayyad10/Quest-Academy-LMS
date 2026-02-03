"""Set class restrictions on worlds"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import World

def set_class_restrictions():
    db = SessionLocal()
    try:
        # Original 5 worlds - Warrior ONLY
        warrior_worlds = ["C++ World", "JAVA World", "SQL World", "JavaScript World", "AI World"]
        
        # Other classes assignments
        class_assignments = {
            "The Python Caverns": "Mage",
            "The Git Graveyard": "Mage",
            "The Debugging Ward": "Rogue",
            "Refactoring Sanctuary": "Rogue",
            "Penetration Peaks": "Healer",
            "Scripting Shadows": "Healer",
        }
        
        worlds = db.query(World).all()
        
        for world in worlds:
            if world.title in warrior_worlds:
                world.required_class = "Warrior"
                print(f"✓ {world.title} -> Warrior only")
            elif world.title in class_assignments:
                world.required_class = class_assignments[world.title]
                print(f"✓ {world.title} -> {class_assignments[world.title]} only")
            else:
                # Leave as All for any unknowns
                world.required_class = "All"
                print(f"? {world.title} -> All classes")
        
        db.commit()
        print("\n✅ Class restrictions set successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    set_class_restrictions()
