"""
Adaptive Interview Termination System - Intelligently ends interviews early for 
clear performance signals or extends for borderline cases with clear explanations.

This system makes the interview process more efficient and humane by recognizing
when sufficient information has been gathered or when additional assessment is needed.
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import statistics
from datetime import datetime
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class TerminationReason(Enum):
    """Reasons for interview termination."""
    STRONG_PERFORMANCE = "strong_performance"      # Clearly interview-ready candidate
    WEAK_PERFORMANCE = "weak_performance"         # Clearly not ready, no point continuing
    BORDERLINE_CASE = "borderline_case"           # Performance is ambiguous, need more data
    MAX_QUESTIONS_REACHED = "max_questions"       # Reached configured question limit
    USER_REQUESTED = "user_requested"             # Candidate requested to end
    TECHNICAL_ISSUE = "technical_issue"           # System issue forced termination


class TerminationDecision(Enum):
    """Decision about whether to terminate interview."""
    TERMINATE = "terminate"
    CONTINUE = "continue"
    EXTEND = "extend"  # Continue beyond normal limits for borderline cases


@dataclass
class TerminationResult:
    """Result of termination analysis."""
    decision: TerminationDecision
    reason: TerminationReason
    confidence: float  # 0.0 to 1.0
    explanation: str
    recommended_action: str
    estimated_questions_remaining: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "decision": self.decision.value,
            "reason": self.reason.value,
            "confidence": round(self.confidence, 2),
            "explanation": self.explanation,
            "recommended_action": self.recommended_action,
            "estimated_questions_remaining": self.estimated_questions_remaining
        }


class AdaptiveTerminationAgent:
    """
    Agent that determines optimal interview termination timing.
    
    Features:
    - Early termination for clearly strong or weak candidates
    - Extension for borderline cases needing more data
    - Clear, empathetic explanations to candidates
    - Performance trend analysis
    - Configurable thresholds
    """
    
    # Configuration thresholds
    STRONG_PERFORMANCE_THRESHOLD = 8.0    # Average score for early termination
    WEAK_PERFORMANCE_THRESHOLD = 4.0      # Average score for early termination  
    BORDERLINE_LOWER_BOUND = 5.5          # Lower bound for borderline extension
    BORDERLINE_UPPER_BOUND = 7.5          # Upper bound for borderline extension
    MIN_QUESTIONS_BEFORE_TERMINATION = 3  # Minimum questions before considering termination
    MAX_EXTENSION_QUESTIONS = 3           # Maximum additional questions for extension
    
    def __init__(self):
        self.termination_history: List[TerminationResult] = []
    
    def should_terminate(
        self,
        scores: List[float],
        question_count: int,
        max_questions: int,
        current_performance: float,
        context: Dict[str, Any]
    ) -> TerminationResult:
        """
        Determine if interview should be terminated.
        
        Args:
            scores: List of all scores so far
            question_count: Number of questions asked
            max_questions: Maximum configured questions
            current_performance: Current question score
            context: Additional context (candidate info, interview goals, etc.)
            
        Returns:
            TerminationResult with decision and explanation
        """
        # Need minimum data before making termination decisions
        if question_count < self.MIN_QUESTIONS_BEFORE_TERMINATION:
            return TerminationResult(
                decision=TerminationDecision.CONTINUE,
                reason=TerminationReason.MAX_QUESTIONS_REACHED,
                confidence=1.0,
                explanation=f"Need at least {self.MIN_QUESTIONS_BEFORE_TERMINATION} questions for reliable assessment",
                recommended_action="Continue with interview"
            )
        
        # Calculate performance metrics
        avg_score = statistics.mean(scores) if scores else current_performance
        score_variance = statistics.variance(scores) if len(scores) > 1 else 0
        performance_trend = self._analyze_trend(scores)
        
        # Check for strong performance termination
        if self._should_terminate_strong(avg_score, question_count, max_questions):
            result = self._create_strong_termination_result(avg_score, question_count)
        
        # Check for weak performance termination
        elif self._should_terminate_weak(avg_score, question_count, max_questions):
            result = self._create_weak_termination_result(avg_score, question_count)
        
        # Check for borderline case extension
        elif self._should_extend_borderline(avg_score, question_count, max_questions):
            result = self._create_borderline_extension_result(
                avg_score, question_count, max_questions, performance_trend
            )
        
        # Check if reached maximum questions
        elif question_count >= max_questions:
            result = self._create_max_questions_result(avg_score)
        
        # Default: continue
        else:
            result = self._create_continue_result(avg_score, question_count, max_questions)
        
        # Store result
        self.termination_history.append(result)
        
        logger.info(
            f"Termination decision: {result.decision.value} | "
            f"Reason: {result.reason.value} | Confidence: {result.confidence:.2f}"
        )
        
        return result
    
    def _should_terminate_strong(self, avg_score: float, question_count: int, max_questions: int) -> bool:
        """Check if candidate shows strong enough performance for early termination."""
        # Must exceed threshold and have consistent performance
        return (avg_score >= self.STRONG_PERFORMANCE_THRESHOLD and 
                question_count >= self.MIN_QUESTIONS_BEFORE_TERMINATION and
                question_count <= max_questions - 2)  # Leave room for confirmation
    
    def _should_terminate_weak(self, avg_score: float, question_count: int, max_questions: int) -> bool:
        """Check if candidate shows weak performance warranting early termination."""
        return (avg_score <= self.WEAK_PERFORMANCE_THRESHOLD and 
                question_count >= self.MIN_QUESTIONS_BEFORE_TERMINATION)
    
    def _should_extend_borderline(self, avg_score: float, question_count: int, max_questions: int) -> bool:
        """Check if performance is borderline and needs more questions."""
        is_borderline = (self.BORDERLINE_LOWER_BOUND <= avg_score <= self.BORDERLINE_UPPER_BOUND)
        within_extension_limit = question_count < max_questions + self.MAX_EXTENSION_QUESTIONS
        return is_borderline and within_extension_limit
    
    def _analyze_trend(self, scores: List[float]) -> str:
        """Analyze performance trend direction."""
        if len(scores) < 3:
            return "insufficient_data"
        
        # Simple trend analysis - compare first half vs second half
        mid = len(scores) // 2
        first_avg = statistics.mean(scores[:mid])
        second_avg = statistics.mean(scores[mid:])
        
        if second_avg > first_avg + 0.5:
            return "improving"
        elif second_avg < first_avg - 0.5:
            return "declining"
        else:
            return "stable"
    
    def _create_strong_termination_result(self, avg_score: float, question_count: int) -> TerminationResult:
        """Create termination result for strong performers."""
        explanation = (
            f"Outstanding performance! Your average score of {avg_score:.1f}/10 "
            f"demonstrates exceptional technical knowledge and readiness. "
            f"After {question_count} questions, we have sufficient confidence "
            f"in your abilities to provide a comprehensive assessment."
        )
        
        return TerminationResult(
            decision=TerminationDecision.TERMINATE,
            reason=TerminationReason.STRONG_PERFORMANCE,
            confidence=min(0.95, avg_score / 10.0),  # Higher scores = higher confidence
            explanation=explanation,
            recommended_action="Proceed to detailed feedback and next steps"
        )
    
    def _create_weak_termination_result(self, avg_score: float, question_count: int) -> TerminationResult:
        """Create termination result for weak performers."""
        explanation = (
            f"After {question_count} questions, your average score of {avg_score:.1f}/10 "
            f"indicates significant gaps in the assessed areas. Continuing would not "
            f"provide additional valuable insights at this time. We recommend "
            f"focusing on foundational learning before reassessment."
        )
        
        return TerminationResult(
            decision=TerminationDecision.TERMINATE,
            reason=TerminationReason.WEAK_PERFORMANCE,
            confidence=min(0.9, (5.0 - avg_score) / 5.0),  # Lower scores = higher confidence in termination
            explanation=explanation,
            recommended_action="Review feedback and focus on identified skill gaps"
        )
    
    def _create_borderline_extension_result(
        self, 
        avg_score: float, 
        question_count: int, 
        max_questions: int,
        trend: str
    ) -> TerminationResult:
        """Create extension result for borderline cases."""
        questions_needed = min(2, max_questions + self.MAX_EXTENSION_QUESTIONS - question_count)
        
        trend_msg = ""
        if trend == "improving":
            trend_msg = "Your performance shows positive improvement, "
        elif trend == "declining":
            trend_msg = "While showing some challenges, "
        else:
            trend_msg = "Your performance is consistent, "
        
        explanation = (
            f"{trend_msg}we need a few more questions to make a definitive assessment. "
            f"Your current average of {avg_score:.1f}/10 falls in our borderline range "
            f"({self.BORDERLINE_LOWER_BOUND}-{self.BORDERLINE_UPPER_BOUND}). "
            f"This additional assessment will help us provide you with the most accurate "
            f"and helpful feedback."
        )
        
        return TerminationResult(
            decision=TerminationDecision.EXTEND,
            reason=TerminationReason.BORDERLINE_CASE,
            confidence=0.8,
            explanation=explanation,
            recommended_action="Continue with additional questions for clearer assessment",
            estimated_questions_remaining=questions_needed
        )
    
    def _create_max_questions_result(self, avg_score: float) -> TerminationResult:
        """Create result when maximum questions reached."""
        explanation = (
            f"You've completed all {len(self.termination_history) + 1} planned questions. "
            f"Your final average score is {avg_score:.1f}/10. "
            f"We now have a comprehensive view of your technical abilities."
        )
        
        return TerminationResult(
            decision=TerminationDecision.TERMINATE,
            reason=TerminationReason.MAX_QUESTIONS_REACHED,
            confidence=1.0,
            explanation=explanation,
            recommended_action="Proceed to detailed results and feedback"
        )
    
    def _create_continue_result(self, avg_score: float, question_count: int, max_questions: int) -> TerminationResult:
        """Create result to continue interview."""
        remaining = max_questions - question_count
        explanation = (
            f"Your current performance average of {avg_score:.1f}/10 suggests "
            f"we should continue to gather more data points. "
            f"{remaining} more questions will help us provide you with "
            f"a more comprehensive and accurate assessment."
        )
        
        return TerminationResult(
            decision=TerminationDecision.CONTINUE,
            reason=TerminationReason.MAX_QUESTIONS_REACHED,  # Default reason when continuing
            confidence=0.7,
            explanation=explanation,
            recommended_action=f"Continue with {remaining} more questions"
        )
    
    def get_termination_summary(self) -> Dict[str, Any]:
        """Get summary of all termination decisions."""
        if not self.termination_history:
            return {"message": "No termination decisions recorded"}
        
        # Calculate statistics
        decision_counts = {}
        reason_counts = {}
        confidences = []
        
        for result in self.termination_history:
            decision = result.decision.value
            reason = result.reason.value
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
            confidences.append(result.confidence)
        
        avg_confidence = statistics.mean(confidences) if confidences else 0
        
        return {
            "total_decisions": len(self.termination_history),
            "average_confidence": round(avg_confidence, 2),
            "decision_distribution": decision_counts,
            "reason_distribution": reason_counts,
            "final_decision": self.termination_history[-1].to_dict() if self.termination_history else None
        }
    
    def reset(self) -> None:
        """Reset termination history for new interview."""
        self.termination_history.clear()
        logger.info("AdaptiveTerminationAgent reset for new session")