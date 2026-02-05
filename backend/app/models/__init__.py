"""
Database models for InterviewPilot.
"""
from app.models.database import (
    User,
    UserProfile,
    UserMemory,
    Interview,
    InterviewSessionQuestion,
    CompanyResearch,
    PreparationMaterial,
    QuestionFrequency,
    Base,
    get_db
)
from app.models.interview_data import (
    Company,
    Role,
    InterviewRound,
    CompanyQuestion,
    UserCompanyProgress,
    UserRoleProgress,
    UserQuestionResponse
)

__all__ = [
    # Database models
    "User",
    "UserProfile",
    "UserMemory",
    "Interview",
    "InterviewSessionQuestion",
    "CompanyResearch",
    "PreparationMaterial",
    "QuestionFrequency",
    "Base",
    "get_db",
    
    # Interview data models
    "Company",
    "Role",
    "InterviewRound",
    "CompanyQuestion",
    "UserCompanyProgress",
    "UserRoleProgress",
    "UserQuestionResponse"
]
