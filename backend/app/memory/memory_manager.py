"""
Bounded Memory Manager for the AI Interview Agent.
Manages conversational state with memory limits to prevent token overflow.
"""
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from app.schemas.question_schema import InterviewQuestion, QAPair


@dataclass
class PerformanceMetrics:
    """Tracks interview performance metrics."""
    total_score: float = 0.0
    question_count: int = 0
    technical_scores: List[float] = field(default_factory=list)
    behavioral_scores: List[float] = field(default_factory=list)
    coding_scores: List[float] = field(default_factory=list)
    
    @property
    def average_score(self) -> float:
        """Calculate average score."""
        if self.question_count == 0:
            return 0.0
        return self.total_score / self.question_count
    
    @property
    def technical_average(self) -> float:
        """Calculate technical questions average."""
        if not self.technical_scores:
            return 0.0
        return sum(self.technical_scores) / len(self.technical_scores)
    
    @property
    def behavioral_average(self) -> float:
        """Calculate behavioral questions average."""
        if not self.behavioral_scores:
            return 0.0
        return sum(self.behavioral_scores) / len(self.behavioral_scores)
    
    @property
    def coding_average(self) -> float:
        """Calculate coding questions average."""
        if not self.coding_scores:
            return 0.0
        return sum(self.coding_scores) / len(self.coding_scores)
    
    def add_score(self, score: float, question_type: str) -> None:
        """Add a score for a question."""
        self.total_score += score
        self.question_count += 1
        
        if question_type == "technical" or question_type == "system_design":
            self.technical_scores.append(score)
        elif question_type == "behavioral":
            self.behavioral_scores.append(score)
        elif question_type == "coding":
            self.coding_scores.append(score)


@dataclass
class InterviewState:
    """Complete state for an interview session."""
    session_id: str
    role: str
    experience_level: str
    company: Optional[str] = None
    current_question_idx: int = 0
    current_difficulty: str = "medium"
    history: List[QAPair] = field(default_factory=list)
    compressed_history: str = ""
    asked_question_ids: List[str] = field(default_factory=list)
    asked_topics: List[str] = field(default_factory=list)
    performance: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    started_at: datetime = field(default_factory=datetime.now)
    status: str = "in_progress"  # in_progress, completed, abandoned
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "role": self.role,
            "experience_level": self.experience_level,
            "company": self.company,
            "current_question_idx": self.current_question_idx,
            "current_difficulty": self.current_difficulty,
            "history_count": len(self.history),
            "asked_questions_count": len(self.asked_question_ids),
            "average_score": self.performance.average_score,
            "status": self.status,
        }


class MemoryManager:
    """
    Manages bounded conversational memory for interview sessions.
    
    Features:
    - Maintains last N interactions in full detail
    - Compresses older interactions to prevent token overflow
    - Tracks performance metrics
    - Provides context summarization
    """
    
    def __init__(self, max_recent_history: int = 5):
        """
        Initialize the memory manager.
        
        Args:
            max_recent_history: Maximum number of recent Q&A pairs to keep in full detail
        """
        self.max_recent_history = max_recent_history
        self._sessions: Dict[str, InterviewState] = {}
    
    def create_session(
        self,
        role: str,
        experience_level: str,
        company: Optional[str] = None,
        initial_difficulty: str = "medium",
    ) -> InterviewState:
        """
        Create a new interview session.
        
        Args:
            role: Target role for the interview
            experience_level: Experience level (fresher, mid, senior)
            company: Optional target company
            initial_difficulty: Starting difficulty level
            
        Returns:
            New InterviewState instance
        """
        session_id = str(uuid.uuid4())[:8]
        state = InterviewState(
            session_id=session_id,
            role=role,
            experience_level=experience_level,
            company=company,
            current_difficulty=initial_difficulty,
        )
        self._sessions[session_id] = state
        return state
    
    def get_session(self, session_id: str) -> Optional[InterviewState]:
        """Get an existing session by ID."""
        return self._sessions.get(session_id)
    
    def add_interaction(
        self,
        state: InterviewState,
        question: InterviewQuestion,
        answer: str,
        score: float,
        feedback: str,
        strengths: List[str],
        weaknesses: List[str],
    ) -> None:
        """
        Add a Q&A interaction to the session history.
        
        Args:
            state: Current interview state
            question: The question that was asked
            answer: User's answer
            score: Score for the answer (0-10)
            feedback: Feedback text
            strengths: List of strengths identified
            weaknesses: List of weaknesses identified
        """
        # Create Q&A pair
        qa_pair = QAPair(
            question=question,
            answer=answer,
            score=score,
            feedback=feedback,
            strengths=strengths,
            weaknesses=weaknesses,
        )
        
        # Add to history
        state.history.append(qa_pair)
        
        # Track question and topic
        if question.question_id:
            state.asked_question_ids.append(question.question_id)
        state.asked_topics.append(question.topic)
        
        # Update performance metrics
        state.performance.add_score(score, question.question_type)
        
        # Increment question counter
        state.current_question_idx += 1
        
        # Compress old history if needed
        self._compress_history_if_needed(state)
        
        # Adjust difficulty based on performance
        self._adjust_difficulty(state, score)
    
    def _compress_history_if_needed(self, state: InterviewState) -> None:
        """Compress older history entries to save tokens."""
        if len(state.history) <= self.max_recent_history:
            return
        
        # Number of entries to compress
        entries_to_compress = len(state.history) - self.max_recent_history
        
        # Create summary of old entries
        old_entries = state.history[:entries_to_compress]
        summary_parts = []
        
        for qa in old_entries:
            summary_parts.append(
                f"Q: {qa.question.topic} ({qa.question.question_type}) - "
                f"Score: {qa.score:.1f}/10"
            )
        
        # Add to compressed history
        if state.compressed_history:
            state.compressed_history += "\n"
        state.compressed_history += "\n".join(summary_parts)
        
        # Keep only recent history
        state.history = state.history[entries_to_compress:]
    
    def _adjust_difficulty(self, state: InterviewState, latest_score: float) -> None:
        """Adjust difficulty based on recent performance."""
        recent_scores = [qa.score for qa in state.history if qa.score is not None][-3:]
        
        if not recent_scores:
            return
        
        avg_recent = sum(recent_scores) / len(recent_scores)
        
        # Adjust based on performance
        if avg_recent >= 8.0 and state.current_difficulty != "hard":
            if state.current_difficulty == "easy":
                state.current_difficulty = "medium"
            else:
                state.current_difficulty = "hard"
        elif avg_recent < 5.0 and state.current_difficulty != "easy":
            if state.current_difficulty == "hard":
                state.current_difficulty = "medium"
            else:
                state.current_difficulty = "easy"
    
    def get_context_summary(self, state: InterviewState) -> str:
        """
        Get a summary of the interview context for LLM prompts.
        
        Args:
            state: Current interview state
            
        Returns:
            Context summary string
        """
        summary_parts = [
            f"Interview Session: {state.session_id}",
            f"Role: {state.role}",
            f"Experience Level: {state.experience_level}",
            f"Current Difficulty: {state.current_difficulty}",
            f"Questions Asked: {state.current_question_idx}",
            f"Average Score: {state.performance.average_score:.1f}/10",
        ]
        
        if state.company:
            summary_parts.insert(2, f"Target Company: {state.company}")
        
        # Add compressed history summary
        if state.compressed_history:
            summary_parts.append(f"\nPrevious Topics Covered:\n{state.compressed_history}")
        
        # Add recent history
        if state.history:
            summary_parts.append("\nRecent Interactions:")
            for i, qa in enumerate(state.history[-3:], 1):
                summary_parts.append(
                    f"{i}. Topic: {qa.question.topic}, "
                    f"Type: {qa.question.question_type}, "
                    f"Score: {qa.score:.1f}/10"
                )
        
        return "\n".join(summary_parts)
    
    def get_recent_weaknesses(self, state: InterviewState, limit: int = 5) -> List[str]:
        """Get the most recent weaknesses identified."""
        weaknesses = []
        for qa in reversed(state.history):
            weaknesses.extend(qa.weaknesses)
            if len(weaknesses) >= limit:
                break
        return weaknesses[:limit]
    
    def get_recent_strengths(self, state: InterviewState, limit: int = 5) -> List[str]:
        """Get the most recent strengths identified."""
        strengths = []
        for qa in reversed(state.history):
            strengths.extend(qa.strengths)
            if len(strengths) >= limit:
                break
        return strengths[:limit]
    
    def should_end_interview(
        self,
        state: InterviewState,
        max_questions: int = 8,
    ) -> bool:
        """
        Determine if the interview should end.
        
        Args:
            state: Current interview state
            max_questions: Maximum number of questions
            
        Returns:
            True if interview should end
        """
        return state.current_question_idx >= max_questions
    
    def finalize_session(self, state: InterviewState) -> Dict[str, Any]:
        """
        Finalize an interview session and return summary data.
        
        Args:
            state: Current interview state
            
        Returns:
            Dictionary containing final session data
        """
        state.status = "completed"
        
        return {
            "session_id": state.session_id,
            "role": state.role,
            "experience_level": state.experience_level,
            "company": state.company,
            "total_questions": state.current_question_idx,
            "final_score": state.performance.average_score,
            "technical_score": state.performance.technical_average,
            "behavioral_score": state.performance.behavioral_average,
            "coding_score": state.performance.coding_average,
            "topics_covered": list(set(state.asked_topics)),
            "all_strengths": self.get_recent_strengths(state, 10),
            "all_weaknesses": self.get_recent_weaknesses(state, 10),
            "history": [
                {
                    "question": qa.question.question_text,
                    "topic": qa.question.topic,
                    "type": qa.question.question_type,
                    "answer": qa.answer[:200] + "..." if len(qa.answer) > 200 else qa.answer,
                    "score": qa.score,
                    "feedback": qa.feedback,
                }
                for qa in state.history
            ],
        }


# Singleton instance
_memory_manager: Optional[MemoryManager] = None


def get_memory_manager() -> MemoryManager:
    """Get or create the singleton memory manager instance."""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager()
    return _memory_manager
