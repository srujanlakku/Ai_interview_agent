"""
Interview Data Models
Company, Role, and Question data structures for India-focused MNC interview intelligence
"""

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


# Association table for many-to-many relationship between Company and Role
company_role_association = Table(
    'company_role_association',
    Base.metadata,
    Column('company_id', String, ForeignKey('company.id')),
    Column('role_id', String, ForeignKey('role.id'))
)


class Company(Base):
    """MNC Companies operating in India"""
    __tablename__ = 'company'
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    industry_type = Column(String, nullable=False)  # Tech, IT Services, Startup, Consulting, FinTech, Hardware
    description = Column(Text)
    headquarters = Column(String)
    india_office_locations = Column(String)  # Comma-separated cities
    company_type = Column(String, nullable=False)  # MNC, Indian IT, Startup, Consulting, FinTech
    
    # Relationships
    roles = relationship("Role", secondary=company_role_association, back_populates="companies")
    questions = relationship("CompanyQuestion", back_populates="company", cascade="all, delete-orphan")
    user_company_progress = relationship("UserCompanyProgress", back_populates="company", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class Role(Base):
    """Job roles across companies"""
    __tablename__ = 'role'
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    level = Column(String)  # Junior, Mid, Senior, Lead
    
    # Relationships
    companies = relationship("Company", secondary=company_role_association, back_populates="roles")
    questions = relationship("CompanyQuestion", back_populates="role", cascade="all, delete-orphan")
    user_role_progress = relationship("UserRoleProgress", back_populates="role", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, server_default=func.now())


class InterviewRound(Base):
    """Interview round types"""
    __tablename__ = 'interview_round'
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)  # HR, Technical Round 1, Technical Round 2, System Design, Behavioral
    description = Column(Text)
    order = Column(Integer)
    
    created_at = Column(DateTime, server_default=func.now())


class CompanyQuestion(Base):
    """Repeated interview questions database"""
    __tablename__ = 'interview_question'
    
    id = Column(String, primary_key=True)
    company_id = Column(String, ForeignKey('company.id'), nullable=True)  # NULL = general question
    role_id = Column(String, ForeignKey('role.id'), nullable=True)  # NULL = role-agnostic
    round_id = Column(String, ForeignKey('interview_round.id'), nullable=True)
    
    question_text = Column(Text, nullable=False)
    category = Column(String)  # Technical, Behavioral, HR, System Design
    difficulty = Column(String, nullable=False)  # Easy, Medium, Hard
    
    # Topic tags for categorization
    topics = Column(String)  # Comma-separated: DSA, OOPs, DBMS, OS, Networking, System Design, AI/ML, Behavioral
    
    # Frequency and importance
    frequency_score = Column(Integer, default=1)  # 1-10, how often this question is asked
    is_repeated = Column(Boolean, default=True)  # Is this a commonly repeated question?
    
    # Expected answer guidelines
    answer_guidelines = Column(Text)
    
    # Relationships
    company = relationship("Company", back_populates="questions")
    role = relationship("Role", back_populates="questions")
    user_question_responses = relationship("UserQuestionResponse", back_populates="question", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class UserCompanyProgress(Base):
    """Track user progress per company"""
    __tablename__ = 'user_company_progress'
    
    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Reference users table
    company_id = Column(String, ForeignKey('company.id'), nullable=False)
    
    # Progress metrics
    readiness_score = Column(Integer, default=0)  # 0-100
    questions_attempted = Column(Integer, default=0)
    questions_mastered = Column(Integer, default=0)
    topics_covered = Column(String)  # Comma-separated
    
    # Last interview stats
    last_interview_score = Column(Integer)
    last_interview_date = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="company_progress", foreign_keys=[user_id])
    company = relationship("Company", back_populates="user_company_progress")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class UserRoleProgress(Base):
    """Track user progress per role"""
    __tablename__ = 'user_role_progress'
    
    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Reference users table
    role_id = Column(String, ForeignKey('role.id'), nullable=False)
    
    # Progress metrics
    readiness_score = Column(Integer, default=0)  # 0-100
    questions_attempted = Column(Integer, default=0)
    questions_mastered = Column(Integer, default=0)
    topics_covered = Column(String)  # Comma-separated
    
    # Last interview stats
    last_interview_score = Column(Integer)
    last_interview_date = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="role_progress", foreign_keys=[user_id])
    role = relationship("Role", back_populates="user_role_progress")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class UserQuestionResponse(Base):
    """Track user responses to specific questions"""
    __tablename__ = 'user_question_response'
    
    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Reference users table
    question_id = Column(String, ForeignKey('interview_question.id'), nullable=False)
    
    # Response tracking
    answer_text = Column(Text)
    score = Column(Integer)  # 1-10
    confidence_level = Column(Integer)  # 1-10
    time_taken = Column(Integer)  # seconds
    
    # AI Feedback
    ai_feedback = Column(Text)
    is_passed = Column(Boolean, default=False)
    
    # Attempt tracking
    attempt_number = Column(Integer, default=1)
    last_attempted_date = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="question_responses", foreign_keys=[user_id])
    question = relationship("CompanyQuestion", back_populates="user_question_responses")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
