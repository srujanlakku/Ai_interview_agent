"""
Interview API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.utils.database import get_db
from app.schemas.schemas import InterviewCreate, InterviewResponse, InterviewQuestionCreate, PerformanceMetrics
from app.services.interview_service import InterviewService
from app.utils.security import get_current_user
from app.agents.interviewer_agent import InterviewerAgent
from app.agents.evaluation_agent import EvaluationAgent
from app.agents.memory_agent import MemoryAgent
from app.utils.logging_config import get_logger
from app.utils.exceptions import NotFoundError, ValidationError
import asyncio

logger = get_logger(__name__)
router = APIRouter(prefix="/api/interviews", tags=["interviews"])

# Note: Modern orchestration uses InterviewSupervisorAgent via InterviewService.
# evaluation_agent is kept here for legacy support of the direct /finalize route if needed.
evaluation_agent = EvaluationAgent()


@router.post("/create", response_model=InterviewResponse)
async def create_interview(
    interview_create: InterviewCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new interview"""
    try:
        user_id = current_user.get("user_id")
        interview = InterviewService.create_interview(db, user_id, interview_create)
        logger.info(f"Interview created: {interview.id}")
        return interview
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating interview: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create interview")


@router.get("/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get interview details"""
    try:
        user_id = current_user.get("user_id")
        interview = InterviewService.get_interview(db, interview_id, user_id)
        return interview
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching interview: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch interview")


@router.get("/user/list", response_model=List[InterviewResponse])
async def get_user_interviews(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all interviews for current user"""
    try:
        user_id = current_user.get("user_id")
        interviews = InterviewService.get_user_interviews(db, user_id)
        return interviews
    except Exception as e:
        logger.error(f"Error fetching user interviews: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch interviews")


@router.post("/{interview_id}/start-question")
async def start_next_question(
    interview_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get next interview question using multi-agent supervisor"""
    try:
        user_id = current_user.get("user_id")
        result = await InterviewService.start_agent_interview(db, interview_id, user_id)
        
        return {
            "interview_id": interview_id,
            "status": result.get("status"),
            "question": result.get("current_question"),
            "question_number": result.get("question_count")
        }
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error starting agent question: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start question")


@router.post("/{interview_id}/submit-answer")
async def submit_answer(
    interview_id: int, 
    answer: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Submit answer and get next step from multi-agent supervisor"""
    try:
        user_id = current_user.get("user_id")
        new_state = await InterviewService.process_agent_step(db, interview_id, user_id, answer)
        
        return {
            "success": True,
            "status": new_state.get("status"),
            "next_question": new_state.get("current_question") if new_state.get("status") == "in_progress" else None,
            "summary": new_state.get("summary") if new_state.get("status") == "completed" else None,
            "question_number": new_state.get("question_count")
        }
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error submitting agent answer: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit answer")


@router.post("/{interview_id}/finalize")
async def finalize_interview(
    interview_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Finalize interview and get scores"""
    try:
        user_id = current_user.get("user_id")
        interview = InterviewService.get_interview(db, interview_id, user_id)
        
        # Evaluate entire interview
        interview_data = {
            "questions": [],
            "user_profile": {}
        }
        
        evaluation_result = await evaluation_agent.execute(interview_data)
        
        if not evaluation_result.get("success"):
            raise HTTPException(status_code=500, detail="Failed to evaluate interview")
        
        scores = evaluation_result.get("scores", {})
        readiness = evaluation_result.get("readiness_level", "Not Ready")
        feedback = evaluation_result.get("feedback", "")
        
        # Update interview
        updated_interview = InterviewService.finalize_interview(
            db, interview_id, user_id,
            overall_score=scores.get("overall_score", 0),
            readiness_level=readiness,
            feedback=feedback,
            duration_minutes=30
        )
        
        return {
            "success": True,
            "interview_id": interview_id,
            "scores": scores,
            "readiness_level": readiness,
            "feedback": feedback
        }
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error finalizing interview: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to finalize interview")


@router.get("/all/statistics", response_model=dict)
async def get_interview_statistics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get interview statistics for current user"""
    try:
        user_id = current_user.get("user_id")
        stats = InterviewService.get_interview_statistics(db, user_id)
        return stats
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")


@router.get("/{interview_id}/review")
async def get_interview_review(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get detailed review of interview with all questions, answers, and feedback"""
    try:
        user_id = current_user.get("user_id")
        
        # Get interview
        interview = InterviewService.get_interview(db, interview_id, user_id)
        
        # Build review response
        from app.schemas.schemas import InterviewReviewResponse, QuestionReviewItem, CodingQuestionData
        
        questions_review = []
        for q in interview.questions:
            coding_data = None
            if q.question_type == "coding" and q.problem_statement:
                coding_data = CodingQuestionData(
                    problem_statement=q.problem_statement,
                    expected_approach=q.expected_approach or "",
                    code_solution=q.code_solution or "",
                    difficulty_level=q.difficulty_level or "Medium"
                )
            
            questions_review.append(QuestionReviewItem(
                question_id=q.id,
                question=q.question_text,
                question_type=q.question_type or "soft_skill",
                candidate_answer=q.user_answer,
                ideal_answer=q.ideal_answer,
                score=q.question_score,
                feedback=q.question_feedback,
                coding_data=coding_data
            ))
        
        return InterviewReviewResponse(
            interview_id=interview.id,
            company_name=interview.company_name,
            job_role=interview.job_role,
            overall_score=interview.score,
            questions=questions_review
        )
    
    except Exception as e:
        logger.error(f"Error fetching interview review: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch review: {str(e)}")
