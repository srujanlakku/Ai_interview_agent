"""
API Routes for InterviewPilot.
"""
from app.api.auth_routes import router as auth_router
from app.api.interview_routes import router as interview_router
from app.api.profile_routes import router as profile_router
from app.api.memory_routes import router as memory_router
from app.api.speech_routes import router as speech_router
from app.api.intelligence_routes import router as intelligence_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.resume_routes import router as resume_router
from app.api.practice_routes import router as practice_router

__all__ = [
    "auth_router",
    "interview_router",
    "profile_router",
    "memory_router",
    "speech_router",
    "intelligence_router",
    "dashboard_router",
    "resume_router",
    "practice_router"
]
