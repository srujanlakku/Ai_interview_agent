"""
Scorer module for the AI Interview Agent.
Provides scoring calculations and performance tracking.
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ScoreBreakdown:
    """Detailed score breakdown for an answer."""
    technical_accuracy: float = 0.0
    depth_of_understanding: float = 0.0
    communication_clarity: float = 0.0
    overall: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "technical_accuracy": round(self.technical_accuracy, 1),
            "depth_of_understanding": round(self.depth_of_understanding, 1),
            "communication_clarity": round(self.communication_clarity, 1),
            "overall": round(self.overall, 1),
        }


@dataclass  
class CategoryScores:
    """Scores organized by question category."""
    technical: List[float] = field(default_factory=list)
    behavioral: List[float] = field(default_factory=list)
    coding: List[float] = field(default_factory=list)
    system_design: List[float] = field(default_factory=list)
    
    def get_averages(self) -> Dict[str, float]:
        """Get average scores for each category."""
        return {
            "technical": self._avg(self.technical),
            "behavioral": self._avg(self.behavioral),
            "coding": self._avg(self.coding),
            "system_design": self._avg(self.system_design),
        }
    
    def _avg(self, scores: List[float]) -> float:
        """Calculate average of a list of scores."""
        if not scores:
            return 0.0
        return round(sum(scores) / len(scores), 1)


class Scorer:
    """
    Handles all scoring logic for interview evaluations.
    
    Provides:
    - Individual answer scoring
    - Cumulative score tracking
    - Category-based scoring
    - Performance analysis
    """
    
    # Weight configuration for final score calculation
    WEIGHTS = {
        "technical_accuracy": 0.4,
        "depth_of_understanding": 0.35,
        "communication_clarity": 0.25,
    }
    
    # Readiness thresholds
    READINESS_THRESHOLDS = {
        "interview_ready": 7.5,
        "almost_ready": 5.5,
    }
    
    def __init__(self):
        """Initialize the scorer."""
        self._all_scores: List[ScoreBreakdown] = []
        self._category_scores = CategoryScores()
        self._question_count = 0
    
    def score_answer(
        self,
        evaluation: Dict[str, Any],
        question_type: str,
    ) -> ScoreBreakdown:
        """
        Process an evaluation result and calculate scores.
        
        Args:
            evaluation: Evaluation dictionary from EvaluationAgent
            question_type: Type of question (technical, behavioral, etc.)
            
        Returns:
            ScoreBreakdown with calculated scores
        """
        # Extract component scores
        tech_acc = float(evaluation.get("technical_accuracy", 5))
        depth = float(evaluation.get("depth_of_understanding", 5))
        clarity = float(evaluation.get("communication_clarity", 5))
        
        # Ensure scores are within bounds
        tech_acc = max(0, min(10, tech_acc))
        depth = max(0, min(10, depth))
        clarity = max(0, min(10, clarity))
        
        # Calculate weighted overall score
        overall = (
            tech_acc * self.WEIGHTS["technical_accuracy"] +
            depth * self.WEIGHTS["depth_of_understanding"] +
            clarity * self.WEIGHTS["communication_clarity"]
        )
        
        breakdown = ScoreBreakdown(
            technical_accuracy=tech_acc,
            depth_of_understanding=depth,
            communication_clarity=clarity,
            overall=overall,
        )
        
        # Store for cumulative tracking
        self._all_scores.append(breakdown)
        self._question_count += 1
        
        # Track by category
        self._add_to_category(question_type, overall)
        
        return breakdown
    
    def _add_to_category(self, question_type: str, score: float) -> None:
        """Add score to appropriate category."""
        q_type = question_type.lower()
        if q_type in ("technical", "system_design"):
            if q_type == "system_design":
                self._category_scores.system_design.append(score)
            else:
                self._category_scores.technical.append(score)
        elif q_type == "behavioral":
            self._category_scores.behavioral.append(score)
        elif q_type == "coding":
            self._category_scores.coding.append(score)
        else:
            self._category_scores.technical.append(score)
    
    def get_cumulative_score(self) -> float:
        """Get the cumulative average score."""
        if not self._all_scores:
            return 0.0
        return round(
            sum(s.overall for s in self._all_scores) / len(self._all_scores),
            1
        )
    
    def get_category_averages(self) -> Dict[str, float]:
        """Get average scores by category."""
        return self._category_scores.get_averages()
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive performance summary.
        
        Returns:
            Dictionary with performance metrics
        """
        cumulative = self.get_cumulative_score()
        categories = self.get_category_averages()
        
        # Determine strongest and weakest areas
        non_zero_categories = {k: v for k, v in categories.items() if v > 0}
        
        strongest = max(non_zero_categories.items(), key=lambda x: x[1])[0] if non_zero_categories else "N/A"
        weakest = min(non_zero_categories.items(), key=lambda x: x[1])[0] if non_zero_categories else "N/A"
        
        # Calculate score distribution
        if self._all_scores:
            scores = [s.overall for s in self._all_scores]
            high_scores = sum(1 for s in scores if s >= 7)
            low_scores = sum(1 for s in scores if s < 5)
        else:
            high_scores = low_scores = 0
        
        return {
            "total_questions": self._question_count,
            "cumulative_score": cumulative,
            "category_scores": categories,
            "strongest_area": strongest,
            "weakest_area": weakest,
            "high_score_count": high_scores,
            "low_score_count": low_scores,
            "readiness_level": self.determine_readiness(cumulative),
            "trend": self._calculate_trend(),
        }
    
    def determine_readiness(self, score: Optional[float] = None) -> str:
        """
        Determine interview readiness level.
        
        Args:
            score: Score to evaluate (uses cumulative if not provided)
            
        Returns:
            Readiness level string
        """
        if score is None:
            score = self.get_cumulative_score()
        
        if score >= self.READINESS_THRESHOLDS["interview_ready"]:
            return "Interview Ready"
        elif score >= self.READINESS_THRESHOLDS["almost_ready"]:
            return "Almost Ready"
        else:
            return "Not Ready"
    
    def _calculate_trend(self) -> str:
        """Calculate performance trend based on recent scores."""
        if len(self._all_scores) < 3:
            return "Insufficient data"
        
        # Compare first half to second half
        mid = len(self._all_scores) // 2
        first_half = [s.overall for s in self._all_scores[:mid]]
        second_half = [s.overall for s in self._all_scores[mid:]]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        diff = second_avg - first_avg
        
        if diff > 1:
            return "Improving"
        elif diff < -1:
            return "Declining"
        else:
            return "Stable"
    
    def get_difficulty_recommendation(self) -> str:
        """
        Recommend difficulty adjustment based on recent performance.
        
        Returns:
            Recommended difficulty level
        """
        if len(self._all_scores) < 2:
            return "medium"
        
        recent_scores = [s.overall for s in self._all_scores[-3:]]
        avg_recent = sum(recent_scores) / len(recent_scores)
        
        if avg_recent >= 8:
            return "hard"
        elif avg_recent >= 5.5:
            return "medium"
        else:
            return "easy"
    
    def reset(self) -> None:
        """Reset all scores for a new session."""
        self._all_scores = []
        self._category_scores = CategoryScores()
        self._question_count = 0
