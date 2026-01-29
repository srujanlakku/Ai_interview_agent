import sys
from pathlib import Path

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.database import init_db
from app.utils.logging_config import setup_logging
from app.models import interview_data
from app.models.database import User, UserProfile, UserMemory, Interview
from app.api import auth_routes, interview_routes, intelligence_routes

setup_logging()
init_db()

app = FastAPI(
    title="InterviewPilot",
    description="Enterprise-grade AI interviewer platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(interview_routes.router)
app.include_router(intelligence_routes.router)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "InterviewPilot"}
