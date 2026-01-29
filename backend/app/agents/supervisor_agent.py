"""
Interview Supervisor Agent - Orchestrator of the multi-agent interview system.
Coordinates all other agents and manages the session lifecycle.
"""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.agents.question_selector_agent import QuestionSelectorAgent
from app.agents.followup_agent import FollowUpAgent
from app.agents.coding_evaluator_agent import CodingEvaluatorAgent
from app.agents.technical_evaluator_agent import TechnicalEvaluatorAgent
from app.agents.soft_skill_evaluator_agent import SoftSkillEvaluatorAgent
from app.agents.summary_agent import SummaryAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class InterviewSupervisorAgent(BaseAgent):
    """Orchestrator Agent that manages the interview process and delegates to sub-agents"""

    def __init__(self):
        super().__init__("InterviewSupervisorAgent")
        # Sub-agents
        self.selector = QuestionSelectorAgent()
        self.followup_decider = FollowUpAgent()
        self.coding_evaluator = CodingEvaluatorAgent()
        self.tech_evaluator = TechnicalEvaluatorAgent()
        self.soft_skill_evaluator = SoftSkillEvaluatorAgent()
        self.summary_generator = SummaryAgent()
        
        # Configuration
        self.max_questions = 8

    async def start_interview(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Starts a new interview session.
        """
        logger.info(f"Supervisor starting interview for {user_profile.get('target_role')}")
        
        # Initial call to QuestionSelectorAgent
        result = await self.selector.execute(
            role=user_profile.get("target_role", "Software Engineer"),
            company=user_profile.get("target_company", "Generic"),
            interview_stage="Initial",
            previous_questions=[],
            difficulty_level="medium"
        )
        
        return {
            "status": "in_progress",
            "current_question": result,
            "question_count": 1,
            "history": [],
            "performance_context": {
                "overall_sentiment": 0.5,
                "current_difficulty": "medium"
            }
        }

    async def process_answer(self, 
                             user_profile: Dict[str, Any],
                             state: Dict[str, Any], 
                             user_answer: str) -> Dict[str, Any]:
        """
        Processes the candidate's answer and determines next steps.
        """
        current_question = state.get("current_question")
        question_type = current_question.get("question_type", "technical")
        
        # 1. Evaluate the answer based on type
        evaluation = {}
        if question_type == "coding":
            evaluation = await self.coding_evaluator.execute(
                problem=current_question.get("question_text"),
                solution=user_answer,
                expected_approach=current_question.get("coding_data", {}).get("expected_approach", ""),
                ideal_solution=current_question.get("coding_data", {}).get("code_solution", "")
            )
        elif question_type == "technical":
            evaluation = await self.tech_evaluator.execute(
                question=current_question.get("question_text"),
                answer=user_answer,
                ideal_answer_points=current_question.get("ideal_answer_points", [])
            )
        else: # soft_skill
            evaluation = await self.soft_skill_evaluator.execute(
                question=current_question.get("question_text"),
                answer=user_answer
            )
            
        # 2. Store in history
        history_item = {
            "question": current_question,
            "answer": user_answer,
            "evaluation": evaluation
        }
        state["history"].append(history_item)
        
        # 3. Decide on follow-up or next question
        followup_decision = await self.followup_decider.execute(
            question=current_question.get("question_text"),
            answer=user_answer,
            performance_context=state.get("performance_context")
        )
        
        # 4. Update state variables
        state["question_count"] += 1
        
        # Check if we should end
        if state["question_count"] > self.max_questions:
            return await self.end_interview(user_profile, state)
            
        # 5. Determine next question
        if followup_decision.get("decision") == "follow_up":
            # Direct follow-up
            next_question = {
                "question_text": followup_decision.get("follow_up_question"),
                "question_type": question_type, # Keep same type for follow-up
                "topic": current_question.get("topic"),
                "is_follow_up": True
            }
        else:
            # New question selection
            new_difficulty = state["performance_context"].get("current_difficulty", "medium")
            if followup_decision.get("decision") == "increase_difficulty":
                new_difficulty = "hard" if new_difficulty == "medium" else "hard"
            elif evaluation.get("score", 5) < 4:
                new_difficulty = "easy"
                
            state["performance_context"]["current_difficulty"] = new_difficulty
            
            next_question = await self.selector.execute(
                role=user_profile.get("target_role"),
                company=user_profile.get("target_company"),
                interview_stage="Ongoing",
                previous_questions=[h["question"] for h in state["history"]],
                difficulty_level=new_difficulty
            )
            
        state["current_question"] = next_question
        return state

    async def end_interview(self, user_profile: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Finalizes the interview and generates the summary.
        """
        logger.info("Supervisor ending interview and generating summary")
        
        summary = await self.summary_generator.execute(
            interview_data={
                "role": user_profile.get("target_role"),
                "company": user_profile.get("target_company"),
                "duration": len(state["history"])
            },
            all_evaluations=[h["evaluation"] for h in state["history"]]
        )
        
        state["status"] = "completed"
        state["summary"] = summary
        return state

    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Generic execute implementation for BaseAgent compatibility"""
        pass
