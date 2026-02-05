"""
Difficulty Calibration Controller - Adaptive difficulty adjustment based on performance history.
Monitors trends and dynamically adjusts question difficulty for optimal assessment.
"""
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
from collections import deque


class DifficultyLevel(str, Enum):
    """Question difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class TrendDirection(str, Enum):
    """Performance trend directions."""
    IMPROVING = "improving"
    DECLINING = "declining"
    STABLE = "stable"


class AdjustmentReason(str, Enum):
    """Reasons for difficulty adjustment."""
    CONSISTENT_HIGH_PERFORMANCE = "consistent_high_performance"
    CONSISTENT_LOW_PERFORMANCE = "consistent_low_performance"
    VOLATILE_PERFORMANCE = "volatile_performance"
    STABLE_PERFORMANCE = "stable_performance"
    INSUFFICIENT_DATA = "insufficient_data"


@dataclass
class PerformanceSnapshot:
    """Snapshot of performance at a point in time."""
    question_number: int
    score: float
    difficulty: DifficultyLevel
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "question_number": self.question_number,
            "score": self.score,
            "difficulty": self.difficulty.value,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class CalibrationDecision:
    """Decision made by the difficulty controller."""
    recommended_difficulty: DifficultyLevel
    reason: AdjustmentReason
    confidence: float  # 0.0 to 1.0
    trend_direction: TrendDirection
    performance_stats: Dict[str, float]
    explanation: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "recommended_difficulty": self.recommended_difficulty.value,
            "reason": self.reason.value,
            "confidence": round(self.confidence, 2),
            "trend_direction": self.trend_direction.value,
            "performance_stats": self.performance_stats,
            "explanation": self.explanation,
            "timestamp": self.timestamp.isoformat()
        }


class DifficultyCalibrationController:
    """
    Enterprise-grade difficulty calibration controller.
    
    Features:
    - Performance trend analysis
    - Adaptive difficulty adjustment
    - Confidence-based decision making
    - Detailed adjustment rationale
    - Performance volatility detection
    """
    
    # Configuration thresholds
    HIGH_PERFORMANCE_THRESHOLD = 8.0
    LOW_PERFORMANCE_THRESHOLD = 5.0
    TREND_SIGNIFICANCE_THRESHOLD = 1.5  # Minimum score difference to consider trend
    VOLATILITY_THRESHOLD = 2.0  # Standard deviation threshold for volatility
    MIN_QUESTIONS_FOR_TREND = 3  # Minimum questions needed for trend analysis
    CONFIDENCE_BOOST_PER_QUESTION = 0.1  # Confidence increase per question
    
    def __init__(self, max_history: int = 20):
        """
        Initialize the difficulty controller.
        
        Args:
            max_history: Maximum number of performance snapshots to keep
        """
        self.performance_history: deque = deque(maxlen=max_history)
        self.difficulty_adjustments: List[CalibrationDecision] = []
        self.current_difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
        self.session_start_time: Optional[datetime] = None
    
    def record_performance(
        self,
        question_number: int,
        score: float,
        difficulty: DifficultyLevel
    ) -> None:
        """
        Record a performance snapshot.
        
        Args:
            question_number: Current question number
            score: Score achieved (0-10)
            difficulty: Difficulty level of the question
        """
        snapshot = PerformanceSnapshot(
            question_number=question_number,
            score=score,
            difficulty=difficulty
        )
        self.performance_history.append(snapshot)
        
        if not self.session_start_time:
            self.session_start_time = datetime.now()
    
    def get_difficulty_recommendation(
        self,
        current_question: int,
        role: str = "Software Engineer",
        experience_level: str = "mid"
    ) -> CalibrationDecision:
        """
        Get difficulty recommendation based on performance history.
        
        Args:
            current_question: Current question number
            role: Target role
            experience_level: Experience level
            
        Returns:
            CalibrationDecision with recommendation and rationale
        """
        if len(self.performance_history) < self.MIN_QUESTIONS_FOR_TREND:
            return self._get_insufficient_data_decision(current_question)
        
        # Calculate performance statistics
        stats = self._calculate_performance_stats()
        
        # Determine trend direction
        trend_direction = self._analyze_trend_direction(stats)
        
        # Determine adjustment reason
        reason = self._determine_adjustment_reason(stats, trend_direction)
        
        # Calculate confidence level
        confidence = self._calculate_confidence(stats)
        
        # Recommend difficulty level
        recommended_difficulty = self._recommend_difficulty(
            stats, trend_direction, reason, experience_level
        )
        
        # Generate explanation
        explanation = self._generate_explanation(
            stats, trend_direction, reason, recommended_difficulty
        )
        
        decision = CalibrationDecision(
            recommended_difficulty=recommended_difficulty,
            reason=reason,
            confidence=confidence,
            trend_direction=trend_direction,
            performance_stats=stats,
            explanation=explanation
        )
        
        self.difficulty_adjustments.append(decision)
        self.current_difficulty = recommended_difficulty
        
        return decision
    
    def _calculate_performance_stats(self) -> Dict[str, float]:
        """Calculate comprehensive performance statistics."""
        if not self.performance_history:
            return {}
        
        scores = [snapshot.score for snapshot in self.performance_history]
        difficulties = [snapshot.difficulty for snapshot in self.performance_history]
        
        # Basic statistics
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        # Trend analysis (comparing first half vs second half)
        mid_point = len(scores) // 2
        if mid_point > 0:
            first_half_avg = sum(scores[:mid_point]) / mid_point
            second_half_avg = sum(scores[mid_point:]) / (len(scores) - mid_point)
            trend_magnitude = second_half_avg - first_half_avg
        else:
            trend_magnitude = 0.0
            first_half_avg = second_half_avg = avg_score
        
        # Volatility analysis
        if len(scores) > 1:
            variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
            volatility = variance ** 0.5
        else:
            volatility = 0.0
        
        # Difficulty distribution
        difficulty_counts = {}
        for diff in difficulties:
            difficulty_counts[diff.value] = difficulty_counts.get(diff.value, 0) + 1
        
        # Performance consistency
        consistency_score = 10.0 - (volatility * 2)  # Invert volatility to consistency
        consistency_score = max(0.0, min(10.0, consistency_score))
        
        return {
            "total_questions": len(scores),
            "average_score": round(avg_score, 2),
            "max_score": max_score,
            "min_score": min_score,
            "trend_magnitude": round(trend_magnitude, 2),
            "volatility": round(volatility, 2),
            "consistency_score": round(consistency_score, 2),
            "first_half_average": round(first_half_avg, 2),
            "second_half_average": round(second_half_avg, 2),
            "difficulty_distribution": difficulty_counts
        }
    
    def _analyze_trend_direction(self, stats: Dict[str, float]) -> TrendDirection:
        """Analyze the direction of performance trend."""
        trend_magnitude = stats.get("trend_magnitude", 0.0)
        
        if abs(trend_magnitude) < 0.5:
            return TrendDirection.STABLE
        elif trend_magnitude > 0:
            return TrendDirection.IMPROVING
        else:
            return TrendDirection.DECLINING
    
    def _determine_adjustment_reason(
        self,
        stats: Dict[str, float],
        trend_direction: TrendDirection
    ) -> AdjustmentReason:
        """Determine the reason for difficulty adjustment."""
        avg_score = stats.get("average_score", 5.0)
        volatility = stats.get("volatility", 0.0)
        trend_magnitude = stats.get("trend_magnitude", 0.0)
        
        # High performance with stability
        if (avg_score >= self.HIGH_PERFORMANCE_THRESHOLD and 
            volatility <= self.VOLATILITY_THRESHOLD and
            trend_direction == TrendDirection.STABLE):
            return AdjustmentReason.CONSISTENT_HIGH_PERFORMANCE
        
        # Low performance with stability
        if (avg_score <= self.LOW_PERFORMANCE_THRESHOLD and
            volatility <= self.VOLATILITY_THRESHOLD and
            trend_direction == TrendDirection.STABLE):
            return AdjustmentReason.CONSISTENT_LOW_PERFORMANCE
        
        # High volatility
        if volatility > self.VOLATILITY_THRESHOLD:
            return AdjustmentReason.VOLATILE_PERFORMANCE
        
        # Stable performance within normal range
        if (self.LOW_PERFORMANCE_THRESHOLD < avg_score < self.HIGH_PERFORMANCE_THRESHOLD and
            trend_direction == TrendDirection.STABLE):
            return AdjustmentReason.STABLE_PERFORMANCE
        
        # Default case
        return AdjustmentReason.INSUFFICIENT_DATA
    
    def _calculate_confidence(self, stats: Dict[str, float]) -> float:
        """Calculate confidence level in the recommendation."""
        total_questions = stats.get("total_questions", 0)
        
        # Base confidence increases with more data
        base_confidence = min(1.0, total_questions * self.CONFIDENCE_BOOST_PER_QUESTION)
        
        # Adjust based on volatility (lower confidence with high volatility)
        volatility = stats.get("volatility", 0.0)
        volatility_penalty = min(0.5, volatility / 10.0)
        
        # Adjust based on trend significance
        trend_magnitude = abs(stats.get("trend_magnitude", 0.0))
        trend_bonus = min(0.3, trend_magnitude / 5.0)
        
        confidence = base_confidence - volatility_penalty + trend_bonus
        return max(0.1, min(1.0, confidence))  # Ensure reasonable bounds
    
    def _recommend_difficulty(
        self,
        stats: Dict[str, float],
        trend_direction: TrendDirection,
        reason: AdjustmentReason,
        experience_level: str
    ) -> DifficultyLevel:
        """Recommend appropriate difficulty level."""
        avg_score = stats.get("average_score", 5.0)
        trend_magnitude = stats.get("trend_magnitude", 0.0)
        
        # Experience level base difficulty
        base_difficulty = self._get_base_difficulty(experience_level)
        
        # Adjust based on performance
        if reason == AdjustmentReason.CONSISTENT_HIGH_PERFORMANCE:
            return DifficultyLevel.HARD
        elif reason == AdjustmentReason.CONSISTENT_LOW_PERFORMANCE:
            return DifficultyLevel.EASY
        elif reason == AdjustmentReason.VOLATILE_PERFORMANCE:
            # Return to medium for volatile performance
            return DifficultyLevel.MEDIUM
        elif reason == AdjustmentReason.STABLE_PERFORMANCE:
            # Adjust based on average score
            if avg_score >= 7.5:
                return DifficultyLevel.HARD
            elif avg_score >= 6.0:
                return DifficultyLevel.MEDIUM
            else:
                return DifficultyLevel.EASY
        else:
            # Insufficient data - maintain current or use base
            return self.current_difficulty or base_difficulty
    
    def _get_base_difficulty(self, experience_level: str) -> DifficultyLevel:
        """Get base difficulty based on experience level."""
        base_difficulties = {
            "fresher": DifficultyLevel.EASY,
            "mid": DifficultyLevel.MEDIUM,
            "senior": DifficultyLevel.MEDIUM  # Senior candidates start medium to prove themselves
        }
        return base_difficulties.get(experience_level, DifficultyLevel.MEDIUM)
    
    def _generate_explanation(
        self,
        stats: Dict[str, float],
        trend_direction: TrendDirection,
        reason: AdjustmentReason,
        recommended_difficulty: DifficultyLevel
    ) -> str:
        """Generate human-readable explanation for the decision."""
        avg_score = stats.get("average_score", 5.0)
        volatility = stats.get("volatility", 0.0)
        total_questions = int(stats.get("total_questions", 0))
        
        explanations = {
            AdjustmentReason.CONSISTENT_HIGH_PERFORMANCE: (
                f"Based on consistently high performance (avg: {avg_score}/10) "
                f"with low volatility ({volatility:.1f}), escalating to {recommended_difficulty.value} "
                f"difficulty to properly challenge the candidate."
            ),
            AdjustmentReason.CONSISTENT_LOW_PERFORMANCE: (
                f"Performance consistently below threshold (avg: {avg_score}/10) "
                f"with stable results. Reducing to {recommended_difficulty.value} difficulty "
                f"to build confidence and assess fundamentals."
            ),
            AdjustmentReason.VOLATILE_PERFORMANCE: (
                f"Performance shows high volatility (σ={volatility:.1f}), indicating "
                f"uncertainty in knowledge. Resetting to {recommended_difficulty.value} difficulty "
                f"for more consistent assessment."
            ),
            AdjustmentReason.STABLE_PERFORMANCE: (
                f"Stable performance trend (avg: {avg_score}/10) suggests "
                f"{recommended_difficulty.value} difficulty is appropriate for accurate assessment."
            ),
            AdjustmentReason.INSUFFICIENT_DATA: (
                f"Insufficient data ({total_questions} questions answered). "
                f"Maintaining {recommended_difficulty.value} difficulty while gathering more information."
            )
        }
        
        return explanations.get(reason, "Adjusting difficulty based on performance analysis.")
    
    def _get_insufficient_data_decision(
        self,
        current_question: int
    ) -> CalibrationDecision:
        """Get decision when there's insufficient performance data."""
        return CalibrationDecision(
            recommended_difficulty=self.current_difficulty or DifficultyLevel.MEDIUM,
            reason=AdjustmentReason.INSUFFICIENT_DATA,
            confidence=0.3,
            trend_direction=TrendDirection.STABLE,
            performance_stats={"total_questions": current_question, "message": "Insufficient data"},
            explanation=f"Not enough questions answered ({current_question}) to make reliable adjustment."
        )
    
    def get_calibration_history(self) -> List[Dict[str, Any]]:
        """Get history of all calibration decisions."""
        return [decision.to_dict() for decision in self.difficulty_adjustments]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        if not self.performance_history:
            return {"message": "No performance data recorded"}
        
        stats = self._calculate_performance_stats()
        latest_difficulty = self.current_difficulty.value if self.current_difficulty else "unknown"
        
        # Get difficulty adjustment frequency
        adjustments = len(self.difficulty_adjustments)
        
        # Calculate time elapsed
        if self.session_start_time:
            elapsed_time = datetime.now() - self.session_start_time
            elapsed_minutes = elapsed_time.total_seconds() / 60
        else:
            elapsed_minutes = 0
        
        return {
            "session_duration_minutes": round(elapsed_minutes, 1),
            "total_questions_answered": len(self.performance_history),
            "current_difficulty": latest_difficulty,
            "difficulty_adjustments_made": adjustments,
            "performance_statistics": stats,
            "calibration_decisions": self.get_calibration_history()
        }
    
    def reset_session(self) -> None:
        """Reset the controller for a new session."""
        self.performance_history.clear()
        self.difficulty_adjustments.clear()
        self.current_difficulty = DifficultyLevel.MEDIUM
        self.session_start_time = None
    
    def get_difficulty_progression(self) -> List[Dict[str, Any]]:
        """Get the progression of difficulty levels throughout the session."""
        progression = []
        for i, snapshot in enumerate(self.performance_history):
            progression.append({
                "question": snapshot.question_number,
                "score": snapshot.score,
                "difficulty": snapshot.difficulty.value,
                "timestamp": snapshot.timestamp.isoformat()
            })
        return progression
    
    def predict_next_performance(self) -> Dict[str, float]:
        """Predict expected performance on next question based on trends."""
        if len(self.performance_history) < 2:
            return {"predicted_score": 5.0, "confidence": 0.1}
        
        stats = self._calculate_performance_stats()
        trend_magnitude = stats.get("trend_magnitude", 0.0)
        avg_score = stats.get("average_score", 5.0)
        
        # Simple prediction based on trend
        predicted_score = avg_score + (trend_magnitude * 0.3)  # Dampen trend effect
        predicted_score = max(0.0, min(10.0, predicted_score))
        
        # Confidence based on trend consistency
        volatility = stats.get("volatility", 5.0)  # High default volatility
        trend_consistency = 1.0 - min(1.0, volatility / 5.0)
        
        return {
            "predicted_score": round(predicted_score, 1),
            "confidence": round(trend_consistency, 2),
            "based_on_questions": len(self.performance_history)
        }
    
    def get_adaptive_strategy_insights(self) -> Dict[str, Any]:
        """Get insights about the adaptive strategy effectiveness."""
        if not self.difficulty_adjustments:
            return {"message": "No adjustments made yet"}
        
        # Analyze adjustment patterns
        adjustment_reasons = {}
        difficulty_changes = 0
        
        for decision in self.difficulty_adjustments:
            reason = decision.reason.value
            adjustment_reasons[reason] = adjustment_reasons.get(reason, 0) + 1
            
            # Count actual difficulty changes
            if len(self.difficulty_adjustments) > 1:
                prev_decision = self.difficulty_adjustments[-2]
                if prev_decision.recommended_difficulty != decision.recommended_difficulty:
                    difficulty_changes += 1
        
        # Calculate adjustment frequency
        total_adjustments = len(self.difficulty_adjustments)
        questions_answered = len(self.performance_history)
        adjustment_frequency = total_adjustments / max(1, questions_answered)
        
        # Confidence trend
        confidence_scores = [d.confidence for d in self.difficulty_adjustments]
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        return {
            "total_adjustments": total_adjustments,
            "difficulty_changes": difficulty_changes,
            "adjustment_frequency": round(adjustment_frequency, 2),
            "average_confidence": round(avg_confidence, 2),
            "reason_distribution": adjustment_reasons,
            "strategy_effectiveness": "High" if avg_confidence > 0.7 else "Medium" if avg_confidence > 0.5 else "Low"
        }