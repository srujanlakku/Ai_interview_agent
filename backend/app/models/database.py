"""
Database models for InterviewPilot
"""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, JSON, Enum as SQLEnum, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./interview_pilot.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Get database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    interviews = relationship("Interview", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    memory = relationship("UserMemory", back_populates="user", cascade="all, delete-orphan")
    company_progress = relationship("UserCompanyProgress", back_populates="user", cascade="all, delete-orphan", foreign_keys="UserCompanyProgress.user_id")
    role_progress = relationship("UserRoleProgress", back_populates="user", cascade="all, delete-orphan", foreign_keys="UserRoleProgress.user_id")
    question_responses = relationship("UserQuestionResponse", back_populates="user", cascade="all, delete-orphan", foreign_keys="UserQuestionResponse.user_id")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_company = Column(String(255), nullable=True)
    target_role = Column(String(255), nullable=True)
    interview_type = Column(String(50), nullable=True)  # HR, Technical, Managerial, Mixed
    experience_level = Column(String(50), nullable=True)  # Fresher, Junior, Mid, Senior
    available_hours = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")


class UserMemory(Base):
    __tablename__ = "user_memory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    memory_type = Column(String(50), nullable=False)  # strength, weakness, topic_covered, missed_topic
    content = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)  # Changed from 'metadata' to 'data'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="memory")


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interview_type = Column(String(50), nullable=False)  # mock, final_prep
    company_name = Column(String(255), nullable=True)
    job_role = Column(String(255), nullable=True)
    score = Column(Float, nullable=True)
    readiness_level = Column(String(50), nullable=True)  # Not Ready, Almost Ready, Interview Ready
    feedback = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    agent_state = Column(JSON, nullable=True)  # Store multi-agent orchestration state
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="interviews")
    questions = relationship("InterviewSessionQuestion", back_populates="interview", cascade="all, delete-orphan")


class InterviewSessionQuestion(Base):
    __tablename__ = "interview_session_questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="soft_skill")  # soft_skill, technical, coding
    user_answer = Column(Text, nullable=True)
    answer_transcript = Column(Text, nullable=True)  # For voice answers
    question_score = Column(Float, nullable=True)
    question_feedback = Column(Text, nullable=True)
    difficulty_level = Column(String(50), nullable=True)  # Easy, Medium, Hard
    topic = Column(String(255), nullable=True)
    
    # New fields for answer review
    ideal_answer = Column(Text, nullable=True)  # Expected/correct answer
    
    # Coding question specific fields
    problem_statement = Column(Text, nullable=True)  # For coding questions
    expected_approach = Column(Text, nullable=True)  # Expected solution approach
    code_solution = Column(Text, nullable=True)  # Sample correct code
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interview = relationship("Interview", back_populates="questions")


class CompanyResearch(Base):
    __tablename__ = "company_research"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), unique=True, index=True, nullable=False)
    job_role = Column(String(255), index=True, nullable=False)
    frequently_asked_questions = Column(JSON, nullable=True)
    interview_rounds = Column(JSON, nullable=True)
    evaluation_criteria = Column(JSON, nullable=True)
    required_skills = Column(JSON, nullable=True)
    technologies = Column(JSON, nullable=True)
    research_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PreparationMaterial(Base):
    __tablename__ = "preparation_materials"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    topic = Column(String(255), nullable=False)
    content_type = Column(String(50), nullable=False)  # text, image, video, link
    content = Column(Text, nullable=False)
    relevance_score = Column(Float, nullable=True)
    difficulty_level = Column(String(50), nullable=True)  # Easy, Medium, Hard
    created_at = Column(DateTime, default=datetime.utcnow)


class QuestionFrequency(Base):
    """Track frequently asked questions by company and role"""
    __tablename__ = "question_frequency"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), index=True, nullable=False)
    job_role = Column(String(255), index=True, nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # soft_skill, technical, coding
    category = Column(String(100), nullable=True)  # DSA, System Design, Behavioral, etc.
    frequency_count = Column(Integer, default=1)
    last_asked_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

