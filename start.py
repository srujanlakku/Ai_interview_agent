#!/usr/bin/env python3
"""
Comprehensive project startup and initialization script
Sets up backend, frontend, and database for InterviewPilot
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def setup_environment():
    """Set up environment variables"""
    os.environ["PYTHONPATH"] = str(backend_dir)
    os.environ["DATABASE_URL"] = "sqlite:///./interview_pilot.db"
    print("✓ Environment variables set")

def create_database_tables():
    """Create database tables"""
    try:
        from app.models.database import Base, engine
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False
    return True

def seed_interview_data():
    """Seed interview data"""
    try:
        from app.scripts.init_interview_db import init_interview_database
        init_interview_database()
        print("✓ Interview data seeded")
    except Exception as e:
        print(f"✗ Error seeding data: {e}")
        return False
    return True

def start_backend():
    """Start backend server"""
    os.chdir(str(backend_dir))
    env = os.environ.copy()
    env["PYTHONPATH"] = str(backend_dir)
    
    try:
        subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "127.0.0.1",
            "--port", "8080",
            "--log-level", "info"
        ], env=env)
        print("✓ Backend started on http://127.0.0.1:8080")
        time.sleep(2)
    except Exception as e:
        print(f"✗ Error starting backend: {e}")
        return False
    return True

def start_frontend():
    """Start frontend server"""
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(str(frontend_dir))
    
    try:
        subprocess.Popen([sys.executable, "-m", "http.server", "3000"])
        print("✓ Frontend started on http://127.0.0.1:3000")
        time.sleep(1)
    except Exception as e:
        print(f"✗ Error starting frontend: {e}")
        return False
    return True

def main():
    """Main startup routine"""
    print("\n" + "="*60)
    print("InterviewPilot - Comprehensive Startup")
    print("="*60 + "\n")
    
    setup_environment()
    
    if not create_database_tables():
        print("\n✗ Failed to create database tables")
        sys.exit(1)
    
    if not seed_interview_data():
        print("\n✗ Failed to seed interview data")
        sys.exit(1)
    
    if not start_backend():
        print("\n✗ Failed to start backend")
        sys.exit(1)
    
    if not start_frontend():
        print("\n⚠ Frontend may not have started properly")
    
    print("\n" + "="*60)
    print("✓ InterviewPilot is ready!")
    print("="*60)
    print("\nAccess the application:")
    print("  Frontend:  http://localhost:3000")
    print("  Backend:   http://localhost:8080")
    print("  API Docs:  http://localhost:8080/docs")
    print("\nPress Ctrl+C to stop all services")
    print("="*60 + "\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n✓ Shutdown complete")
        sys.exit(0)

if __name__ == "__main__":
    main()
