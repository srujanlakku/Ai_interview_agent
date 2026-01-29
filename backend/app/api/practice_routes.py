"""
Practice API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict, Any
from app.services.practice_service import PracticeService
from app.schemas.schemas import (
    PracticeSessionInit, PracticeStepResponse, 
    PracticeFeedbackRequest, PracticeFeedbackResponse
)
from app.utils.security import get_current_user
from app.utils.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/practice", tags=["practice"])

@router.post("/start", response_model=Dict[str, Any])
async def start_practice(
    init_data: PracticeSessionInit,
    current_user: dict = Depends(get_current_user)
):
    """Start a new practice session"""
    try:
        session = await PracticeService.start_session(
            init_data.skill_category, 
            init_data.level
        )
        return session
    except Exception as e:
        logger.error(f"Error starting practice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit", response_model=PracticeFeedbackResponse)
async def submit_practice_answer(
    answer_data: PracticeFeedbackRequest,
    current_user: dict = Depends(get_current_user)
):
    """Submit an answer to a practice question"""
    try:
        feedback = await PracticeService.submit_answer(
            answer_data.session_id, 
            answer_data.user_answer
        )
        return feedback
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error submitting practice answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}/next", response_model=PracticeStepResponse)
async def get_next_practice_step(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get the next educational step in the practice session"""
    try:
        step = await PracticeService.get_next_step(session_id)
        return step
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting next practice step: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
