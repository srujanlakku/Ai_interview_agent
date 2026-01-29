"""
Resume Analyzer Agent - Analyzes resume content against job roles and companies.
"""
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class ResumeAnalyzerAgent(BaseAgent):
    """Agent for automated resume analysis and improvement suggestions"""

    def __init__(self):
        super().__init__("ResumeAnalyzerAgent")

    async def execute(self, 
                      resume_text: str, 
                      target_role: str, 
                      target_company: str = "General") -> Dict[str, Any]:
        """
        Analyzes the resume content and provides a rating with suggestions.
        """
        # Default template
        default_analysis = {
            "rating": 0,
            "strengths": [],
            "weaknesses": [],
            "missing_skills": [],
            "replace_suggestions": [],
            "rewrite_examples": []
        }
        
        try:
            prompt = f"""
            As an expert Career Coach and Technical Recruiter at {target_company}, analyze the following resume for a {target_role} position.
            
            Resume Content:
            {resume_text}
            
            Requirements:
            1. Provide an overall rating (1 to 5) where 1 is weak and 5 is interview-ready.
            2. Identify specific strengths and weaknesses.
            3. List critical missing skills for a {target_role} role.
            4. Identify overused/generic terms or poor impact statements.
            5. Provide concrete 'replace' suggestions and 'rewrite' examples.
            
            Return ONLY the JSON format below:
            {{
                "rating": 0.0 to 5.0,
                "strengths": ["list of strings"],
                "weaknesses": ["list of strings"],
                "missing_skills": ["list of strings"],
                "replace_suggestions": [
                    {{
                        "original": "generic word or short phrase",
                        "suggested": "impactful alternative"
                    }}
                ],
                "rewrite_examples": [
                    {{
                        "before": "weak bullet point",
                        "after": "improved impact-driven bullet point"
                    }}
                ]
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a professional resume reviewer specializing in high-growth tech companies. You provide precise, actionable, and deterministic feedback.",
                temperature=0.3,
                max_tokens=2000
            )

            result = self._extract_json(response)
            # Merge with defaults to ensure all keys exist
            return {**default_analysis, **result}

        except Exception as e:
            logger.error(f"ResumeAnalyzerAgent failed: {str(e)}")
            
            error_msg = str(e)
            user_feedback = "Analysis failed due to a system error."
            
            if "API key not configured" in error_msg:
                user_feedback = "LLM API keys (OpenAI/Anthropic) are not configured in the backend .env file."
            elif "Failed to get response from LLM services" in error_msg:
                user_feedback = "All LLM services are currently unavailable or rate-limited."
            
            return {
                **default_analysis,
                "rating": 0,
                "strengths": [f"⚠️ {user_feedback}"],
                "weaknesses": ["Please check your backend configuration (API keys in .env)."]
            }

    def _extract_json(self, response: str) -> Dict[str, Any]:
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception:
            return {}
