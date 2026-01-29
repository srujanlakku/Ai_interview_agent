"""
Main FastAPI application
"""
import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.utils.database import init_db
from app.utils.logging_config import setup_logging, get_logger
from app.utils.exceptions import InterviewPilotException
# Import all models to ensure they're registered with Base
from app.models import interview_data
from app.models.database import User, UserProfile, UserMemory, Interview
from app.api import auth_routes, interview_routes, profile_routes, memory_routes, speech_routes, intelligence_routes, dashboard_routes, resume_routes, practice_routes

logger = get_logger(__name__)

# Setup logging
setup_logging()

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="InterviewPilot",
    description="Enterprise-grade AI interviewer platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(interview_routes.router)
app.include_router(profile_routes.router)
app.include_router(memory_routes.router)
app.include_router(speech_routes.router)
app.include_router(intelligence_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(resume_routes.router)
app.include_router(practice_routes.router)


@app.get("/")
async def root():
    """Health check"""
    return {"status": "operational", "app": "InterviewPilot"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "InterviewPilot API",
        "version": "1.0.0"
    }


@app.exception_handler(InterviewPilotException)
async def interview_pilot_exception_handler(request: Request, exc: InterviewPilotException):
    """Handle custom InterviewPilot exceptions"""
    logger.error(f"InterviewPilot exception: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "error_code": exc.error_code,
            "message": exc.message
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP exception {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

