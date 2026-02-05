"""
Main application module for InterviewPilot.
"""
from app.config import settings
from app.main import app
from app.utils.database import init_db

# Initialize database
init_db()

__all__ = [
    "settings",
    "app",
    "init_db"
]
