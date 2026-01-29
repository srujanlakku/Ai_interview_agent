"""
Interview Intelligence Routes
Company selection, role selection, and question retrieval endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from ..models.interview_data import (
    Company, Role, CompanyQuestion, UserCompanyProgress, UserRoleProgress, InterviewRound
)
from ..models.database import get_db

router = APIRouter(prefix="/api/interview", tags=["interview"])


# ==================== COMPANY ENDPOINTS ====================

@router.get("/companies")
def get_all_companies(db: Session = Depends(get_db)):
    """Get all companies"""
    companies = db.query(Company).all()
    return {
        "success": True,
        "companies": [
            {
                "id": c.id,
                "name": c.name,
                "industry_type": c.industry_type,
                "company_type": c.company_type,
                "description": c.description,
                "india_office_locations": c.india_office_locations,
            }
            for c in companies
        ]
    }


@router.get("/companies/{company_id}")
def get_company_details(company_id: str, db: Session = Depends(get_db)):
    """Get company details with supported roles"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return {
        "success": True,
        "company": {
            "id": company.id,
            "name": company.name,
            "industry_type": company.industry_type,
            "company_type": company.company_type,
            "description": company.description,
            "headquarters": company.headquarters,
            "india_office_locations": company.india_office_locations,
            "supported_roles": [
                {
                    "id": r.id,
                    "name": r.name,
                    "level": r.level,
                }
                for r in company.roles
            ]
        }
    }


@router.get("/companies/filter/{filter_type}")
def filter_companies(filter_type: str, db: Session = Depends(get_db)):
    """Filter companies by type: all, mnc, indian_it, startup, consulting"""
    if filter_type == "all":
        companies = db.query(Company).all()
    elif filter_type == "mnc":
        companies = db.query(Company).filter(Company.company_type == "MNC").all()
    elif filter_type == "indian_it":
        companies = db.query(Company).filter(Company.company_type == "Indian IT").all()
    elif filter_type == "startup":
        companies = db.query(Company).filter(Company.company_type == "Startup").all()
    elif filter_type == "consulting":
        companies = db.query(Company).filter(Company.company_type == "Consulting").all()
    else:
        raise HTTPException(status_code=400, detail="Invalid filter type")
    
    return {
        "success": True,
        "filter": filter_type,
        "companies": [
            {
                "id": c.id,
                "name": c.name,
                "industry_type": c.industry_type,
                "company_type": c.company_type,
            }
            for c in companies
        ]
    }


# ==================== ROLE ENDPOINTS ====================

@router.get("/roles")
def get_all_roles(db: Session = Depends(get_db)):
    """Get all available roles"""
    roles = db.query(Role).all()
    return {
        "success": True,
        "roles": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "level": r.level,
            }
            for r in roles
        ]
    }


@router.get("/companies/{company_id}/roles")
def get_company_roles(company_id: str, db: Session = Depends(get_db)):
    """Get roles supported by a specific company"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return {
        "success": True,
        "company_id": company_id,
        "company_name": company.name,
        "roles": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "level": r.level,
            }
            for r in company.roles
        ]
    }


# ==================== QUESTION ENDPOINTS ====================

@router.get("/questions/company/{company_id}/role/{role_id}")
def get_company_role_questions(
    company_id: str,
    role_id: str,
    difficulty: Optional[str] = None,
    round_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get repeated questions for a company and role combination"""
    query = db.query(CompanyQuestion).filter(
        (CompanyQuestion.company_id == company_id) | (CompanyQuestion.company_id == None),
        (CompanyQuestion.role_id == role_id) | (CompanyQuestion.role_id == None),
        CompanyQuestion.is_repeated == True
    )
    
    if difficulty:
        query = query.filter(CompanyQuestion.difficulty == difficulty)
    
    if round_id:
        query = query.filter(CompanyQuestion.round_id == round_id)
    
    questions = query.order_by(CompanyQuestion.frequency_score.desc()).all()
    
    return {
        "success": True,
        "company_id": company_id,
        "role_id": role_id,
        "total_questions": len(questions),
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "category": q.category,
                "difficulty": q.difficulty,
                "topics": q.topics,
                "frequency_score": q.frequency_score,
                "answer_guidelines": q.answer_guidelines,
            }
            for q in questions
        ]
    }


@router.get("/questions/role/{role_id}")
def get_role_questions(
    role_id: str,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all questions for a specific role across all companies"""
    query = db.query(CompanyQuestion).filter(
        (CompanyQuestion.role_id == role_id) | (CompanyQuestion.role_id == None),
        CompanyQuestion.is_repeated == True
    )
    
    if difficulty:
        query = query.filter(CompanyQuestion.difficulty == difficulty)
    
    questions = query.order_by(CompanyQuestion.frequency_score.desc()).all()
    
    return {
        "success": True,
        "role_id": role_id,
        "total_questions": len(questions),
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "category": q.category,
                "difficulty": q.difficulty,
                "topics": q.topics,
                "frequency_score": q.frequency_score,
            }
            for q in questions
        ]
    }


# ==================== INTERVIEW ROUNDS ====================

@router.get("/rounds")
def get_interview_rounds(db: Session = Depends(get_db)):
    """Get all interview rounds"""
    rounds = db.query(InterviewRound).order_by(InterviewRound.order).all()
    return {
        "success": True,
        "rounds": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "order": r.order,
            }
            for r in rounds
        ]
    }


# ==================== USER PROGRESS ENDPOINTS ====================

@router.get("/user/progress/company/{company_id}")
def get_user_company_progress(company_id: str, db: Session = Depends(get_db)):
    """Get user's progress for a specific company"""
    # This would be implemented with actual user authentication
    # For now, returning mock data structure
    return {
        "success": True,
        "company_id": company_id,
        "readiness_score": 0,
        "questions_attempted": 0,
        "questions_mastered": 0,
        "topics_covered": [],
    }


@router.get("/user/progress/role/{role_id}")
def get_user_role_progress(role_id: str, db: Session = Depends(get_db)):
    """Get user's progress for a specific role"""
    return {
        "success": True,
        "role_id": role_id,
        "readiness_score": 0,
        "questions_attempted": 0,
        "questions_mastered": 0,
        "topics_covered": [],
    }


@router.post("/user/select-interview")
def select_interview(
    company_id: str,
    role_id: str,
    round_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """User selects a company and role for interview"""
    # Validate company exists
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Validate role exists and is supported by company
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if role not in company.roles:
        raise HTTPException(status_code=400, detail="Role not supported by this company")
    
    # Get questions for this company-role combination
    questions = db.query(CompanyQuestion).filter(
        ((CompanyQuestion.company_id == company_id) | (CompanyQuestion.company_id == None)) &
        ((CompanyQuestion.role_id == role_id) | (CompanyQuestion.role_id == None)) &
        (CompanyQuestion.is_repeated == True)
    ).order_by(CompanyQuestion.frequency_score.desc()).limit(5).all()
    
    return {
        "success": True,
        "message": f"Interview selected: {company.name} - {role.name}",
        "company": {
            "id": company.id,
            "name": company.name,
        },
        "role": {
            "id": role.id,
            "name": role.name,
            "level": role.level,
        },
        "available_questions": len(questions),
        "interview_questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "difficulty": q.difficulty,
                "category": q.category,
                "topics": q.topics,
            }
            for q in questions
        ]
    }


# ==================== STATISTICS ENDPOINTS ====================

@router.get("/stats/company/{company_id}")
def get_company_stats(company_id: str, db: Session = Depends(get_db)):
    """Get statistics for a company"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    total_questions = db.query(CompanyQuestion).filter(
        CompanyQuestion.company_id == company_id
    ).count()
    
    return {
        "success": True,
        "company": {
            "id": company.id,
            "name": company.name,
        },
        "stats": {
            "total_questions": total_questions,
            "supported_roles": len(company.roles),
            "industry_type": company.industry_type,
        }
    }
