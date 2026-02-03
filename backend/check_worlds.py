"""Quick script to check and publish all worlds"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import World

def check_worlds():
    db = SessionLocal()
    try:
        worlds = db.query(World).all()
        print(f"\n=== Found {len(worlds)} worlds ===\n")
        
        for w in worlds:
            print(f"ID: {w.world_id} | Title: {w.title}")
            print(f"   Published: {w.is_published} | Teacher ID: {w.teacher_id}")
            print(f"   Required Class: {w.required_class or 'All'}")
            print()
        
        # Make all worlds published and open to all classes
        unpublished = 0
        for w in worlds:
            if not w.is_published:
                w.is_published = True
                unpublished += 1
            # Remove class restriction
            if w.required_class and w.required_class != 'All':
                w.required_class = 'All'
        
        if unpublished > 0:
            db.commit()
            print(f"\n✓ Published {unpublished} worlds!")
        else:
            print("\n✓ All worlds are already published")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_worlds()
