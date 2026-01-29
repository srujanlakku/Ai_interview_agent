"""
Interviewer Agent for conducting mock interviews
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
from app.utils.exceptions import LLMError
import json

logger = get_logger(__name__)


class InterviewerAgent(BaseAgent):
    """Agent for conducting mock interviews"""

    def __init__(self):
        super().__init__("InterviewerAgent")
        self.current_difficulty = "medium"
        self.question_count = 0
        self.max_questions = 10

    async def execute(self, user_profile: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Start interview session"""
        try:
            logger.info("Starting interview session")
            self.question_count = 0
            
            # Generate initial context
            system_context = self._build_interview_context(user_profile, research_data)
            
            # Generate first question
            first_question = await self.generate_next_question(
                system_context,
                user_profile.get("experience_level", "Junior"),
                []
            )

            return {
                "success": True,
                "interview_started": True,
                "question": first_question,
                "question_number": 1
            }
        except Exception as e:
            logger.error(f"Failed to start interview: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "interview_started": False
            }

    async def generate_next_question(self, system_context: str, experience_level: str,
                                    previous_answers: List[str]) -> str:
        """Generate next interview question"""
        try:
            if self.question_count >= self.max_questions:
                return "Thank you for completing the mock interview!"

            prompt = f"""
            Based on the following context, generate a single interview question:
            
            Experience Level: {experience_level}
            Difficulty: {self.current_difficulty}
            Previous Questions Count: {len(previous_answers)}
            
            {system_context}
            
            Requirements:
            - Make the question clear and specific
            - Avoid repetition from previous topics
            - Adapt difficulty based on feedback
            - Return ONLY the question text, no numbering or extra formatting
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a professional technical interviewer. Generate realistic interview questions.",
                temperature=0.7,
                max_tokens=300
            )

            self.question_count += 1
            return response.strip()

        except Exception as e:
            logger.error(f"Failed to generate question: {str(e)}")
            raise LLMError("Could not generate interview question")

    async def evaluate_answer(self, question: str, user_answer: str, 
                             experience_level: str) -> Dict[str, Any]:
        """Evaluate user's answer"""
        try:
            prompt = f"""
            Evaluate the following interview answer:
            
            Question: {question}
            User's Answer: {user_answer}
            Experience Level: {experience_level}
            
            Provide evaluation in JSON format:
            {{
                "score": <0-10>,
                "strengths": ["strength1", "strength2"],
                "weaknesses": ["weakness1", "weakness2"],
                "feedback": "Specific feedback",
                "suggested_improvement": "How to improve",
                "difficulty_adjustment": "increase|maintain|decrease"
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are an expert interview evaluator. Provide constructive feedback.",
                temperature=0.5,
                max_tokens=500
            )

            evaluation = self._extract_json(response)
            return evaluation

        except Exception as e:
            logger.error(f"Failed to evaluate answer: {str(e)}")
            return {
                "score": 5,
                "feedback": "Unable to evaluate at this moment",
                "difficulty_adjustment": "maintain"
            }

    async def generate_follow_up(self, original_question: str, user_answer: str) -> str:
        """Generate follow-up question based on answer quality"""
        try:
            prompt = f"""
            Based on the user's answer quality, generate a thoughtful follow-up question:
            
            Original Question: {original_question}
            User's Answer: {user_answer}
            
            The follow-up should:
            - Dive deeper into their understanding
            - Address any gaps in their answer
            - Test their thinking process
            - Return ONLY the question text
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a technical interviewer generating thoughtful follow-ups.",
                temperature=0.6,
                max_tokens=300
            )

            return response.strip()

        except Exception as e:
            logger.error(f"Failed to generate follow-up: {str(e)}")
            return ""

    def adjust_difficulty(self, performance_score: float) -> None:
        """Adjust interview difficulty based on performance"""
        if performance_score >= 8:
            self.current_difficulty = "hard"
        elif performance_score >= 6:
            self.current_difficulty = "medium"
        else:
            self.current_difficulty = "easy"
        logger.info(f"Difficulty adjusted to: {self.current_difficulty}")

    def _build_interview_context(self, user_profile: Dict[str, Any], 
                                research_data: Dict[str, Any]) -> str:
        """Build interview context string"""
        context = f"""
        Interview Context:
        - Target Company: {user_profile.get('target_company', 'Unknown')}
        - Target Role: {user_profile.get('target_role', 'Unknown')}
        - Interview Type: {user_profile.get('interview_type', 'Mixed')}
        - Experience Level: {user_profile.get('experience_level', 'Junior')}
        
        Company Research:
        - FAQ Topics: {', '.join(research_data.get('frequently_asked_questions', [])[:5])}
        - Required Skills: {', '.join(research_data.get('required_skills', [])[:5])}
        """
        return context

    def _extract_json(self, response: str) -> Dict[str, Any]:
        """Extract JSON from response"""
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except (json.JSONDecodeError, ValueError):
            logger.warning("Failed to extract JSON from evaluation")
            return {}
