"""
Summary Agent - Generates the final interview report and readiness assessment.
"""
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class SummaryAgent(BaseAgent):
    """Agent for generating final interview summaries and readiness reports"""

    def __init__(self):
        super().__init__("SummaryAgent")

    async def execute(self, 
                      interview_data: Dict[str, Any], 
                      all_evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates a final report.
        """
        try:
            prompt = f"""
            As a SummaryAgent, compile the final interview report for the candidate.
            
            Interview Data: {json.dumps(interview_data)}
            All Question Evaluations: {json.dumps(all_evaluations)}
            
            Requirements:
            1. Summarize top strengths and key weaknesses across all questions.
            2. Provide a final overall score (0-10).
            3. Give actionable improvement suggestions.
            4. Assess 'Interview Readiness' (Not Ready | Almost Ready | Interview Ready).
            
            Return JSON:
            {{
                "final_score": 0 to 10,
                "readiness_level": "Not Ready | Almost Ready | Interview Ready",
                "summary_report": "Overall narrative summary",
                "key_strengths": ["list"],
                "main_weaknesses": ["list"],
                "improvement_plan": ["step 1", "step 2"],
                "category_scores": {{
                    "technical": 0 to 10,
                    "coding": 0 to 10,
                    "soft_skills": 0 to 10
                }}
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a career mentor and hiring manager. You provide a balanced, encouraging, but realistic assessment of a candidate's performance.",
                temperature=0.4,
                max_tokens=1000
            )

            return self._extract_json(response)

        except Exception as e:
            logger.error(f"SummaryAgent failed: {str(e)}")
            return {"final_score": 0, "summary_report": "Failed to generate report."}

    def _extract_json(self, response: str) -> Dict[str, Any]:
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception:
            return {}
