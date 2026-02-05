"""
Interview Replay & Review System - Enables detailed review of interview sessions
with step-by-step analysis of questions, answers, and evaluations.

Features:
- Interactive timeline navigation
- Question-by-question review
- Detailed evaluation reasoning
- Performance visualization
- Exportable review summaries
- Comparative analysis
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime
import statistics
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class ReviewMode(Enum):
    """Different review modes available."""
    TIMELINE = "timeline"          # Chronological question review
    TOPIC_FOCUS = "topic_focus"    # Review by topic/category
    WEAKNESS_FOCUS = "weakness"    # Focus on areas needing improvement
    STRENGTH_FOCUS = "strength"    # Highlight strong performance areas
    COMPARATIVE = "comparative"    # Compare with previous interviews


@dataclass
class ReviewItem:
    """Individual item in the review timeline."""
    question_number: int
    timestamp: datetime
    question: Dict[str, Any]
    answer: str
    evaluation: Dict[str, Any]
    reflection: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "question_number": self.question_number,
            "timestamp": self.timestamp.isoformat(),
            "question": self.question,
            "answer": self.answer,
            "evaluation": self.evaluation,
            "reflection": self.reflection
        }


@dataclass
class PerformanceInsight:
    """Insight derived from performance analysis."""
    insight_type: str  # "strength", "weakness", "trend", "pattern"
    description: str
    confidence: float  # 0.0 to 1.0
    supporting_evidence: List[str]
    recommendation: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "insight_type": self.insight_type,
            "description": self.description,
            "confidence": round(self.confidence, 2),
            "supporting_evidence": self.supporting_evidence,
            "recommendation": self.recommendation
        }


class ReplayAgent:
    """
    Agent that enables comprehensive interview replay and review capabilities.
    
    Features:
    - Interactive timeline navigation
    - Detailed performance analysis
    - Pattern recognition across questions
    - Insight generation
    - Exportable review summaries
    - Comparative analysis tools
    """
    
    def __init__(self):
        self.review_items: List[ReviewItem] = []
        self.performance_insights: List[PerformanceInsight] = []
        self.active_mode: ReviewMode = ReviewMode.TIMELINE
        self.current_position: int = 0
    
    def load_interview_session(self, session_data: Dict[str, Any]) -> None:
        """
        Load interview session data for review.
        
        Args:
            session_data: Complete interview session data including:
                - questions and answers
                - evaluations and scores
                - timestamps
                - reflections (if available)
        """
        # Clear existing data
        self.review_items.clear()
        self.performance_insights.clear()
        
        # Load questions and answers
        questions = session_data.get("questions", [])
        answers = session_data.get("answers", [])
        evaluations = session_data.get("evaluations", [])
        reflections = session_data.get("reflections", [])
        
        # Create review items
        for i, (question, answer, evaluation) in enumerate(zip(questions, answers, evaluations)):
            reflection = reflections[i] if i < len(reflections) else None
            
            item = ReviewItem(
                question_number=i + 1,
                timestamp=datetime.now(),  # TODO: Use actual timestamps from session
                question=question,
                answer=answer,
                evaluation=evaluation,
                reflection=reflection
            )
            self.review_items.append(item)
        
        # Generate performance insights
        self._generate_performance_insights()
        
        logger.info(f"Loaded interview session with {len(self.review_items)} items for review")
    
    def get_timeline_view(self) -> List[Dict[str, Any]]:
        """Get chronological timeline view of the interview."""
        return [item.to_dict() for item in self.review_items]
    
    def get_current_item(self) -> Optional[Dict[str, Any]]:
        """Get currently selected review item."""
        if 0 <= self.current_position < len(self.review_items):
            return self.review_items[self.current_position].to_dict()
        return None
    
    def navigate_to(self, position: int) -> Optional[Dict[str, Any]]:
        """Navigate to specific question position."""
        if 0 <= position < len(self.review_items):
            self.current_position = position
            return self.get_current_item()
        return None
    
    def next_item(self) -> Optional[Dict[str, Any]]:
        """Navigate to next item."""
        return self.navigate_to(self.current_position + 1)
    
    def previous_item(self) -> Optional[Dict[str, Any]]:
        """Navigate to previous item."""
        return self.navigate_to(self.current_position - 1)
    
    def get_topic_focus_view(self, topic: str) -> List[Dict[str, Any]]:
        """Get items focused on specific topic."""
        filtered_items = [
            item for item in self.review_items
            if item.question.get("topic", "").lower() == topic.lower()
        ]
        return [item.to_dict() for item in filtered_items]
    
    def get_weakness_focus_view(self) -> List[Dict[str, Any]]:
        """Get items highlighting areas for improvement."""
        weak_items = [
            item for item in self.review_items
            if item.evaluation.get("score", 5) < 6.0
        ]
        return [item.to_dict() for item in weak_items]
    
    def get_strength_focus_view(self) -> List[Dict[str, Any]]:
        """Get items highlighting strong performance."""
        strong_items = [
            item for item in self.review_items
            if item.evaluation.get("score", 5) >= 8.0
        ]
        return [item.to_dict() for item in strong_items]
    
    def _generate_performance_insights(self) -> None:
        """Generate insights from performance data."""
        if not self.review_items:
            return
        
        scores = [item.evaluation.get("score", 5) for item in self.review_items]
        topics = [item.question.get("topic", "Unknown") for item in self.review_items]
        categories = [item.question.get("category", "Technical") for item in self.review_items]
        
        # Overall performance insight
        avg_score = statistics.mean(scores) if scores else 5.0
        self._add_overall_performance_insight(avg_score)
        
        # Topic performance insights
        self._add_topic_insights(topics, scores)
        
        # Trend analysis
        self._add_trend_insights(scores)
        
        # Pattern recognition
        self._add_pattern_insights(categories, scores)
        
        # Question type analysis
        self._add_question_type_insights()
    
    def _add_overall_performance_insight(self, avg_score: float) -> None:
        """Add overall performance insight."""
        if avg_score >= 8.0:
            insight = PerformanceInsight(
                insight_type="strength",
                description=f"Exceptional overall performance with average score of {avg_score:.1f}/10",
                confidence=0.9,
                supporting_evidence=[f"Consistently scored above 8.0 across {len(self.review_items)} questions"],
                recommendation="Continue building on this strong foundation. Focus on maintaining excellence while expanding knowledge depth."
            )
        elif avg_score >= 6.0:
            insight = PerformanceInsight(
                insight_type="mixed",
                description=f"Solid performance with room for improvement (avg: {avg_score:.1f}/10)",
                confidence=0.8,
                supporting_evidence=[f"Mixed results across {len(self.review_items)} questions"],
                recommendation="Identify specific weak areas and develop targeted improvement plans. Continue strengthening strong areas."
            )
        else:
            insight = PerformanceInsight(
                insight_type="weakness",
                description=f"Significant improvement needed (avg: {avg_score:.1f}/10)",
                confidence=0.95,
                supporting_evidence=[f"Consistent challenges across {len(self.review_items)} questions"],
                recommendation="Focus on fundamental concepts and seek additional learning resources. Consider mentorship or structured training programs."
            )
        
        self.performance_insights.append(insight)
    
    def _add_topic_insights(self, topics: List[str], scores: List[float]) -> None:
        """Add insights about topic-specific performance."""
        topic_scores = {}
        for topic, score in zip(topics, scores):
            if topic not in topic_scores:
                topic_scores[topic] = []
            topic_scores[topic].append(score)
        
        for topic, topic_scores_list in topic_scores.items():
            avg_topic_score = statistics.mean(topic_scores_list)
            if avg_topic_score >= 8.0:
                insight = PerformanceInsight(
                    insight_type="strength",
                    description=f"Strong performance in {topic}",
                    confidence=0.85,
                    supporting_evidence=[f"Avg score: {avg_topic_score:.1f} across {len(topic_scores_list)} questions"],
                    recommendation=f"Leverage your {topic} expertise in future interviews and consider mentoring others."
                )
                self.performance_insights.append(insight)
            elif avg_topic_score < 5.0:
                insight = PerformanceInsight(
                    insight_type="weakness",
                    description=f"Needs improvement in {topic}",
                    confidence=0.9,
                    supporting_evidence=[f"Avg score: {avg_topic_score:.1f} across {len(topic_scores_list)} questions"],
                    recommendation=f"Dedicate focused study time to {topic}. Practice problems and seek clarification on fundamental concepts."
                )
                self.performance_insights.append(insight)
    
    def _add_trend_insights(self, scores: List[float]) -> None:
        """Add insights about performance trends."""
        if len(scores) < 3:
            return
        
        # Simple trend analysis
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        if second_avg > first_avg + 1.0:
            insight = PerformanceInsight(
                insight_type="trend",
                description="Positive performance improvement trend",
                confidence=0.8,
                supporting_evidence=[
                    f"First half average: {first_avg:.1f}",
                    f"Second half average: {second_avg:.1f}",
                    "Demonstrated learning and adaptation"
                ],
                recommendation="Your preparation and adaptability are paying off. Continue this upward trajectory."
            )
            self.performance_insights.append(insight)
        elif second_avg < first_avg - 1.0:
            insight = PerformanceInsight(
                insight_type="trend",
                description="Performance decline observed",
                confidence=0.75,
                supporting_evidence=[
                    f"First half average: {first_avg:.1f}",
                    f"Second half average: {second_avg:.1f}",
                    "May indicate fatigue or knowledge gaps"
                ],
                recommendation="Consider pacing strategies and ensure consistent preparation throughout the interview process."
            )
            self.performance_insights.append(insight)
    
    def _add_pattern_insights(self, categories: List[str], scores: List[float]) -> None:
        """Add insights about performance patterns."""
        # Find correlations between categories and performance
        category_performance = {}
        for category, score in zip(categories, scores):
            if category not in category_performance:
                category_performance[category] = []
            category_performance[category].append(score)
        
        # Identify categories with highest variance
        for category, cat_scores in category_performance.items():
            if len(cat_scores) > 1:
                variance = statistics.variance(cat_scores)
                if variance > 2.0:  # High variance indicates inconsistent performance
                    insight = PerformanceInsight(
                        insight_type="pattern",
                        description=f"Inconsistent performance in {category} questions",
                        confidence=0.7,
                        supporting_evidence=[
                            f"Score variance: {variance:.2f}",
                            f"Range: {min(cat_scores):.1f} to {max(cat_scores):.1f}",
                            "Performance varies significantly across similar questions"
                        ],
                        recommendation=f"Focus on consistent preparation for {category} topics. Identify specific areas causing variability."
                    )
                    self.performance_insights.append(insight)
    
    def _add_question_type_insights(self) -> None:
        """Add insights about different question types."""
        # Analyze performance by question characteristics
        coding_questions = [item for item in self.review_items if "coding" in item.question.get("type", "").lower()]
        theory_questions = [item for item in self.review_items if "theory" in item.question.get("type", "").lower()]
        
        if coding_questions:
            coding_scores = [item.evaluation.get("score", 5) for item in coding_questions]
            avg_coding = statistics.mean(coding_scores)
            insight = PerformanceInsight(
                insight_type="pattern",
                description=f"Coding question performance: {avg_coding:.1f}/10",
                confidence=0.8,
                supporting_evidence=[f"Based on {len(coding_questions)} coding questions"],
                recommendation="Practice coding problems regularly to maintain and improve implementation skills."
            )
            self.performance_insights.append(insight)
        
        if theory_questions:
            theory_scores = [item.evaluation.get("score", 5) for item in theory_questions]
            avg_theory = statistics.mean(theory_scores)
            insight = PerformanceInsight(
                insight_type="pattern",
                description=f"Theory question performance: {avg_theory:.1f}/10",
                confidence=0.8,
                supporting_evidence=[f"Based on {len(theory_questions)} theory questions"],
                recommendation="Ensure strong conceptual understanding. Practice explaining complex topics clearly and concisely."
            )
            self.performance_insights.append(insight)
    
    def get_performance_insights(self) -> List[Dict[str, Any]]:
        """Get all generated performance insights."""
        return [insight.to_dict() for insight in self.performance_insights]
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get comprehensive summary statistics."""
        if not self.review_items:
            return {"message": "No data available"}
        
        scores = [item.evaluation.get("score", 5) for item in self.review_items]
        topics = list(set(item.question.get("topic", "Unknown") for item in self.review_items))
        categories = list(set(item.question.get("category", "Technical") for item in self.review_items))
        
        return {
            "total_questions": len(self.review_items),
            "average_score": round(statistics.mean(scores), 2),
            "score_range": {
                "min": min(scores),
                "max": max(scores)
            },
            "score_distribution": self._get_score_distribution(scores),
            "topics_covered": len(topics),
            "topic_list": sorted(topics),
            "categories_covered": len(categories),
            "category_list": sorted(categories),
            "performance_trend": self._get_performance_trend(scores)
        }
    
    def _get_score_distribution(self, scores: List[float]) -> Dict[str, int]:
        """Get distribution of scores across ranges."""
        distribution = {
            "excellent": 0,    # 8-10
            "good": 0,         # 6-7.9
            "average": 0,      # 4-5.9
            "poor": 0          # 0-3.9
        }
        
        for score in scores:
            if score >= 8:
                distribution["excellent"] += 1
            elif score >= 6:
                distribution["good"] += 1
            elif score >= 4:
                distribution["average"] += 1
            else:
                distribution["poor"] += 1
        
        return distribution
    
    def _get_performance_trend(self, scores: List[float]) -> str:
        """Get overall performance trend description."""
        if len(scores) < 2:
            return "insufficient_data"
        
        # Simple trend analysis
        avg_first = statistics.mean(scores[:len(scores)//2])
        avg_second = statistics.mean(scores[len(scores)//2:])
        
        if avg_second > avg_first + 0.5:
            return "improving"
        elif avg_second < avg_first - 0.5:
            return "declining"
        else:
            return "stable"
    
    def export_review_summary(self, format_type: str = "json") -> str:
        """Export review summary in specified format."""
        summary_data = {
            "review_metadata": {
                "total_items": len(self.review_items),
                "review_date": datetime.now().isoformat(),
                "mode": self.active_mode.value
            },
            "performance_summary": self.get_summary_statistics(),
            "key_insights": self.get_performance_insights(),
            "detailed_timeline": self.get_timeline_view()
        }
        
        if format_type.lower() == "json":
            return json.dumps(summary_data, indent=2)
        elif format_type.lower() == "text":
            return self._format_text_summary(summary_data)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def _format_text_summary(self, data: Dict[str, Any]) -> str:
        """Format summary as readable text."""
        summary = []
        summary.append("=== INTERVIEW REVIEW SUMMARY ===\n")
        
        perf_summary = data["performance_summary"]
        summary.append(f"Total Questions: {perf_summary['total_questions']}")
        summary.append(f"Average Score: {perf_summary['average_score']}/10")
        summary.append(f"Topics Covered: {perf_summary['topics_covered']}")
        summary.append(f"Trend: {perf_summary['performance_trend'].title()}\n")
        
        summary.append("KEY INSIGHTS:")
        for insight in data["key_insights"][:5]:  # Top 5 insights
            summary.append(f"- {insight['description']} (Confidence: {insight['confidence']})")
        
        return "\n".join(summary)
    
    def reset(self) -> None:
        """Reset replay agent for new session."""
        self.review_items.clear()
        self.performance_insights.clear()
        self.current_position = 0
        self.active_mode = ReviewMode.TIMELINE
        logger.info("ReplayAgent reset for new session")