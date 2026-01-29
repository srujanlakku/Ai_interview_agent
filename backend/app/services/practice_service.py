"""
Practice Service - Manages educational practice sessions.
"""
import uuid
from typing import Dict, Any, List, Optional
from app.agents.practice_agent import PracticeAgent
from app.utils.logging_config import get_logger

logger = get_logger(__name__)
practice_agent = PracticeAgent()

# Simple in-memory storage for practice sessions (ephemeral)
# In production, this might be Redis or a "practice_sessions" DB table
practice_sessions: Dict[str, Dict[str, Any]] = {}

class PracticeService:
    """Service for handling skill practice sessions"""

    @staticmethod
    async def start_session(skill_category: str, level: str) -> Dict[str, Any]:
        """Start a new practice session"""
        session_id = str(uuid.uuid4())
        
        # Get first step
        step_data = await practice_agent.get_next_step(skill_category, level)
        
        # Initialize session state
        session_state = {
            "session_id": session_id,
            "skill_category": skill_category,
            "level": level,
            "current_step": step_data,
            "history": []
        }
        
        practice_sessions[session_id] = session_state
        
        return {
            "session_id": session_id,
            "step": step_data
        }

    @staticmethod
    async def submit_answer(session_id: str, user_answer: str) -> Dict[str, Any]:
        """Submit answer for the current practice step"""
        session = practice_sessions.get(session_id)
        if not session:
            raise ValueError("Session not found")
            
        current_step = session["current_step"]
        
        # Evaluate
        feedback = await practice_agent.evaluate_answer(
            concept=current_step["concept"],
            question=current_step["practice_question"],
            user_answer=user_answer
        )
        
        # Update history
        session["history"].append({
            "step": current_step,
            "user_answer": user_answer,
            "feedback": feedback
        })
        
        return feedback

    @staticmethod
    async def get_next_step(session_id: str) -> Dict[str, Any]:
        """Get the next practice step in the session"""
        session = practice_sessions.get(session_id)
        if not session:
            raise ValueError("Session not found")
            
        # Get next step from agent
        step_data = await practice_agent.get_next_step(
            skill_category=session["skill_category"],
            level=session["level"],
            history=session["history"]
        )
        
        session["current_step"] = step_data
        
        return step_data
