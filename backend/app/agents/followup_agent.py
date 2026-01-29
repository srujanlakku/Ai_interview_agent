"""
Follow-Up Agent - Analyzes candidate answers and decides whether to go deeper or switch topics.
"""
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class FollowUpAgent(BaseAgent):
    """Agent responsible for deciding on follow-up questions"""

    def __init__(self):
        super().__init__("FollowUpAgent")

    async def execute(self, 
                      question: str, 
                      answer: str, 
                      performance_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes the answer and decides on the next move.
        """
        try:
            prompt = f"""
            As a FollowUpAgent, analyze the candidate's answer and decide the next step.
            
            Question: {question}
            Candidate's Answer: {answer}
            Performance Context: {json.dumps(performance_context)}
            
            Decide if we should:
            1. Ask a deeper follow-up question (if the answer was good but could be more detailed, or if a specific gap exists).
            2. Increase difficulty (if the answer was perfect and effortless).
            3. Switch topic (if the answer was either satisfactory or completely failed, and it's time to move on).
            
            Return JSON:
            {{
                "decision": "follow_up | increase_difficulty | switch_topic",
                "reasoning": "Brief explanation",
                "follow_up_question": "Only if decision is follow_up",
                "suggested_next_topic": "Only if switching",
                "sentiment_score": 0.0 to 1.0
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a discerning interviewer. You know when to push a candidate deeper and when to move to a new topic.",
                temperature=0.6,
                max_tokens=500
            )

            result = self._extract_json(response)
            return result

        except Exception as e:
            logger.error(f"FollowUpAgent failed: {str(e)}")
            return {"decision": "switch_topic", "reasoning": "Error in agent", "sentiment_score": 0.5}

    def _extract_json(self, response: str) -> Dict[str, Any]:
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception:
            return {}
