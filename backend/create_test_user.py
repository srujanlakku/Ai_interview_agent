#!/usr/bin/env python
"""Create test user"""
import sys
from pathlib import Path

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.models import interview_data  # Import to register models
from app.models.database import SessionLocal, User, Base, engine
from app.utils.security import hash_password

# Create tables
Base.metadata.create_all(bind=engine)

# Create session
db = SessionLocal()

try:
    # Check if test user exists
    test_user = db.query(User).filter(User.email == "test@example.com").first()
    if not test_user:
        print("Creating test user...")
        test_user = User(
            email="test@example.com",
            full_name="Test User",
            hashed_password=hash_password("password123"),
            is_active=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✓ Test user created (ID: {test_user.id})")
    else:
        print(f"✓ Test user already exists (ID: {test_user.id})")
    
    # List all users
    users = db.query(User).all()
    print(f"\nTotal users: {len(users)}")
    for user in users:
        print(f"  - {user.email} (ID: {user.id})")
        
finally:
    db.close()

print("\n✅ User setup complete!")
