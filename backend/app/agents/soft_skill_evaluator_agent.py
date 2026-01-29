"""
Soft Skill Evaluator Agent - Evaluates communication, confidence, and structured thinking.
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class SoftSkillEvaluatorAgent(BaseAgent):
    """Agent for evaluating soft skills and communication"""

    def __init__(self):
        super().__init__("SoftSkillEvaluatorAgent")

    async def execute(self, 
                      question: str, 
                      answer: str) -> Dict[str, Any]:
        """
        Evaluates soft skills shown in the answer.
        """
        try:
            prompt = f"""
            As a SoftSkillEvaluatorAgent, evaluate the candidate's communication and behavioral traits.
            
            Question: {question}
            Answer: {answer}
            
            Focus on:
            1. Communication Clarity: Is the message easy to follow?
            2. Confidence: Does the tone sound sure?
            3. Structured Thinking: Is there a beginning, middle, and end (e.g., STAR method)?
            4. Professional Tone: Is the language appropriate?
            
            Return JSON:
            {{
                "score": 0 to 10,
                "feedback": "Communication feedback",
                "clarity": 0 to 10,
                "confidence": 0 to 10,
                "structure": 0 to 10,
                "tone": "professional | casual | hesitant",
                "strengths": ["list"],
                "improvements": ["list"]
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are an expert HR and behavioral coach. You focus on how things are said as much as what is said.",
                temperature=0.5,
                max_tokens=600
            )

            return self._extract_json(response)

        except Exception as e:
            logger.error(f"SoftSkillEvaluatorAgent failed: {str(e)}")
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
