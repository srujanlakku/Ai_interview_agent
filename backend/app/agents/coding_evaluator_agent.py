"""
Coding Evaluator Agent - Evaluates coding solutions based on multiple technical criteria.
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class CodingEvaluatorAgent(BaseAgent):
    """Agent for evaluating coding answers"""

    def __init__(self):
        super().__init__("CodingEvaluatorAgent")

    async def execute(self, 
                      problem: str, 
                      solution: str, 
                      expected_approach: str,
                      ideal_solution: str) -> Dict[str, Any]:
        """
        Evaluates a coding solution.
        """
        try:
            prompt = f"""
            As a CodingEvaluatorAgent, evaluate this candidate's code:
            
            Problem Statement: {problem}
            Expected Approach: {expected_approach}
            Ideal Solution Reference: {ideal_solution}
            
            Candidate's Code Solution:
            {solution}
            
            Evaluate based on:
            1. Correctness: Does it solve the problem?
            2. Time & Space Complexity: Is it optimal?
            3. Edge Cases: Does it handle empty input, large values, etc.?
            4. Code Clarity: Is it readable and well-structured?
            
            Return JSON:
            {{
                "score": 0 to 10,
                "feedback": "Overall evaluation summary",
                "rubric": {{
                    "correctness": 0 to 10,
                    "efficiency": 0 to 10,
                    "edge_cases": 0 to 10,
                    "clarity": 0 to 10
                }},
                "strengths": ["list"],
                "weaknesses": ["list"],
                "improvement_suggestions": "Specific advice"
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a principal software engineer. You provide tough but fair code reviews.",
                temperature=0.3,
                max_tokens=800
            )

            return self._extract_json(response)

        except Exception as e:
            logger.error(f"CodingEvaluatorAgent failed: {str(e)}")
            return {"score": 5, "feedback": "Evaluation error occurred."}

    def _extract_json(self, response: str) -> Dict[str, Any]:
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception:
            return {}
