import sqlite3
from passlib.context import CryptContext

# Simple context for hashing
pwd_context = CryptContext(schemes=["plaintext"], deprecated="auto")

# Connect to database
conn = sqlite3.connect('./interview_pilot.db')
cursor = conn.cursor()

# Check if test user exists
cursor.execute("SELECT * FROM users WHERE email = ?", ("test@example.com",))
existing = cursor.fetchone()

if not existing:
    # Create test user with plaintext (for testing only)
    # In production, use proper bcrypt
    hashed = "$2b$12$abcdefghijklmnopqrstuvwxyz"  # Dummy bcrypt hash
    cursor.execute("""
        INSERT INTO users (email, full_name, hashed_password, is_active)
        VALUES (?, ?, ?, ?)
    """, ("test@example.com", "Test User", hashed, 1))
    conn.commit()
    print("✓ Test user created")
else:
    print("✓ Test user already exists")

# Show all users
cursor.execute("SELECT id, email, full_name FROM users")
users = cursor.fetchall()
print(f"\nUsers in database ({len(users)}):")
for user in users:
    print(f"  - {user[1]} (ID: {user[0]})")

conn.close()
