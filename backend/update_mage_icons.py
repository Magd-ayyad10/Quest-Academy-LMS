from app.database import SessionLocal
from app.models import World
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def update_mage_icons():
    db = SessionLocal()
    try:
        mapping = {
            "The Go Grove": "/images/worlds/mage_go.png",
            "The Rust Ridge": "/images/worlds/mage_rust.png",
            "The Docker Docks": "/images/worlds/mage_docker.png",
            "The Kube Kingdom": "/images/worlds/mage_kubernetes.png",
            "The Graph Galaxy": "/images/worlds/mage_graphql.png",
            "The Cloud Citadel": "/images/worlds/mage_cloud.png"
        }

        updated_count = 0
        for title, image_path in mapping.items():
            world = db.query(World).filter(World.title == title).first()
            if world:
                print(f"Updating {title}...")
                world.thumbnail_url = image_path
                world.required_class = "Mage"  # Enforce Mage restriction
                updated_count += 1
            else:
                print(f"Warning: World '{title}' not found!")
        
        if updated_count > 0:
            db.commit()
            print(f"\nSuccessfully updated {updated_count} worlds (Icon + Mage Restriction).")
        else:
            print("\nNo worlds updated.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_mage_icons()
