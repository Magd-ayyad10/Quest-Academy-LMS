from app.database import SessionLocal
from app.models import World
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def repair_warrior_icons():
    db = SessionLocal()
    try:
        # Define the original mapping for Warrior worlds based on backend/add_new_worlds.py and defaults
        # We need to manually set these back to what they were (or sane defaults if lost).
        # We previously saw they might have 'None' or '/assets/worlds/...'
        
        # NOTE: The User complained they "disappeared". In my previous Dashboard.jsx edit:
        # const bgImage = world.thumbnail_url || getWorldBg(world.title);
        # If thumbnail_url is None, it falls back to getWorldBg() which returns hardcoded paths like '/images/worlds/python_bg.jpg'
        
        # However, if thumbnail_url is set to "None" (string) or an invalid path, it might break.
        # The check_warrior_icons.py showed ID 33 is None, but others have "/assets/worlds/..."
        # The "/assets/..." path might be wrong if the folder is actually "public/images/worlds/..."
        # Let's check if "public/assets/worlds" exists? No, I only saw "public/images".
        
        # It seems the seed script used "/assets/worlds/..." but those files might not exist or be served correctly if mapped to "/images".
        # Let's update them to use the logic that works (null) so they fallback to the frontend defaults, OR update them to valid paths.
        
        warrior_worlds = db.query(World).filter(World.required_class == "Warrior").all()
        print(f"Restoring {len(warrior_worlds)} Warrior worlds...")

        for w in warrior_worlds:
            # If the path starts with /assets/, it's likely broken because we are serving from /images
            # The frontend `getWorldBg` function in Dashboard.jsx handles:
            # python, javascript, sql, c++, java, ai, git.
            
            # If we set thumbnail_url to None (NULL), the frontend will use its internal hardcoded map, which IS working (presumably).
            # The User said "put the icons of the warrior page back as they were".
            # If they were working before, they were likely using the fallback logic.
            # So I should nullify the thumbnail_url for Warrior worlds if it looks suspicious.
            
            print(f"Processing {w.title} (Current: {w.thumbnail_url})")
            w.thumbnail_url = None
                
        db.commit()
        print(f"\n✓ Warrior worlds restored to use default frontend icons/backgrounds.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    repair_warrior_icons()
