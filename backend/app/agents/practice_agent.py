"""
Practice Agent - Handles educational skill practice mode.
"""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class PracticeAgent(BaseAgent):
    """Agent for educational practice flow: Explain -> Question -> Feedback"""

    def __init__(self):
        super().__init__("PracticeAgent")

    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Generic execute for BaseAgent compatibility. 
        Delegates to get_next_step by default if called directly."""
        return await self.get_next_step(*args, **kwargs)

    async def get_next_step(self, 
                            skill_category: str, 
                            level: str, 
                            history: List[Dict[str, Any]] = []) -> Dict[str, Any]:
        """
        Generates an educational explanation followed by a practice question.
        """
        try:
            prompt = f"""
            You are an expert Educational Coach. Your goal is to help the user practice '{skill_category}' at a '{level}' level.
            
            Context: This is NOT a high-pressure interview. Use an 'explain-first' approach.
            
            Previous Practice History: {json.dumps(history[-3:]) if history else "Start of session"}
            
            Requirements:
            1. Select a specific concept or sub-topic within '{skill_category}'.
            2. PROVIDE A CLEAR, CONCISE EXPLANATION of the concept (2-3 paragraphs).
            3. ASK ONE FOCUSED PRACTICE QUESTION based on that explanation.
            
            Return ONLY the JSON format below:
            {{
                "concept": "Name of the concept",
                "explanation": "Markdown formatted explanation",
                "practice_question": "The question for the user to answer"
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a helpful and detailed teacher who explains things clearly before asking questions.",
                temperature=0.7
            )

            return self._extract_json(response)

        except Exception as e:
            logger.error(f"PracticeAgent.get_next_step failed: {str(e)}")
            return {}

    async def evaluate_answer(self, 
                             concept: str,
                             question: str, 
                             user_answer: str) -> Dict[str, Any]:
        """
        Evaluates the user's answer with detailed feedback and improvement tips.
        """
        try:
            prompt = f"""
            Concept: {concept}
            Question: {question}
            User Answer: {user_answer}
            
            Evaluate this answer educationally.
            
            Requirements:
            1. Provide positive but honest feedback.
            2. Explain the 'Correct Approach' or 'Ideal Answer' in detail.
            3. Provide 3-4 specific improvement tips.
            
            Return ONLY the JSON format below:
            {{
                "feedback": "Your educational feedback",
                "correct_approach": "Detailed ideal approach explanation",
                "improvement_tips": ["tip 1", "tip 2", "tip 3"],
                "score_estimate": 0.0 to 10.0
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are an encouraging educational evaluator. Focus on growth and understanding.",
                temperature=0.4
            )

            return self._extract_json(response)

        except Exception as e:
            logger.error(f"PracticeAgent.evaluate_answer failed: {str(e)}")
            return {}

    def _extract_json(self, response: str) -> Dict[str, Any]:
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception:
            return {}
