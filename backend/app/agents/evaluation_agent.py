"""
Evaluation Agent for scoring interview answers.
Provides detailed assessment with cumulative scoring.
"""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent, LLMError

# Try to import logging
try:
    from app.utils.logging_config import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


class EvaluationAgent(BaseAgent):
    """
    Agent for evaluating interview answers.
    
    Features:
    - Score on technical correctness, depth, and clarity
    - Maintain cumulative scoring state
    - Generate actionable feedback
    """

    def __init__(self):
        super().__init__("EvaluationAgent")
        self._cumulative_scores: List[Dict[str, float]] = []

    async def execute(
        self,
        question: str,
        answer: str,
        question_type: str = "technical",
        ideal_answer_points: Optional[List[str]] = None,
        experience_level: str = "mid",
    ) -> Dict[str, Any]:
        """
        Evaluate a single interview answer with explainable output.
        
        Args:
            question: The interview question
            answer: User's answer
            question_type: Type of question (technical, coding, behavioral)
            ideal_answer_points: Expected key points in answer
            experience_level: User's experience level
            
        Returns:
            Evaluation dictionary with scores, reasons, and actionable feedback
        """
        try:
            logger.info(f"Evaluating {question_type} answer")
            
            # Handle empty or very short answers
            if not answer or len(answer.strip()) < 10:
                return self._create_low_score_evaluation(
                    "Answer is too short or empty. Please provide a more detailed response."
                )
            
            # Build evaluation prompt with explainable structure
            ideal_points_str = ""
            if ideal_answer_points:
                ideal_points_str = f"\nKey points expected:\n- " + "\n- ".join(ideal_answer_points)
            
            prompt = f"""
Evaluate this interview answer for a {experience_level}-level candidate.

Question Type: {question_type}
Question: {question}

Candidate's Answer: {answer}
{ideal_points_str}

Provide a detailed evaluation in JSON format:
{{
    "score": <0-10 overall score>,
    "score_reasoning": "Why this score was given",
    "technical_accuracy": <0-10>,
    "depth_of_understanding": <0-10>,
    "communication_clarity": <0-10>,
    "strengths": ["specific strength 1", "specific strength 2"],
    "what_was_done_well": ["what was done well", "specific positive aspects"],
    "what_was_missing": ["what was missing", "areas that were weak"],
    "feedback": "Constructive feedback paragraph explaining performance",
    "improvement_suggestions": ["specific actionable suggestion 1", "specific actionable suggestion 2"]
}}

Scoring Guidelines:
- 0-3: Poor - Major gaps, incorrect information, unclear
- 4-5: Below Average - Some correct points but significant gaps
- 6-7: Good - Solid understanding with minor gaps
- 8-9: Excellent - Comprehensive, well-explained
- 10: Outstanding - Perfect answer with extra insights
"""

            system_prompt = """You are an expert technical interviewer evaluating candidate responses.
Be fair, constructive, and specific in your feedback. Consider the candidate's experience level
when scoring. Provide actionable improvement suggestions."""

            response = await self.call_llm(
                prompt,
                system_message=system_prompt,
                temperature=0.4,
                max_tokens=800,
            )

            evaluation = self.extract_json_with_default(response, self._default_evaluation())
            
            # Ensure score is within bounds
            evaluation["score"] = max(0, min(10, float(evaluation.get("score", 5))))
            
            # Add fallback for missing fields
            if "what_was_done_well" not in evaluation:
                evaluation["what_was_done_well"] = evaluation.get("strengths", [])
            if "what_was_missing" not in evaluation:
                evaluation["what_was_missing"] = evaluation.get("weaknesses", evaluation.get("improvement_suggestions", []))
            
            # Store for cumulative tracking
            self._cumulative_scores.append({
                "score": evaluation["score"],
                "technical_accuracy": evaluation.get("technical_accuracy", 5),
                "depth_of_understanding": evaluation.get("depth_of_understanding", 5),
                "communication_clarity": evaluation.get("communication_clarity", 5),
            })
            
            return evaluation

        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            return self._default_evaluation()

    async def evaluate_coding_answer(
        self,
        problem: str,
        solution: str,
        expected_approach: Optional[str] = None,
        ideal_solution: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate a coding problem solution.
        
        Args:
            problem: The coding problem statement
            solution: User's code solution
            expected_approach: Expected solution approach
            ideal_solution: Reference solution (optional)
            
        Returns:
            Evaluation dictionary with scores and feedback
        """
        try:
            logger.info("Evaluating coding solution")
            
            if not solution or len(solution.strip()) < 20:
                return self._create_low_score_evaluation(
                    "No valid code solution provided."
                )
            
            approach_hint = ""
            if expected_approach:
                approach_hint = f"\nExpected Approach: {expected_approach}"
            
            prompt = f"""
Evaluate this coding solution:

Problem: {problem}
{approach_hint}

Candidate's Solution:
```
{solution}
```

Provide evaluation in JSON format:
{{
    "score": <0-10 overall>,
    "correctness": <0-10>,
    "efficiency": <0-10>,
    "code_quality": <0-10>,
    "approach_analysis": "Brief analysis of the approach",
    "strengths": ["specific strength"],
    "weaknesses": ["specific weakness"],
    "feedback": "Constructive feedback",
    "time_complexity": "Estimated time complexity",
    "space_complexity": "Estimated space complexity"
}}
"""

            system_prompt = """You are a senior software engineer evaluating code.
Assess correctness, efficiency, readability, and best practices.
Be fair but thorough in identifying issues."""

            response = await self.call_llm(
                prompt,
                system_message=system_prompt,
                temperature=0.3,
                max_tokens=800,
            )

            evaluation = self.extract_json_with_default(response, self._default_coding_evaluation())
            evaluation["score"] = max(0, min(10, float(evaluation.get("score", 5))))
            
            return evaluation

        except Exception as e:
            logger.error(f"Coding evaluation failed: {str(e)}")
            return self._default_coding_evaluation()

    def get_cumulative_scores(self) -> Dict[str, float]:
        """
        Get cumulative scores across all evaluations.
        
        Returns:
            Dictionary with average scores
        """
        if not self._cumulative_scores:
            return {
                "average_score": 0,
                "technical_average": 0,
                "depth_average": 0,
                "clarity_average": 0,
                "total_questions": 0,
            }
        
        n = len(self._cumulative_scores)
        return {
            "average_score": sum(s["score"] for s in self._cumulative_scores) / n,
            "technical_average": sum(s["technical_accuracy"] for s in self._cumulative_scores) / n,
            "depth_average": sum(s["depth_of_understanding"] for s in self._cumulative_scores) / n,
            "clarity_average": sum(s["communication_clarity"] for s in self._cumulative_scores) / n,
            "total_questions": n,
        }

    def reset_cumulative_scores(self) -> None:
        """Reset cumulative scoring for a new session."""
        self._cumulative_scores = []

    def _default_evaluation(self) -> Dict[str, Any]:
        """Return default evaluation structure."""
        return {
            "score": 5.0,
            "technical_accuracy": 5.0,
            "depth_of_understanding": 5.0,
            "communication_clarity": 5.0,
            "strengths": ["Attempted to answer"],
            "weaknesses": ["Could be more detailed"],
            "feedback": "Thank you for your response. Consider providing more specific details.",
            "improvement_suggestions": ["Add concrete examples", "Explain reasoning step by step"],
        }

    def _default_coding_evaluation(self) -> Dict[str, Any]:
        """Return default coding evaluation structure."""
        return {
            "score": 5.0,
            "correctness": 5.0,
            "efficiency": 5.0,
            "code_quality": 5.0,
            "approach_analysis": "Unable to fully analyze the approach.",
            "strengths": ["Code was provided"],
            "weaknesses": ["Could not fully evaluate"],
            "feedback": "Please ensure your code is complete and handles edge cases.",
            "time_complexity": "Unknown",
            "space_complexity": "Unknown",
        }

    def _create_low_score_evaluation(self, reason: str) -> Dict[str, Any]:
        """Create a low score evaluation with specific reason."""
        return {
            "score": 2.0,
            "technical_accuracy": 2.0,
            "depth_of_understanding": 2.0,
            "communication_clarity": 2.0,
            "strengths": [],
            "weaknesses": [reason],
            "feedback": reason,
            "improvement_suggestions": [
                "Provide a complete answer",
                "Explain your thought process",
            ],
        }

