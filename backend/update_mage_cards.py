from app.database import SessionLocal
from app.models import World
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def update_mage_cards():
    db = SessionLocal()
    try:
        # Update to the new PORTRAIT cards
        mapping = {
            "The Go Grove": "/images/worlds/mage_go_card.png",
            "The Rust Ridge": "/images/worlds/mage_rust_card.png",
            "The Docker Docks": "/images/worlds/mage_docker_card.png",
            "The Kube Kingdom": "/images/worlds/mage_kube_card.png",
            "The Graph Galaxy": "/images/worlds/mage_graph_card.png",
            "The Cloud Citadel": "/images/worlds/mage_cloud_card.png"
        }

        updated_count = 0
        for title, image_path in mapping.items():
            world = db.query(World).filter(World.title == title).first()
            if world:
                print(f"Updating {title} thumbnail to {image_path}...")
                world.thumbnail_url = image_path
                updated_count += 1
            else:
                print(f"Warning: World '{title}' not found!")
        
        if updated_count > 0:
            db.commit()
            print(f"\nSuccessfully updated {updated_count} worlds with new Portrait Cards.")
        else:
            print("\nNo worlds updated.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_mage_cards()
