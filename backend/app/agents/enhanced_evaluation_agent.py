"""
Enhanced Evaluation Agent with structured output and confidence bands.
"""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent, LLMError
from app.evaluation.enhanced_scorer import EnhancedScorer, DetailedScore, ConfidenceBand

# Try to import logging
try:
    from app.utils.logging_config import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


class EnhancedEvaluationAgent(BaseAgent):
    """
    Enhanced agent for evaluating interview answers with structured output.
    
    Features:
    - 3-dimensional scoring (correctness, depth, clarity)
    - Confidence bands (Strong/Medium/Weak)
    - Detailed explanations for scores
    - Actionable improvement suggestions
    """

    def __init__(self):
        super().__init__("EnhancedEvaluationAgent")
        self._cumulative_scores: List[Dict[str, float]] = []
        self.scorer = EnhancedScorer()

    async def execute(
        self,
        question: str,
        answer: str,
        question_type: str = "technical",
        ideal_answer_points: Optional[List[str]] = None,
        experience_level: str = "mid",
    ) -> Dict[str, Any]:
        """
        Evaluate answer with structured scoring and confidence bands.
        
        Args:
            question: The interview question
            answer: User's answer
            question_type: Type of question
            ideal_answer_points: Expected key points
            experience_level: Candidate's experience level
            
        Returns:
            Enhanced evaluation with detailed scores and confidence bands
        """
        try:
            # Use enhanced scorer for detailed evaluation
            detailed_score: DetailedScore = await self.scorer.score_answer(
                question=question,
                answer=answer,
                question_type=question_type,
                ideal_points=ideal_answer_points or [],
                experience_level=experience_level
            )
            
            # Generate comprehensive feedback
            feedback = self._generate_enhanced_feedback(detailed_score, question_type, experience_level)
            
            result = {
                "score": detailed_score.overall,
                "correctness_score": detailed_score.correctness,
                "depth_score": detailed_score.depth,
                "clarity_score": detailed_score.clarity,
                "confidence_band": detailed_score.confidence_band.value,
                "explanation": detailed_score.explanation,
                "feedback": feedback,
                "strengths": self._extract_strengths(detailed_score),
                "weaknesses": self._extract_weaknesses(detailed_score),
                "improvement_suggestions": self._generate_improvements(detailed_score, question_type),
                "question_type": question_type,
                "experience_level": experience_level
            }
            
            # Track for cumulative analysis
            self._cumulative_scores.append({
                "overall": detailed_score.overall,
                "correctness": detailed_score.correctness,
                "depth": detailed_score.depth,
                "clarity": detailed_score.clarity,
                "confidence": detailed_score.confidence_band.value
            })
            
            logger.info(f"Enhanced evaluation completed: {detailed_score.overall}/10 ({detailed_score.confidence_band.value})")
            return result
            
        except Exception as e:
            logger.error(f"Enhanced evaluation failed: {str(e)}")
            return self._fallback_evaluation(answer, question_type)

    def _generate_enhanced_feedback(self, score: DetailedScore, question_type: str, experience_level: str) -> str:
        """Generate detailed, contextual feedback."""
        base_feedback = score.explanation
        
        # Add confidence-based context
        confidence_messages = {
            ConfidenceBand.STRONG: "Your response demonstrates strong mastery of the subject matter.",
            ConfidenceBand.MEDIUM: "Your response shows solid knowledge with room for deeper exploration.",
            ConfidenceBand.WEAK: "Your response indicates areas needing significant improvement."
        }
        
        confidence_msg = confidence_messages.get(score.confidence_band, "")
        
        # Add question-type specific guidance
        type_guidance = {
            "coding": "Consider walking through your approach step-by-step and explaining trade-offs.",
            "system_design": "Focus on scalability, trade-offs, and real-world constraints in your design.",
            "behavioral": "Use the STAR method (Situation, Task, Action, Result) to structure your response.",
            "technical": "Provide specific examples and relate concepts to practical applications."
        }
        
        guidance = type_guidance.get(question_type, "")
        
        return f"{base_feedback} {confidence_msg} {guidance}".strip()

    def _extract_strengths(self, score: DetailedScore) -> List[str]:
        """Extract key strengths from detailed scoring."""
        strengths = []
        
        if score.correctness >= 8.0:
            strengths.append("High technical accuracy")
        elif score.correctness >= 6.0:
            strengths.append("Good foundational knowledge")
            
        if score.depth >= 8.0:
            strengths.append("Deep conceptual understanding")
        elif score.depth >= 6.0:
            strengths.append("Solid depth of knowledge")
            
        if score.clarity >= 8.0:
            strengths.append("Excellent communication skills")
        elif score.clarity >= 6.0:
            strengths.append("Clear and organized explanation")
            
        return strengths or ["Response completed"]

    def _extract_weaknesses(self, score: DetailedScore) -> List[str]:
        """Identify areas for improvement."""
        weaknesses = []
        
        if score.correctness < 6.0:
            weaknesses.append("Technical accuracy needs strengthening")
        if score.depth < 6.0:
            weaknesses.append("Could demonstrate deeper understanding")
        if score.clarity < 6.0:
            weaknesses.append("Communication clarity could be improved")
            
        return weaknesses

    def _generate_improvements(self, score: DetailedScore, question_type: str) -> List[str]:
        """Generate specific improvement recommendations."""
        improvements = []
        
        if score.correctness < 7.0:
            improvements.append("Review fundamental concepts and practice with concrete examples")
        if score.depth < 7.0:
            improvements.append("Study advanced topics and their practical applications")
        if score.clarity < 7.0:
            improvements.append("Practice structuring responses clearly and concisely")
            
        # Question-type specific suggestions
        type_suggestions = {
            "coding": [
                "Practice explaining your algorithmic approach before coding",
                "Discuss time/space complexity and alternative solutions"
            ],
            "system_design": [
                "Focus on scalability requirements and system constraints",
                "Consider trade-offs between different architectural decisions"
            ],
            "behavioral": [
                "Prepare specific examples using the STAR method",
                "Quantify your achievements with metrics when possible"
            ]
        }
        
        improvements.extend(type_suggestions.get(question_type, []))
        return improvements

    def _fallback_evaluation(self, answer: str, question_type: str) -> Dict[str, Any]:
        """Provide basic evaluation when enhanced scoring fails."""
        word_count = len(answer.split())
        base_score = min(10, max(3, word_count / 20))
        
        return {
            "score": base_score,
            "correctness_score": base_score,
            "depth_score": base_score * 0.8,
            "clarity_score": base_score * 0.9,
            "confidence_band": "medium",
            "explanation": "Using basic evaluation due to system limitations.",
            "feedback": "Provide more detailed responses for comprehensive evaluation.",
            "strengths": ["Response provided"],
            "weaknesses": ["Limited detail in response"],
            "improvement_suggestions": ["Expand answers with specific examples and explanations"],
            "question_type": question_type,
            "experience_level": "mid"
        }

    def get_performance_insights(self) -> Dict[str, Any]:
        """Generate insights from cumulative evaluation data."""
        if not self._cumulative_scores:
            return {"message": "No evaluation data available"}
            
        scores = self._cumulative_scores
        total = len(scores)
        
        # Calculate averages
        avg_scores = {
            "overall": sum(s["overall"] for s in scores) / total,
            "correctness": sum(s["correctness"] for s in scores) / total,
            "depth": sum(s["depth"] for s in scores) / total,
            "clarity": sum(s["clarity"] for s in scores) / total
        }
        
        # Confidence distribution
        confidence_counts = {}
        for s in scores:
            conf = s["confidence"]
            confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
            
        # Identify improvement areas
        weak_areas = []
        if avg_scores["correctness"] < 7.0:
            weak_areas.append("technical accuracy")
        if avg_scores["depth"] < 7.0:
            weak_areas.append("conceptual depth")
        if avg_scores["clarity"] < 7.0:
            weak_areas.append("communication clarity")
            
        return {
            "total_evaluations": total,
            "average_scores": avg_scores,
            "confidence_distribution": confidence_counts,
            "areas_for_improvement": weak_areas,
            "performance_trend": "improving" if total > 1 and scores[-1]["overall"] > scores[0]["overall"] else "stable"
        }