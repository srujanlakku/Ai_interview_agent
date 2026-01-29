"""
Research Agent for company interview pattern research
"""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
from app.utils.exceptions import ResearchError
import json

logger = get_logger(__name__)


class ResearchAgent(BaseAgent):
    """Agent for researching company-specific interview patterns"""

    def __init__(self):
        super().__init__("ResearchAgent")

    async def execute(self, company_name: str, job_role: str) -> Dict[str, Any]:
        """Research company interview patterns"""
        try:
            logger.info(f"Starting research for {company_name} - {job_role}")

            # Execute research tasks
            faq_result = await self.retry_with_fallback(
                lambda: self.research_faq(company_name, job_role)
            )
            
            rounds_result = await self.retry_with_fallback(
                lambda: self.research_interview_rounds(company_name, job_role)
            )

            skills_result = await self.retry_with_fallback(
                lambda: self.research_required_skills(company_name, job_role)
            )

            criteria_result = await self.retry_with_fallback(
                lambda: self.research_evaluation_criteria(job_role)
            )

            research_data = {
                "company_name": company_name,
                "job_role": job_role,
                "frequently_asked_questions": faq_result.get("questions", []),
                "interview_rounds": rounds_result.get("rounds", {}),
                "evaluation_criteria": criteria_result.get("criteria", []),
                "required_skills": skills_result.get("skills", []),
                "technologies": skills_result.get("technologies", [])
            }

            logger.info(f"Research completed for {company_name}")
            return {"success": True, "data": research_data}

        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": self._get_fallback_research(company_name, job_role)
            }

    async def research_faq(self, company_name: str, job_role: str) -> Dict[str, Any]:
        """Research frequently asked questions"""
        try:
            prompt = f"""
            Based on your knowledge, what are the most frequently asked interview questions 
            for a {job_role} position at {company_name}?
            
            Provide 10-15 questions in a JSON array format like:
            {{"questions": ["question1", "question2", ...]}}
            
            Focus on:
            - Technical questions (if applicable)
            - Behavioral questions
            - Role-specific questions
            """

            response = await self.call_llm(
                prompt,
                system_message="You are an expert interview coach with deep knowledge of company-specific hiring practices.",
                temperature=0.5,
                max_tokens=1500
            )

            # Parse JSON response
            questions = self._extract_json(response, "questions", [])
            return {"questions": questions}

        except Exception as e:
            logger.error(f"FAQ research failed: {str(e)}")
            return {"questions": []}

    async def research_interview_rounds(self, company_name: str, job_role: str) -> Dict[str, Any]:
        """Research interview round structure"""
        try:
            prompt = f"""
            What is the typical interview process structure for a {job_role} at {company_name}?
            
            Provide in JSON format:
            {{
                "rounds": {{
                    "round_1": {{"name": "...", "duration": "...", "format": "...", "focus": "..."}},
                    "round_2": {{"name": "...", "duration": "...", "format": "...", "focus": "..."}},
                    ...
                }}
            }}
            
            Include details about:
            - Number of rounds
            - Format (phone, technical, in-person, etc.)
            - Duration
            - Focus areas
            """

            response = await self.call_llm(
                prompt,
                system_message="You are an expert recruiter with knowledge of hiring practices.",
                temperature=0.5,
                max_tokens=1500
            )

            rounds = self._extract_json(response, "rounds", {})
            return {"rounds": rounds}

        except Exception as e:
            logger.error(f"Interview rounds research failed: {str(e)}")
            return {"rounds": {}}

    async def research_required_skills(self, company_name: str, job_role: str) -> Dict[str, Any]:
        """Research required skills and technologies"""
        try:
            prompt = f"""
            What are the key technical skills and technologies required for a {job_role} at {company_name}?
            
            Provide in JSON format:
            {{
                "skills": ["skill1", "skill2", ...],
                "technologies": ["tech1", "tech2", ...]
            }}
            
            Prioritize by importance and frequency.
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a technical recruitment expert.",
                temperature=0.5,
                max_tokens=1000
            )

            data = self._extract_json(response, None, {})
            skills = data.get("skills", []) if isinstance(data, dict) else []
            technologies = data.get("technologies", []) if isinstance(data, dict) else []

            return {"skills": skills, "technologies": technologies}

        except Exception as e:
            logger.error(f"Skills research failed: {str(e)}")
            return {"skills": [], "technologies": []}

    async def research_evaluation_criteria(self, job_role: str) -> Dict[str, Any]:
        """Research evaluation criteria"""
        try:
            prompt = f"""
            What are the key evaluation criteria for a {job_role} interview?
            
            Provide in JSON format:
            {{"criteria": ["criterion1", "criterion2", ...]}}
            
            Include:
            - Technical competency areas
            - Soft skills being assessed
            - Problem-solving approaches
            - Communication skills
            """

            response = await self.call_llm(
                prompt,
                system_message="You are an interview evaluation expert.",
                temperature=0.5,
                max_tokens=1000
            )

            criteria = self._extract_json(response, "criteria", [])
            return {"criteria": criteria}

        except Exception as e:
            logger.error(f"Evaluation criteria research failed: {str(e)}")
            return {"criteria": []}

    def _extract_json(self, response: str, key: Optional[str] = None, default: Any = None) -> Any:
        """Extract JSON from LLM response"""
        try:
            # Try to parse the entire response as JSON
            if response.startswith("{") or response.startswith("["):
                data = json.loads(response)
                if key:
                    return data.get(key, default)
                return data
            
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                if key:
                    return data.get(key, default)
                return data
            
            return default
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to extract JSON: {str(e)}")
            return default

    def _get_fallback_research(self, company_name: str, job_role: str) -> Dict[str, Any]:
        """Return fallback research data when API fails"""
        return {
            "company_name": company_name,
            "job_role": job_role,
            "frequently_asked_questions": [
                "Tell me about yourself",
                "Why do you want to join our company?",
                "Describe your experience with relevant technologies",
                "How do you approach problem-solving?",
                "Tell me about a challenging project you worked on"
            ],
            "interview_rounds": {
                "round_1": {"name": "Phone Screen", "duration": "30-45 mins", "format": "Phone", "focus": "Background and basics"},
                "round_2": {"name": "Technical Round", "duration": "60 mins", "format": "Technical assessment", "focus": "Technical skills"}
            },
            "evaluation_criteria": [
                "Technical competency",
                "Problem-solving ability",
                "Communication skills",
                "Team collaboration",
                "Cultural fit"
            ],
            "required_skills": [
                "Strong problem-solving skills",
                "Communication skills",
                "Teamwork and collaboration"
            ],
            "technologies": ["Python", "JavaScript", "SQL"] if "engineer" in job_role.lower() else []
        }
