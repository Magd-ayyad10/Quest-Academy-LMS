
import sys
import os
from sqlalchemy import text

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def migrate():
    print("🔄 Migrating Database: Adding required_class to worlds table...")
    try:
        with engine.connect() as conn:
            # Check if column exists is hard in raw SQL generic, but we can just try to add it.
            # Postgres syntax: ALTER TABLE worlds ADD COLUMN IF NOT EXISTS required_class VARCHAR(50) DEFAULT 'All';
            # SQLite syntax doesn't support IF NOT EXISTS for columns easily.
            
            # Trying generic approach for Postgres since User mentioned Postgres config earlier.
            conn.execute(text("ALTER TABLE worlds ADD COLUMN required_class VARCHAR(50) DEFAULT 'All'"))
            conn.commit()
            print("✅ Column added successfully!")
            
    except Exception as e:
        print(f"⚠️  Migration might have failed (or column already exists): {e}")

if __name__ == "__main__":
    migrate()
