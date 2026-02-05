"""
Data module for interview questions and repositories.
"""
from app.data.interview_seed_data import (
    COMPANIES_DATA,
    ROLES_DATA, 
    INTERVIEW_ROUNDS_DATA,
    INTERVIEW_QUESTIONS_DATA
)
from app.data.question_repository import (
    QuestionRepository,
    get_question_repository
)

__all__ = [
    "COMPANIES_DATA",
    "ROLES_DATA",
    "INTERVIEW_ROUNDS_DATA", 
    "INTERVIEW_QUESTIONS_DATA",
    "QuestionRepository",
    "get_question_repository"
]