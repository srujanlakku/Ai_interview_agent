"""
Interview service for handling interview operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.models.database import Interview, InterviewSessionQuestion, User
from app.schemas.schemas import InterviewCreate, InterviewQuestionCreate
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.logging_config import get_logger
from app.agents.supervisor_agent import InterviewSupervisorAgent
import json

logger = get_logger(__name__)

supervisor = InterviewSupervisorAgent()


class InterviewService:
    """Service for interview management"""

    @staticmethod
    async def start_agent_interview(db: Session, interview_id: int, user_id: int) -> dict:
        """Initialize the agent-based interview flow"""
        interview = InterviewService.get_interview(db, interview_id, user_id)
        user = db.query(User).filter(User.id == user_id).first()
        
        user_profile = {
            "target_role": interview.job_role or "Software Engineer",
            "target_company": interview.company_name or "Generic",
            "experience_level": "Junior" # Default for now
        }
        
        # Call Supervisor to start
        initial_state = await supervisor.start_interview(user_profile)
        
        # Save state to DB
        interview.agent_state = initial_state
        db.commit()
        
        return initial_state

    @staticmethod
    async def process_agent_step(db: Session, interview_id: int, user_id: int, user_answer: str) -> dict:
        """Process one step of the agent interview"""
        interview = InterviewService.get_interview(db, interview_id, user_id)
        if not interview.agent_state:
            raise ValidationError("Interview agent state not initialized")
            
        user_profile = {
            "target_role": interview.job_role or "Software Engineer",
            "target_company": interview.company_name or "Generic"
        }
        
        # 1. Update the last question asked in DB before processing next
        current_question_data = interview.agent_state.get("current_question", {})
        
        # Call Supervisor to process answer
        new_state = await supervisor.process_answer(
            user_profile=user_profile,
            state=interview.agent_state,
            user_answer=user_answer
        )
        
        # Extract evaluation of the JUST answered question (last in history)
        last_history_item = new_state["history"][-1]
        evaluation = last_history_item.get("evaluation", {})
        
        # 2. Save the question and answer to persistent DB table for review
        from app.models.database import InterviewSessionQuestion
        from app.services.analytics_service import AnalyticsService

        db_question = InterviewSessionQuestion(
            interview_id=interview_id,
            question_text=current_question_data.get("question_text"),
            question_type=current_question_data.get("question_type"),
            user_answer=user_answer,
            question_score=evaluation.get("score"),
            question_feedback=evaluation.get("feedback"),
            difficulty_level=current_question_data.get("difficulty"),
            topic=current_question_data.get("topic"),
            ideal_answer=json.dumps(current_question_data.get("ideal_answer_points", [])),
            # Coding fields if applicable
            problem_statement=current_question_data.get("coding_data", {}).get("problem_statement"),
            expected_approach=current_question_data.get("coding_data", {}).get("expected_approach"),
            code_solution=current_question_data.get("coding_data", {}).get("code_solution")
        )
        db.add(db_question)
        
        # 3. Track question for dashboard
        AnalyticsService.track_question(
            db=db,
            company_name=user_profile["target_company"],
            job_role=user_profile["target_role"],
            question_text=current_question_data.get("question_text"),
            question_type=current_question_data.get("question_type"),
            category=current_question_data.get("topic")
        )

        # Update DB with new state
        interview.agent_state = new_state
        
        # If completed, update main interview fields
        if new_state.get("status") == "completed":
            summary = new_state.get("summary", {})
            interview.score = summary.get("final_score")
            interview.readiness_level = summary.get("readiness_level")
            interview.feedback = summary.get("summary_report")
            
        db.commit()
        db.refresh(interview)
        
        return new_state

    @staticmethod
    def create_interview(db: Session, user_id: int, interview_create: InterviewCreate) -> Interview:
        """Create a new interview"""
        try:
            # Verify user exists
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError(f"User with ID {user_id} not found")

            interview = Interview(
                user_id=user_id,
                interview_type=interview_create.interview_type,
                company_name=interview_create.company_name,
                job_role=interview_create.job_role
            )
            db.add(interview)
            db.commit()
            db.refresh(interview)
            logger.info(f"Interview created: {interview.id} for user {user_id}")
            return interview
        except NotFoundError:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating interview: {str(e)}")
            raise ValidationError(f"Failed to create interview: {str(e)}")

    @staticmethod
    def get_interview(db: Session, interview_id: int, user_id: int) -> Interview:
        """Get an interview by ID"""
        try:
            interview = db.query(Interview).filter(
                Interview.id == interview_id,
                Interview.user_id == user_id
            ).first()
            if not interview:
                raise NotFoundError(f"Interview with ID {interview_id} not found")
            return interview
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error fetching interview: {str(e)}")
            raise NotFoundError("Interview not found")

    @staticmethod
    def get_user_interviews(db: Session, user_id: int, limit: int = 10) -> List[Interview]:
        """Get all interviews for a user"""
        try:
            interviews = db.query(Interview).filter(
                Interview.user_id == user_id
            ).order_by(desc(Interview.created_at)).limit(limit).all()
            return interviews
        except Exception as e:
            logger.error(f"Error fetching user interviews: {str(e)}")
            return []

    @staticmethod
    def add_question_to_interview(db: Session, interview_id: int, user_id: int, 
                                 question_create: InterviewQuestionCreate) -> InterviewSessionQuestion:
        """Add a question to an interview"""
        try:
            # Verify interview exists and belongs to user
            interview = db.query(Interview).filter(
                Interview.id == interview_id,
                Interview.user_id == user_id
            ).first()
            if not interview:
                raise NotFoundError(f"Interview with ID {interview_id} not found")

            question = InterviewSessionQuestion(
                interview_id=interview_id,
                question_text=question_create.question_text,
                difficulty_level=question_create.difficulty_level,
                topic=question_create.topic
            )
            db.add(question)
            db.commit()
            db.refresh(question)
            logger.info(f"Question added to interview {interview_id}")
            return question
        except NotFoundError:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error adding question: {str(e)}")
            raise ValidationError(f"Failed to add question: {str(e)}")

    @staticmethod
    def update_question_response(db: Session, question_id: int, user_answer: str, 
                                score: Optional[float] = None, feedback: Optional[str] = None) -> InterviewSessionQuestion:
        """Update user's answer to a question"""
        try:
            question = db.query(InterviewSessionQuestion).filter(InterviewSessionQuestion.id == question_id).first()
            if not question:
                raise NotFoundError(f"Question with ID {question_id} not found")

            question.user_answer = user_answer
            if score is not None:
                question.question_score = score
            if feedback is not None:
                question.question_feedback = feedback

            db.commit()
            db.refresh(question)
            logger.info(f"Question {question_id} response updated")
            return question
        except NotFoundError:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating question response: {str(e)}")
            raise ValidationError(f"Failed to update response: {str(e)}")

    @staticmethod
    def finalize_interview(db: Session, interview_id: int, user_id: int, 
                          overall_score: float, readiness_level: str, feedback: str,
                          duration_minutes: int) -> Interview:
        """Finalize an interview with scores and feedback"""
        try:
            interview = db.query(Interview).filter(
                Interview.id == interview_id,
                Interview.user_id == user_id
            ).first()
            if not interview:
                raise NotFoundError(f"Interview with ID {interview_id} not found")

            # Validate score
            if not (0 <= overall_score <= 10):
                raise ValidationError("Score must be between 0 and 10")

            interview.score = overall_score
            interview.readiness_level = readiness_level
            interview.feedback = feedback
            interview.duration_minutes = duration_minutes

            db.commit()
            db.refresh(interview)
            logger.info(f"Interview {interview_id} finalized with score {overall_score}")
            return interview
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error finalizing interview: {str(e)}")
            raise ValidationError(f"Failed to finalize interview: {str(e)}")

    @staticmethod
    def get_interview_statistics(db: Session, user_id: int) -> dict:
        """Get interview statistics for a user"""
        try:
            interviews = db.query(Interview).filter(Interview.user_id == user_id).all()
            
            if not interviews:
                return {
                    "total_interviews": 0,
                    "average_score": 0,
                    "highest_score": 0,
                    "lowest_score": 0,
                    "readiness_level": "Not Ready"
                }

            scores = [i.score for i in interviews if i.score is not None]
            
            return {
                "total_interviews": len(interviews),
                "average_score": sum(scores) / len(scores) if scores else 0,
                "highest_score": max(scores) if scores else 0,
                "lowest_score": min(scores) if scores else 0,
                "readiness_level": interviews[-1].readiness_level or "Not Ready"
            }
        except Exception as e:
            logger.error(f"Error calculating interview statistics: {str(e)}")
            return {
                "total_interviews": 0,
                "average_score": 0,
                "highest_score": 0,
                "lowest_score": 0,
                "readiness_level": "Not Ready"
            }
