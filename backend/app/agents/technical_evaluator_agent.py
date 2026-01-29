"""
Technical Evaluator Agent - Evaluates technical theory answers for accuracy and depth.
"""
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class TechnicalEvaluatorAgent(BaseAgent):
    """Agent for evaluating technical theory answers"""

    def __init__(self):
        super().__init__("TechnicalEvaluatorAgent")

    async def execute(self, 
                      question: str, 
                      answer: str, 
                      ideal_answer_points: List[str]) -> Dict[str, Any]:
        """
        Evaluates a technical question.
        """
        try:
            prompt = f"""
            As a TechnicalEvaluatorAgent, evaluate this answer for accuracy and depth.
            
            Question: {question}
            Candidate's Answer: {answer}
            Expected Key Points: {', '.join(ideal_answer_points)}
            
            Focus on:
            1. Accuracy: Is the information technically correct?
            2. Conceptual Depth: Does the candidate understand the 'why'?
            3. Practical Understanding: Can they apply the concept?
            
            Return JSON:
            {{
                "score": 0 to 10,
                "feedback": "Detailed technical feedback",
                "accuracy_score": 0 to 10,
                "depth_score": 0 to 10,
                "missing_concepts": ["concept1", "concept2"],
                "is_factually_correct": true/false
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a senior technical lead. You value precision and deep understanding.",
                temperature=0.3,
                max_tokens=600
            )

            return self._extract_json(response)

        except Exception as e:
            logger.error(f"TechnicalEvaluatorAgent failed: {str(e)}")
            return {"score": 5, "feedback": "Evaluation error."}

    def _extract_json(self, response: str) -> Dict[str, Any]:
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception:
            return {}
