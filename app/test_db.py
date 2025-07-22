import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from sqlalchemy import text  # ✅ import text

def test_connection():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))  
        print("✅ Database connected successfully!")
    except Exception as e:
        print("❌ Database connection failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
