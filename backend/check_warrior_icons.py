from app.database import SessionLocal
from app.models import World
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def restore_warrior_icons():
    db = SessionLocal()
    try:
        # Define the original mapping for Warrior worlds
        # These appear to be the "original" based on previous context or assumptions
        # If specific URLs were lost, we might need to look at previous file versions or revert to defaults
        # However, typically the dashboard used hardcoded logic based on keywords if no URL was in DB.
        # My previous script might have accidentally overwritten them? 
        # Actually my previous script only targeted the 6 specific Mage titles.
        # The user says "logos have disappeared". This suggests that my Frontend change broke the fallback.
        
        # Let's check what the Warrior worlds are currently set to.
        warrior_worlds = db.query(World).filter(World.required_class == "Warrior").all()
        print(f"Found {len(warrior_worlds)} Warrior worlds. Checking status...")
        
        for w in warrior_worlds:
            print(f"ID: {w.world_id} | Title: {w.title} | Thumb: {w.thumbnail_url}")
            
            # If the thumbnail is now None or empty, the frontend should fallback. 
            # If it's something broken, let's reset it to None Use Defaults.
            # But the user said "put the icons back as they were". 
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    restore_warrior_icons()
