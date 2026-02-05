"""
Reflection Agent - Adds internal reflection after each answer to evaluate question effectiveness
and determine optimal next steps (deeper probing, topic switch, difficulty adjustment).

This agent makes the interview process more human-like by simulating an experienced 
interviewer's thought process.
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class NextAction(Enum):
    """Possible next actions after reflection."""
    DEEPER_PROBING = "deeper_probing"
    TOPIC_SWITCH = "topic_switch"
    DIFFICULTY_ADJUSTMENT = "difficulty_adjustment"
    MAINTAIN_CURRENT = "maintain_current"


class QuestionEffectiveness(Enum):
    """Effectiveness rating of the question asked."""
    HIGH = "high"      # Revealed significant insights about candidate
    MEDIUM = "medium"  # Provided useful information
    LOW = "low"        # Didn't yield meaningful insights


@dataclass
class ReflectionResult:
    """Result of the reflection process."""
    question_effectiveness: QuestionEffectiveness
    next_action: NextAction
    reasoning: str
    confidence: float  # 0.0 to 1.0
    suggested_difficulty: Optional[str] = None
    suggested_topic: Optional[str] = None
    probing_depth: Optional[int] = None  # 1-3 scale for follow-up depth
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "question_effectiveness": self.question_effectiveness.value,
            "next_action": self.next_action.value,
            "reasoning": self.reasoning,
            "confidence": round(self.confidence, 2),
            "suggested_difficulty": self.suggested_difficulty,
            "suggested_topic": self.suggested_topic,
            "probing_depth": self.probing_depth
        }


class ReflectionAgent(BaseAgent):
    """
    Agent that reflects on interview interactions to optimize the questioning strategy.
    
    Features:
    - Evaluates question effectiveness after each answer
    - Determines optimal next action (deeper probe, switch topic, adjust difficulty)
    - Maintains contextual awareness of interview flow
    - Provides explainable reasoning for decisions
    """
    
    def __init__(self):
        super().__init__("ReflectionAgent")
        self.reflection_history: List[ReflectionResult] = []
    
    async def reflect_on_interaction(
        self,
        question: str,
        answer: str,
        evaluation: Dict[str, Any],
        current_context: Dict[str, Any]
    ) -> ReflectionResult:
        """
        Reflect on a question-answer interaction and determine next optimal step.
        
        Args:
            question: The question that was asked
            answer: The candidate's answer
            evaluation: Evaluation results from EvaluationAgent
            current_context: Current interview context (scores, topics, difficulty, etc.)
            
        Returns:
            ReflectionResult with next action recommendation
        """
        try:
            # Build reflection prompt
            prompt = self._build_reflection_prompt(question, answer, evaluation, current_context)
            
            # Get reflection from LLM
            response = await self.call_llm(
                prompt,
                system_message=(
                    "You are an experienced technical interview coach with decades of hiring experience. "
                    "You excel at reflecting on interview interactions to optimize the assessment process. "
                    "Think like a master interviewer who knows when to dig deeper, when to pivot, "
                    "and when to adjust difficulty. Always provide specific, actionable insights."
                ),
                temperature=0.4,
                max_tokens=600
            )
            
            # Parse response
            reflection_data = self._parse_reflection_response(response)
            
            # Create result object
            result = ReflectionResult(
                question_effectiveness=QuestionEffectiveness(reflection_data["effectiveness"]),
                next_action=NextAction(reflection_data["next_action"]),
                reasoning=reflection_data["reasoning"],
                confidence=float(reflection_data["confidence"]),
                suggested_difficulty=reflection_data.get("suggested_difficulty"),
                suggested_topic=reflection_data.get("suggested_topic"),
                probing_depth=reflection_data.get("probing_depth")
            )
            
            # Store in history
            self.reflection_history.append(result)
            
            logger.info(
                f"Reflection completed | Effectiveness: {result.question_effectiveness.value} | "
                f"Next Action: {result.next_action.value} | Confidence: {result.confidence:.2f}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"ReflectionAgent failed: {str(e)}")
            # Fallback reflection
            return self._fallback_reflection(evaluation, current_context)
    
    def _build_reflection_prompt(
        self,
        question: str,
        answer: str,
        evaluation: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for reflection analysis."""
        scores = evaluation.get("scores", {})
        overall_score = evaluation.get("score", 5.0)
        strengths = evaluation.get("strengths", [])
        weaknesses = evaluation.get("weaknesses", [])
        
        # Get context information
        current_difficulty = context.get("current_difficulty", "medium")
        covered_topics = context.get("covered_topics", [])
        performance_trend = context.get("performance_trend", "stable")
        question_count = context.get("question_count", 1)
        max_questions = context.get("max_questions", 8)
        
        prompt = f"""
Analyze this interview interaction and determine the optimal next step.

CONTEXT:
- Current Difficulty: {current_difficulty}
- Covered Topics: {', '.join(covered_topics) if covered_topics else 'None'}
- Performance Trend: {performance_trend}
- Question #{question_count} of {max_questions}

INTERACTION:
Question: "{question}"
Answer: "{answer}"

EVALUATION RESULTS:
Overall Score: {overall_score}/10
Component Scores: {scores}
Strengths: {', '.join(strengths[:3]) if strengths else 'None noted'}
Areas for Improvement: {', '.join(weaknesses[:3]) if weaknesses else 'None noted'}

ANALYZE AND RESPOND WITH JSON:
{{
    "effectiveness": "high|medium|low",
    "next_action": "deeper_probing|topic_switch|difficulty_adjustment|maintain_current",
    "reasoning": "Detailed explanation of your analysis and decision",
    "confidence": 0.0 to 1.0,
    "suggested_difficulty": "easy|medium|hard (if adjusting difficulty)",
    "suggested_topic": "topic name (if switching topics)",
    "probing_depth": 1|2|3 (if deeper probing - 1=basic follow-up, 2=detailed exploration, 3=thorough investigation)
}}

CRITERIA FOR EFFECTIVENESS:
HIGH: Revealed significant insights, exposed knowledge gaps, or demonstrated expertise
MEDIUM: Provided useful information but could go deeper
LOW: Answer was vague, evasive, or question didn't elicit meaningful response

DECISION GUIDELINES:
- DEEPER_PROBING: When candidate shows partial knowledge or interesting approach worth exploring
- TOPIC_SWITCH: When topic is exhausted, candidate is struggling, or need broader coverage
- DIFFICULTY_ADJUSTMENT: When performance clearly indicates need for easier/harder questions
- MAINTAIN_CURRENT: When current approach is working well and providing good insights

Provide specific, actionable reasoning that explains WHY you chose this action.
"""
        return prompt
    
    def _parse_reflection_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured data."""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                # Validate required fields
                required_fields = ["effectiveness", "next_action", "reasoning", "confidence"]
                if all(field in data for field in required_fields):
                    return data
            raise ValueError("Invalid response format")
        except Exception as e:
            logger.warning(f"Failed to parse reflection response: {str(e)}")
            # Return minimal valid structure
            return {
                "effectiveness": "medium",
                "next_action": "maintain_current",
                "reasoning": "Fallback analysis due to parsing error",
                "confidence": 0.5
            }
    
    def _fallback_reflection(
        self,
        evaluation: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ReflectionResult:
        """Fallback reflection when LLM fails."""
        score = evaluation.get("score", 5.0)
        question_count = context.get("question_count", 1)
        max_questions = context.get("max_questions", 8)
        
        # Simple rule-based reflection
        if score >= 8.0:
            effectiveness = QuestionEffectiveness.HIGH
            next_action = NextAction.DEEPER_PROBING
            reasoning = "Strong performance indicates deep knowledge - opportunity for deeper exploration"
        elif score >= 6.0:
            effectiveness = QuestionEffectiveness.MEDIUM
            next_action = NextAction.MAINTAIN_CURRENT
            reasoning = "Solid performance, continue with current approach"
        elif score >= 4.0:
            effectiveness = QuestionEffectiveness.MEDIUM
            next_action = NextAction.DIFFICULTY_ADJUSTMENT
            reasoning = "Moderate performance, consider adjusting difficulty level"
        else:
            effectiveness = QuestionEffectiveness.LOW
            next_action = NextAction.TOPIC_SWITCH
            reasoning = "Weak performance, switch to different topic to assess other areas"
        
        # Adjust for interview progress
        if question_count >= max_questions - 2:
            next_action = NextAction.MAINTAIN_CURRENT
            reasoning += " Approaching interview end, maintain current trajectory."
        
        return ReflectionResult(
            question_effectiveness=effectiveness,
            next_action=next_action,
            reasoning=reasoning,
            confidence=0.7
        )
    
    def get_reflection_summary(self) -> Dict[str, Any]:
        """Get summary of all reflections for reporting."""
        if not self.reflection_history:
            return {"message": "No reflections recorded"}
        
        # Calculate statistics
        effectiveness_counts = {}
        action_counts = {}
        
        for reflection in self.reflection_history:
            eff = reflection.question_effectiveness.value
            action = reflection.next_action.value
            effectiveness_counts[eff] = effectiveness_counts.get(eff, 0) + 1
            action_counts[action] = action_counts.get(action, 0) + 1
        
        avg_confidence = sum(r.confidence for r in self.reflection_history) / len(self.reflection_history)
        
        return {
            "total_reflections": len(self.reflection_history),
            "average_confidence": round(avg_confidence, 2),
            "effectiveness_distribution": effectiveness_counts,
            "action_distribution": action_counts,
            "recent_reflections": [
                r.to_dict() for r in self.reflection_history[-3:]
            ]  # Last 3 reflections
        }
    
    def reset(self) -> None:
        """Reset the reflection history for a new interview."""
        self.reflection_history.clear()
        logger.info("ReflectionAgent reset for new session")