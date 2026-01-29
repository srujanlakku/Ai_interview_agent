"""
Evaluation and Scoring Agent
"""
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)


class EvaluationAgent(BaseAgent):
    """Agent for evaluating interview performance and generating scores"""

    def __init__(self):
        super().__init__("EvaluationAgent")

    async def execute(self, interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate complete interview"""
        try:
            logger.info("Evaluating interview")

            questions = interview_data.get("questions", [])
            user_profile = interview_data.get("user_profile", {})

            if not questions:
                return {
                    "success": False,
                    "error": "No questions to evaluate",
                    "score": 0
                }

            # Evaluate each question
            question_evaluations = []
            for q in questions:
                eval_result = await self.evaluate_single_answer(
                    q.get("question_text", ""),
                    q.get("user_answer", ""),
                    user_profile.get("experience_level", "Junior")
                )
                question_evaluations.append(eval_result)

            # Calculate aggregate scores
            scores = self._calculate_scores(question_evaluations)
            readiness = self._determine_readiness(scores)
            feedback = await self._generate_feedback(scores, question_evaluations)

            return {
                "success": True,
                "scores": scores,
                "readiness_level": readiness,
                "feedback": feedback,
                "question_evaluations": question_evaluations
            }

        except Exception as e:
            logger.error(f"Failed to evaluate interview: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "score": 0
            }

    async def evaluate_single_answer(self, question: str, answer: str, 
                                    experience_level: str) -> Dict[str, Any]:
        """Evaluate a single answer"""
        try:
            prompt = f"""
            Evaluate this interview answer for a {experience_level} candidate:
            
            Question: {question}
            Answer: {answer}
            
            Assess on:
            1. Technical Accuracy (0-10)
            2. Conceptual Clarity (0-10)
            3. Communication (0-10)
            4. Structure and Reasoning (0-10)
            
            Return JSON:
            {{
                "technical_accuracy": <0-10>,
                "conceptual_clarity": <0-10>,
                "communication": <0-10>,
                "structure": <0-10>,
                "average_score": <0-10>,
                "strengths": ["strength1", "strength2"],
                "areas_to_improve": ["area1", "area2"],
                "feedback": "Specific feedback"
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are an expert technical interviewer and evaluator.",
                temperature=0.5,
                max_tokens=800
            )

            evaluation = self._extract_json(response)
            return evaluation if evaluation else self._default_evaluation()

        except Exception as e:
            logger.error(f"Failed to evaluate single answer: {str(e)}")
            return self._default_evaluation()

    def _calculate_scores(self, evaluations: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate aggregate scores"""
        try:
            if not evaluations:
                return {
                    "overall_score": 0,
                    "technical_accuracy": 0,
                    "conceptual_clarity": 0,
                    "communication": 0,
                    "structure": 0
                }

            num_questions = len(evaluations)
            tech_acc = sum(e.get("technical_accuracy", 5) for e in evaluations) / num_questions
            concept = sum(e.get("conceptual_clarity", 5) for e in evaluations) / num_questions
            comm = sum(e.get("communication", 5) for e in evaluations) / num_questions
            struct = sum(e.get("structure", 5) for e in evaluations) / num_questions

            overall = (tech_acc + concept + comm + struct) / 4

            return {
                "overall_score": round(overall, 1),
                "technical_accuracy": round(tech_acc, 1),
                "conceptual_clarity": round(concept, 1),
                "communication": round(comm, 1),
                "structure": round(struct, 1)
            }

        except Exception as e:
            logger.error(f"Error calculating scores: {str(e)}")
            return {
                "overall_score": 5,
                "technical_accuracy": 5,
                "conceptual_clarity": 5,
                "communication": 5,
                "structure": 5
            }

    def _determine_readiness(self, scores: Dict[str, float]) -> str:
        """Determine interview readiness level"""
        overall_score = scores.get("overall_score", 0)

        if overall_score >= 8:
            return "Interview Ready"
        elif overall_score >= 6:
            return "Almost Ready"
        else:
            return "Not Ready"

    async def _generate_feedback(self, scores: Dict[str, float],
                                evaluations: List[Dict[str, Any]]) -> str:
        """Generate overall feedback"""
        try:
            strengths = []
            weaknesses = []

            for eval in evaluations:
                strengths.extend(eval.get("strengths", [])[:1])
                weaknesses.extend(eval.get("areas_to_improve", [])[:1])

            prompt = f"""
            Generate constructive feedback based on:
            
            Overall Score: {scores['overall_score']}/10
            Technical: {scores['technical_accuracy']}/10
            Communication: {scores['communication']}/10
            
            Top Strengths: {', '.join(set(strengths)[:3])}
            Areas to Improve: {', '.join(set(weaknesses)[:3])}
            
            Provide concise, actionable feedback (2-3 sentences).
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a professional interview coach providing feedback.",
                temperature=0.6,
                max_tokens=400
            )

            return response.strip()

        except Exception as e:
            logger.error(f"Failed to generate feedback: {str(e)}")
            return "Continue practicing with more mock interviews to improve your skills."

    def _default_evaluation(self) -> Dict[str, Any]:
        """Return default evaluation"""
        return {
            "technical_accuracy": 5,
            "conceptual_clarity": 5,
            "communication": 5,
            "structure": 5,
            "average_score": 5,
            "strengths": ["Participated"],
            "areas_to_improve": ["Clarity"],
            "feedback": "Keep practicing"
        }

    def _extract_json(self, response: str) -> Dict[str, Any]:
        """Extract JSON from response"""
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return None
        except (json.JSONDecodeError, ValueError):
            logger.warning("Failed to extract JSON from evaluation")
            return None
