"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# User Profile Schemas
class UserProfileCreate(BaseModel):
    target_company: str = Field(..., min_length=2, max_length=255)
    target_role: str = Field(..., min_length=2, max_length=255)
    interview_type: str = Field(..., pattern="^(HR|Technical|Managerial|Mixed)$")
    experience_level: str = Field(..., pattern="^(Fresher|Junior|Mid|Senior)$")
    available_hours: float = Field(..., gt=0)


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    target_company: str
    target_role: str
    interview_type: str
    experience_level: str
    available_hours: float
    created_at: datetime

    class Config:
        from_attributes = True


# Interview Schemas
class InterviewCreate(BaseModel):
    interview_type: str = Field(..., pattern="^(mock|final_prep)$")
    company_name: Optional[str] = None
    job_role: Optional[str] = None


class InterviewQuestionCreate(BaseModel):
    question_text: str
    difficulty_level: Optional[str] = None
    topic: Optional[str] = None


class InterviewQuestionResponse(BaseModel):
    id: int
    interview_id: int
    question_text: str
    user_answer: Optional[str] = None
    question_score: Optional[float] = None
    question_feedback: Optional[str] = None
    difficulty_level: Optional[str] = None
    topic: Optional[str] = None

    class Config:
        from_attributes = True


class InterviewResponse(BaseModel):
    id: int
    user_id: int
    interview_type: str
    company_name: Optional[str] = None
    job_role: Optional[str] = None
    score: Optional[float] = None
    readiness_level: Optional[str] = None
    feedback: Optional[str] = None
    duration_minutes: Optional[int] = None
    created_at: datetime
    questions: List[InterviewQuestionResponse] = []

    class Config:
        from_attributes = True


# Company Research Schemas
class CompanyResearchResponse(BaseModel):
    id: int
    company_name: str
    job_role: str
    frequently_asked_questions: Optional[List[str]] = None
    interview_rounds: Optional[Dict[str, Any]] = None
    evaluation_criteria: Optional[List[str]] = None
    required_skills: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Feedback Schemas
class FeedbackResponse(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    improvement_steps: List[str]
    revision_plan: str
    final_checklist: List[str]


class PerformanceMetrics(BaseModel):
    overall_score: float
    technical_accuracy: float
    conceptual_clarity: float
    communication_confidence: float
    readiness_level: str
    progress_trend: str  # improving, stable, declining


# New schemas for feature extensions

class CodingQuestionData(BaseModel):
    """Data structure for coding questions"""
    problem_statement: str
    expected_approach: str
    code_solution: str
    difficulty_level: str


class QuestionReviewItem(BaseModel):
    """Single question review item"""
    question_id: int
    question: str
    question_type: str
    candidate_answer: Optional[str] = None
    ideal_answer: Optional[str] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    coding_data: Optional[CodingQuestionData] = None
    
    class Config:
        from_attributes = True


class InterviewReviewResponse(BaseModel):
    """Complete interview review with all questions"""
    interview_id: int
    company_name: Optional[str] = None
    job_role: Optional[str] = None
    overall_score: Optional[float] = None
    questions: List[QuestionReviewItem]
    
    class Config:
        from_attributes = True


class DashboardQuestionItem(BaseModel):
    """Dashboard question with frequency data"""
    question: str
    question_type: str
    category: Optional[str] = None
    frequency: int
    last_asked: datetime
    
    class Config:
        from_attributes = True


class DashboardTopQuestionsResponse(BaseModel):
    """Response for top questions by company/role"""
    company: str
    role: str
    total_questions: int
    questions: List[DashboardQuestionItem]


class CompanyStatsResponse(BaseModel):
    """Company-level statistics"""
    company: str
    total_interviews: int
    most_asked_roles: List[str]
    common_topics: List[str]


# Feature 1: Resume Analyzer Schemas
class ReplaceSuggestion(BaseModel):
    original: str
    suggested: str

class RewriteExample(BaseModel):
    before: str
    after: str

class ResumeAnalysisResponse(BaseModel):
    rating: float
    strengths: List[str]
    weaknesses: List[str]
    missing_skills: List[str]
    replace_suggestions: List[ReplaceSuggestion]
    rewrite_examples: List[RewriteExample]


# Feature 2: Sure Questions Schemas
class SureQuestionItem(BaseModel):
    question_text: str
    category: str  # behavioral, technical, coding
    difficulty: str
    frequency_score: int

class SureQuestionsResponse(BaseModel):
    company: str
    role: str
    questions: Dict[str, List[SureQuestionItem]] # Grouped by category


# Feature 3: Skill Practice Schemas
class PracticeSessionInit(BaseModel):
    skill_category: str # soft_skills, technical, coding_basics
    level: str # beginner, intermediate, advanced

class PracticeStepResponse(BaseModel):
    explanation: str
    practice_question: str
    concept: str
    next_step_id: Optional[str] = None

class PracticeFeedbackRequest(BaseModel):
    session_id: str
    user_answer: str

class PracticeFeedbackResponse(BaseModel):
    feedback: str
    correct_approach: str
    improvement_tips: List[str]
    score_estimate: Optional[float] = None


class AnswerSubmitRequest(BaseModel):
    """Request schema for submitting interview answer"""
    answer: str

