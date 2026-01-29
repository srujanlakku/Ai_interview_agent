"""
Dashboard API routes for analytics and frequently asked questions
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.services.analytics_service import AnalyticsService
from app.schemas.schemas import (
    DashboardTopQuestionsResponse, DashboardQuestionItem, 
    CompanyStatsResponse, SureQuestionsResponse, SureQuestionItem
)
from app.utils.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/top-questions", response_model=DashboardTopQuestionsResponse)
async def get_top_questions(
    company: str = Query(..., description="Company name"),
    role: str = Query(..., description="Job role"),
    limit: int = Query(20, ge=1, le=100, description="Number of questions to return"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get frequently asked questions for a specific company and role"""
    try:
        logger.info(f"Fetching top questions for {company} - {role} (limit: {limit})")
        
        questions_data = AnalyticsService.get_top_questions(db, company, role, limit)
        
        questions = [
            DashboardQuestionItem(
                question=q.question_text,
                question_type=q.question_type,
                category=q.category,
                frequency=q.frequency_count,
                last_asked=q.last_asked_date
            )
            for q in questions_data
        ]
        
        return DashboardTopQuestionsResponse(
            company=company,
            role=role,
            total_questions=len(questions),
            questions=questions
        )
    
    except Exception as e:
        logger.error(f"Error fetching top questions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch top questions: {str(e)}")


@router.get("/company-stats", response_model=CompanyStatsResponse)
async def get_company_stats(
    company: str = Query(..., description="Company name"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get statistics for a specific company"""
    try:
        logger.info(f"Fetching stats for company: {company}")
        
        stats = AnalyticsService.get_company_stats(db, company)
        
        return CompanyStatsResponse(**stats)
    
    except Exception as e:
        logger.error(f"Error fetching company stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch company stats: {str(e)}")


@router.get("/role-categories")
async def get_role_question_categories(
    role: str = Query(..., description="Job role"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get breakdown of question types for a specific role"""
    try:
        logger.info(f"Fetching question categories for role: {role}")
        
        categories = AnalyticsService.get_question_categories_for_role(db, role)
        
        return {
            "role": role,
            "categories": categories
        }
    
    except Exception as e:
        logger.error(f"Error fetching role categories: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch role categories: {str(e)}")
@router.get("/sure-questions", response_model=SureQuestionsResponse)
async def get_sure_questions(
    company: str = Query(..., description="Company name"),
    role: str = Query(..., description="Job role"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get 'sure' questions for a company and role, grouped by category"""
    try:
        logger.info(f"Fetching sure questions for {company} - {role}")
        
        grouped_questions = AnalyticsService.get_sure_questions(db, company, role)
        
        response_data = {
            "company": company,
            "role": role,
            "questions": {
                cat: [
                    SureQuestionItem(
                        question_text=q.question_text,
                        category=q.category or cat,
                        difficulty="Medium", # Defaulting as it's not in QuestionFrequency
                        frequency_score=q.frequency_count
                    )
                    for q in qs
                ]
                for cat, qs in grouped_questions.items()
            }
        }
        
        return response_data
    
    except Exception as e:
        logger.error(f"Error fetching sure questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
