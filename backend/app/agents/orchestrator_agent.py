"""
Orchestrator Agent - Controls interview flow, difficulty, and termination.
Coordinates between other agents and manages session state.
"""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import uuid
from datetime import datetime

from app.agents.topic_tracker import TopicTracker, TopicCategory, get_topic_tracker
from app.agents.question_selector_agent import QuestionSelectorAgent
from app.agents.evaluation_agent import EvaluationAgent
from app.agents.reflection_agent import ReflectionAgent
from app.agents.adaptive_termination_agent import AdaptiveTerminationAgent
from app.agents.company_aware_agent import CompanyAwareAgent
from app.agents.learning_mode_agent import LearningModeAgent
from app.agents.replay_agent import ReplayAgent
from app.prompts.prompt_manager import get_prompt_manager
from app.security.input_guardrails import get_safe_processor


class InterviewState(Enum):
    """Current state of the interview."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


@dataclass
class InterviewSession:
    """Represents a complete interview session."""
    session_id: str
    candidate_name: str
    role: str
    experience_level: str
    company: Optional[str] = None
    
    # Interview flow
    current_state: InterviewState = InterviewState.NOT_STARTED
    current_question_num: int = 0
    max_questions: int = 8
    current_difficulty: str = "medium"
    
    # Topic tracking
    topic_tracker: Optional[TopicTracker] = None
    asked_question_ids: List[str] = None
    covered_topics: List[str] = None
    
    # Performance tracking
    scores: List[float] = None
    strengths: List[str] = None
    weaknesses: List[str] = None
    
    # Agentic addons state
    reflection_history: List[Dict[str, Any]] = None
    termination_reason: Optional[str] = None
    company_context: Optional[Dict[str, Any]] = None
    learning_context: Optional[Dict[str, Any]] = None
    weaknesses: List[str] = None
    
    # Resume data
    resume_skills: List[str] = None
    resume_projects: List[str] = None
    
    # Session metadata
    started_at: datetime = None
    ended_at: datetime = None
    
    def __post_init__(self):
        if self.asked_question_ids is None:
            self.asked_question_ids = []
        if self.covered_topics is None:
            self.covered_topics = []
        if self.scores is None:
            self.scores = []
        if self.strengths is None:
            self.strengths = []
        if self.weaknesses is None:
            self.weaknesses = []
        if self.resume_skills is None:
            self.resume_skills = []
        if self.resume_projects is None:
            self.resume_projects = []
        if self.started_at is None:
            self.started_at = datetime.now()
        if self.topic_tracker is None:
            self.topic_tracker = get_topic_tracker()
            self.topic_tracker.create_coverage(self.session_id, self.role)
    
    @property
    def average_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)
    
    @property
    def is_complete(self) -> bool:
        return self.current_question_num >= self.max_questions
    
    @property
    def progress_percentage(self) -> float:
        return min(100.0, (self.current_question_num / self.max_questions) * 100)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for persistence."""
        return {
            "session_id": self.session_id,
            "candidate_name": self.candidate_name,
            "role": self.role,
            "experience_level": self.experience_level,
            "company": self.company,
            "current_state": self.current_state.value,
            "current_question_num": self.current_question_num,
            "max_questions": self.max_questions,
            "current_difficulty": self.current_difficulty,
            "average_score": self.average_score,
            "total_questions": len(self.scores),
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "final_score": self.average_score,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
        }


class OrchestratorAgent:
    """
    Orchestrates the entire interview process with advanced agentic capabilities.
    Coordinates between all agents and manages intelligent interview flow.
    """
    
    def __init__(self):
        self.sessions: Dict[str, InterviewSession] = {}
        
        # Core agents
        self.question_agent = QuestionSelectorAgent()
        self.evaluation_agent = EvaluationAgent()
        self.topic_tracker = get_topic_tracker()
        
        # Advanced agentic addons (initialized as needed)
        self._reflection_agent = None
        self._termination_agent = None
        self._company_agent = None
        self._learning_agent = None
        self._replay_agent = None
        
        # Infrastructure
        self.prompt_manager = get_prompt_manager()
        self.safe_processor = get_safe_processor()
    
    def create_session(
        self,
        candidate_name: str,
        role: str,
        experience_level: str,
        company: Optional[str] = None,
        max_questions: int = 8,
        resume_skills: Optional[List[str]] = None,
        resume_projects: Optional[List[str]] = None
    ) -> str:
        """Create a new interview session with advanced agentic capabilities."""
        session_id = str(uuid.uuid4())[:8]
        
        # Initialize session with default values
        session = InterviewSession(
            session_id=session_id,
            candidate_name=candidate_name,
            role=role,
            experience_level=experience_level,
            company=company,
            max_questions=max_questions,
            current_state=InterviewState.IN_PROGRESS,
            asked_question_ids=[],
            covered_topics=[],
            scores=[],
            strengths=[],
            weaknesses=[],
            reflection_history=[],
            resume_skills=resume_skills or [],
            resume_projects=resume_projects or []
        )
        
        self.sessions[session_id] = session
        
        # Initialize agentic addons for this session
        if self._reflection_agent:
            self._reflection_agent.reset()
        if self._termination_agent:
            self._termination_agent.reset()
        if self._learning_agent:
            self._learning_agent.reset()
        if self._replay_agent:
            self._replay_agent.reset()
        
        # Set company context
        if company:
            if not self._company_agent:
                self._company_agent = CompanyAwareAgent()
            company_profile = self._company_agent.set_company_context(company, role)
            session.company_context = company_profile.to_dict()
        
        # Initialize learning context
        session.learning_context = {
            "candidate_name": candidate_name,
            "role": role,
            "experience_level": experience_level,
            "company": company,
            "interview_date": datetime.now().isoformat()
        }
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """Get an existing session."""
        return self.sessions.get(session_id)
    
    def get_next_question_context(self, session_id: str) -> Dict[str, Any]:
        """Get context for selecting the next question."""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Determine next topic based on coverage
        next_category = self.topic_tracker.suggest_next_topic(session_id)
        if next_category:
            prefer_type = next_category.value.lower().replace(" & ", "_").replace(" ", "_")
        else:
            prefer_type = None
        
        # Suggest difficulty based on topic performance
        difficulty = session.current_difficulty
        if next_category:
            difficulty = self.topic_tracker.suggest_difficulty(session_id, next_category)
        
        # Get resume skills if available (this would come from session state)
        resume_skills = getattr(session, 'resume_skills', [])
        resume_projects = getattr(session, 'resume_projects', [])
        
        context = {
            "role": session.role,
            "experience_level": session.experience_level,
            "difficulty": difficulty,
            "asked_question_ids": session.asked_question_ids,
            "asked_topics": session.covered_topics,
            "prefer_type": prefer_type,
            "company": session.company,
        }
        
        # Add resume data if available
        if resume_skills:
            context["resume_skills"] = resume_skills
        if resume_projects:
            context["resume_projects"] = resume_projects
        
        return context
    
    async def get_next_question(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the next question for the interview."""
        session = self.get_session(session_id)
        if not session or session.is_complete:
            return None
        
        context = self.get_next_question_context(session_id)
        
        # Use question selector agent
        question = await self.question_agent.execute(**context)
        
        if question:
            # Update session state
            session.current_question_num += 1
            
            # Record question in topic tracker
            topic = question.get("topic", "General")
            category = self.topic_tracker.map_topic_to_category(topic)
            question_id = question.get("question_id", f"gen_{session.current_question_num}")
            
            self.topic_tracker.get_coverage(session_id).record_question(
                topic=topic,
                category=category,
                question_id=question_id,
                question_text=question.get("question_text", question.get("text", ""))
            )
            
            session.asked_question_ids.append(question_id)
            session.covered_topics.append(topic)
        
        return question
    
    async def process_answer(self, session_id: str, question: Dict[str, Any], answer: str) -> Dict[str, Any]:
        """Process a candidate's answer with advanced agentic intelligence."""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # 1. Safety validation
        is_safe, sanitized_answer, safety_message = await self.safe_processor.process_interview_answer(
            answer, session_id
        )
        
        if not is_safe:
            return {
                "status": "safety_violation",
                "message": safety_message,
                "next_action": "retry"
            }
        
        # 2. Enhanced evaluation with company context
        evaluation_context = {
            "question": question.get("question_text", question.get("text", "")),
            "answer": sanitized_answer,
            "question_type": question.get("question_type", "technical"),
            "ideal_answer_points": question.get("ideal_answer_points", []),
            "experience_level": session.experience_level
        }
        
        # Apply company-specific evaluation criteria (filter unsupported parameters)
        if session.company_context and self._company_agent:
            adapted_criteria = self._company_agent.adapt_evaluation_criteria(evaluation_context)
            # Filter out parameters that EvaluationAgent doesn't support
            supported_params = {k: v for k, v in adapted_criteria.items() 
                              if k in ["question", "answer", "question_type", "ideal_answer_points", "experience_level"]}
            evaluation_context.update(supported_params)
        
        evaluation = await self.evaluation_agent.execute(**evaluation_context)
        
        # 3. Self-reflection on interaction
        current_context = {
            "current_difficulty": session.current_difficulty,
            "covered_topics": session.covered_topics,
            "performance_trend": self._analyze_performance_trend(session.scores),
            "question_count": session.current_question_num,
            "max_questions": session.max_questions
        }
        
        # Use direct method call instead of agent instantiation
        from backend.app.agents.reflection_agent import ReflectionAgent
        reflection_agent = ReflectionAgent.__new__(ReflectionAgent)  # Create without calling __init__
        
        reflection = await reflection_agent.reflect_on_interaction(
            question=question.get("question_text", question.get("text", "")),
            answer=sanitized_answer,
            evaluation=evaluation,
            current_context=current_context
        )
        
        # Store reflection
        session.reflection_history.append(reflection.to_dict())
        
        # 4. Update session state
        score = evaluation.get("score", 5.0)
        session.scores.append(score)
        
        # Update topic tracker with score
        topic = question.get("topic", "General")
        category = self.topic_tracker.map_topic_to_category(topic)
        self.topic_tracker.get_coverage(session_id).record_score(category, score)
        
        # Update strengths and weaknesses
        if evaluation.get("strengths"):
            session.strengths.extend(evaluation["strengths"][:2])
        if evaluation.get("weaknesses"):
            session.weaknesses.extend(evaluation["weaknesses"][:2])
        elif evaluation.get("improvement_suggestions"):
            session.weaknesses.extend(evaluation["improvement_suggestions"][:2])
        
        # Track question
        question_id = question.get("question_id", f"q{session.current_question_num}")
        session.asked_question_ids.append(question_id)
        session.covered_topics.append(topic)
        
        # 5. Adaptive termination check
        # Use direct method call for termination agent
        from backend.app.agents.adaptive_termination_agent import AdaptiveTerminationAgent
        termination_agent = AdaptiveTerminationAgent.__new__(AdaptiveTerminationAgent)
        
        termination_result = termination_agent.should_terminate(
            scores=session.scores,
            question_count=session.current_question_num,
            max_questions=session.max_questions,
            current_performance=score,
            context=current_context
        )
        
        if termination_result.decision == "terminate":
            session.current_state = InterviewState.COMPLETED
            session.termination_reason = termination_result.reason.value
            return {
                "status": "terminated",
                "evaluation": evaluation,
                "reflection": reflection.to_dict(),
                "termination": termination_result.to_dict(),
                "final_score": sum(session.scores) / len(session.scores) if session.scores else 0
            }
        
        # 6. Determine next action based on reflection
        next_action = self._determine_next_action_from_reflection(reflection, session)
        
        # 7. Update difficulty based on reflection
        if reflection.suggested_difficulty:
            session.current_difficulty = reflection.suggested_difficulty
        
        return {
            "status": "processed",
            "evaluation": evaluation,
            "reflection": reflection.to_dict(),
            "next_action": next_action,
            "current_score": score,
            "average_score": sum(session.scores) / len(session.scores) if session.scores else 0,
            "termination_check": termination_result.to_dict()
        }
    
    def _determine_next_action_from_reflection(self, reflection, session: InterviewSession) -> str:
        """Determine next action based on reflection results."""
        action_map = {
            "deeper_probing": "follow_up_question",
            "topic_switch": "new_topic_question",
            "difficulty_adjustment": "adjusted_question",
            "maintain_current": "next_question"
        }
        
        return action_map.get(reflection.next_action.value, "next_question")
    
    def _analyze_performance_trend(self, scores: List[float]) -> str:
        """Analyze performance trend direction."""
        if len(scores) < 3:
            return "insufficient_data"
        
        # Simple trend analysis
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg + 0.5:
            return "improving"
        elif second_avg < first_avg - 0.5:
            return "declining"
        else:
            return "stable"
    
    async def evaluate_answer(
        self,
        session_id: str,
        question: Dict[str, Any],
        answer: str
    ) -> Dict[str, Any]:
        """Evaluate an answer and update session state."""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Use evaluation agent
        evaluation = await self.evaluation_agent.execute(
            question=question.get("question_text", question.get("text", "")),
            answer=answer,
            question_type=question.get("question_type", "technical"),
            ideal_answer_points=question.get("ideal_answer_points", []),
            experience_level=session.experience_level,
        )
        
        # Update session with evaluation results
        score = evaluation.get("score", 5.0)
        session.scores.append(score)
        
        # Update topic tracker with score
        topic = question.get("topic", "General")
        category = self.topic_tracker.map_topic_to_category(topic)
        self.topic_tracker.get_coverage(session_id).record_score(category, score)
        
        # Update strengths and weaknesses
        if evaluation.get("strengths"):
            session.strengths.extend(evaluation["strengths"])
        if evaluation.get("weaknesses"):
            session.weaknesses.extend(evaluation["weaknesses"])
        elif evaluation.get("improvement_suggestions"):
            session.weaknesses.extend(evaluation["improvement_suggestions"])
        
        # Adjust difficulty based on performance
        if len(session.scores) >= 2:
            recent_avg = sum(session.scores[-2:]) / 2
            if recent_avg >= 8.0:
                session.current_difficulty = "hard"
            elif recent_avg <= 4.0:
                session.current_difficulty = "easy"
            else:
                session.current_difficulty = "medium"
        
        return evaluation
    
    def should_end_interview(self, session_id: str) -> bool:
        """Determine if the interview should end."""
        session = self.get_session(session_id)
        if not session:
            return True
        
        # End if max questions reached
        if session.is_complete:
            session.current_state = InterviewState.COMPLETED
            session.ended_at = datetime.now()
            return True
        
        return False
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of the session."""
        session = self.get_session(session_id)
        if not session:
            return {}
        
        coverage = self.topic_tracker.get_coverage(session_id)
        
        return {
            "session_id": session.session_id,
            "candidate_name": session.candidate_name,
            "role": session.role,
            "experience_level": session.experience_level,
            "company": session.company,
            "current_question_num": session.current_question_num,
            "max_questions": session.max_questions,
            "current_difficulty": session.current_difficulty,
            "average_score": session.average_score,
            "progress_percentage": session.progress_percentage,
            "is_complete": session.is_complete,
            "topic_coverage": coverage.to_summary() if coverage else {},
            "strengths": session.strengths,
            "weaknesses": session.weaknesses,
        }
    
    def finalize_session(self, session_id: str) -> Dict[str, Any]:
        """Finalize the session and return complete results."""
        session = self.get_session(session_id)
        if not session:
            return {}
        
        session.current_state = InterviewState.COMPLETED
        if not session.ended_at:
            session.ended_at = datetime.now()
        
        # Get comprehensive summary
        summary = self.get_session_summary(session_id)
        
        # Add detailed results
        coverage = self.topic_tracker.get_coverage(session_id)
        if coverage:
            summary["detailed_coverage"] = coverage.to_summary()
        
        return summary
    
    def abort_session(self, session_id: str) -> None:
        """Abort the session."""
        session = self.get_session(session_id)
        if session:
            session.current_state = InterviewState.ABANDONED
            session.ended_at = datetime.now()
    
    def cleanup_session(self, session_id: str) -> None:
        """Remove session from memory."""
        if session_id in self.sessions:
            del self.sessions[session_id]