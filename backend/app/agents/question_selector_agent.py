"""
Question Selector Agent - Selects questions from local repository with LLM fallback.
Uses intelligent selection to avoid repetition and adapt difficulty.
"""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent, LLMError
from app.schemas.question_schema import InterviewQuestion, QuestionFilter
from app.data.question_repository import get_question_repository

# Try to import logging
try:
    from app.utils.logging_config import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


class QuestionSelectorAgent(BaseAgent):
    """
    Agent responsible for selecting interview questions.
    
    Strategy:
    1. First, try to select from local question repository
    2. If no suitable question found, fall back to LLM generation
    3. Prevent topic repetition and adapt to difficulty level
    """

    def __init__(self):
        super().__init__("QuestionSelectorAgent")
        self._repository = get_question_repository()

    async def execute(
        self,
        role: str,
        experience_level: str = "mid",
        difficulty: str = "medium",
        asked_question_ids: Optional[List[str]] = None,
        asked_topics: Optional[List[str]] = None,
        prefer_type: Optional[str] = None,
        company: Optional[str] = None,
        resume_skills: Optional[List[str]] = None,
        resume_projects: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Select the next interview question.
        
        Args:
            role: Target role (e.g., "Software Engineer", "Backend Developer")
            experience_level: fresher, mid, or senior
            difficulty: easy, medium, or hard
            asked_question_ids: List of already asked question IDs
            asked_topics: List of already covered topics
            prefer_type: Preferred question type (technical, coding, behavioral)
            company: Target company (optional)
            resume_skills: Skills extracted from candidate's resume (optional)
            resume_projects: Projects extracted from candidate's resume (optional)
            
        Returns:
            Dictionary with question details
        """
        asked_question_ids = asked_question_ids or []
        asked_topics = asked_topics or []
        
        logger.info(f"Selecting question for {role} at {difficulty} difficulty")
        
        # Try local repository first
        question = self._select_from_repository(
            role=role,
            difficulty=difficulty,
            asked_question_ids=asked_question_ids,
            asked_topics=asked_topics,
            prefer_type=prefer_type,
            company=company,
            resume_skills=resume_skills,
            resume_projects=resume_projects,
        )
        
        if question:
            logger.info(f"Selected question from repository: {question.topic}")
            return self._format_question(question)
        
        # Fall back to LLM generation
        logger.info("No suitable question in repository, generating with LLM")
        return await self._generate_question_with_llm(
            role=role,
            experience_level=experience_level,
            difficulty=difficulty,
            asked_topics=asked_topics,
            prefer_type=prefer_type,
            resume_skills=resume_skills,
            resume_projects=resume_projects,
        )

    def _select_from_repository(
        self,
        role: str,
        difficulty: str,
        asked_question_ids: List[str],
        asked_topics: List[str],
        prefer_type: Optional[str],
        company: Optional[str],
        resume_skills: Optional[List[str]] = None,
        resume_projects: Optional[List[str]] = None,
    ) -> Optional[InterviewQuestion]:
        """
        Select a question from the local repository.
        
        Args:
            role: Target role
            difficulty: Difficulty level
            asked_question_ids: Questions to exclude
            asked_topics: Topics to deprioritize
            prefer_type: Preferred question type
            company: Target company
            
        Returns:
            Selected question or None
        """
        return self._repository.select_next_question(
            role=role,
            difficulty=difficulty,
            asked_questions=asked_question_ids,
            asked_topics=asked_topics,
            prefer_type=prefer_type,
            resume_skills=resume_skills,
            resume_projects=resume_projects,
        )

    async def _generate_question_with_llm(
        self,
        role: str,
        experience_level: str,
        difficulty: str,
        asked_topics: List[str],
        prefer_type: Optional[str],
        resume_skills: Optional[List[str]] = None,
        resume_projects: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a question using LLM when repository doesn't have suitable options.
        
        Args:
            role: Target role
            experience_level: Experience level
            difficulty: Difficulty level
            asked_topics: Topics already covered
            prefer_type: Preferred question type
            resume_skills: Skills from candidate's resume (optional)
            resume_projects: Projects from candidate's resume (optional)
            
        Returns:
            Generated question dictionary
        """
        # Determine question type if not specified
        if not prefer_type:
            # Rotate between types based on topic count
            type_rotation = ["technical", "behavioral", "technical", "coding"]
            prefer_type = type_rotation[len(asked_topics) % len(type_rotation)]
        
        topics_to_avoid = ", ".join(asked_topics[-5:]) if asked_topics else "None yet"
        
        # Build resume context if available
        resume_context = ""
        if resume_skills and isinstance(resume_skills, list):
            resume_context += f"\nCandidate Skills: {', '.join(str(skill) for skill in resume_skills[:10])}"  # Limit to first 10 skills
        if resume_projects and isinstance(resume_projects, list):
            # Handle mixed types in resume_projects list
            project_descriptions = []
            for proj in resume_projects[:5]:
                if isinstance(proj, dict):
                    # Extract description from dictionary
                    project_descriptions.append(proj.get("description", "Project"))
                else:
                    # Convert string/object to string representation
                    proj_str = str(proj)
                    if len(proj_str) > 50:
                        proj_str = proj_str[:50] + "..."
                    project_descriptions.append(proj_str)
            
            if project_descriptions:
                resume_context += f"\nCandidate Projects: {', '.join(str(desc) for desc in project_descriptions)}"
        
        prompt = f"""
Generate a single {prefer_type} interview question for the following context:

Role: {role}
Experience Level: {experience_level}
Difficulty: {difficulty}
Topics Already Covered: {topics_to_avoid}{resume_context}

Requirements:
1. Generate ONE question only
2. Do NOT repeat topics already covered
3. Question should match the {difficulty} difficulty level
4. For {experience_level} level, calibrate complexity appropriately
5. If resume skills/projects are provided, consider them for relevance

Return JSON:
{{
    "question_text": "The interview question",
    "question_type": "{prefer_type}",
    "topic": "Specific topic name",
    "difficulty": "{difficulty}",
    "ideal_answer_points": ["key point 1", "key point 2", "key point 3"]
}}
"""

        system_prompt = f"""You are a senior technical interviewer for {role} positions.
Generate relevant, practical interview questions that test real-world knowledge.
Ensure questions are clear, specific, and appropriate for {experience_level} candidates."""

        try:
            response = await self.call_llm(
                prompt,
                system_message=system_prompt,
                temperature=0.8,
                max_tokens=500,
            )
            
            result = self.extract_json_with_default(response, self._fallback_question(prefer_type))
            
            # Ensure required fields
            result.setdefault("question_type", prefer_type)
            result.setdefault("difficulty", difficulty)
            result.setdefault("topic", "General")
            result.setdefault("ideal_answer_points", ["Provide clear explanation"])
            
            return result
            
        except Exception as e:
            logger.error(f"LLM question generation failed: {str(e)}")
            return self._fallback_question(prefer_type)

    def _format_question(self, question: InterviewQuestion) -> Dict[str, Any]:
        """
        Format an InterviewQuestion into the expected dictionary format.
        
        Args:
            question: InterviewQuestion instance
            
        Returns:
            Formatted question dictionary
        """
        result = {
            "question_id": question.question_id,
            "question_text": question.question_text,
            "question_type": question.question_type,
            "topic": question.topic,
            "difficulty": question.difficulty,
            "ideal_answer_points": question.ideal_answer_points,
        }
        
        # Add coding data if present
        if question.coding_data:
            result["coding_data"] = {
                "problem_statement": question.coding_data.problem_statement,
                "expected_approach": question.coding_data.expected_approach,
                "code_solution": question.coding_data.code_solution,
            }
        
        return result

    def _fallback_question(self, question_type: str) -> Dict[str, Any]:
        """
        Return a fallback question when all else fails.
        
        Args:
            question_type: Type of question requested
            
        Returns:
            Fallback question dictionary
        """
        fallbacks = {
            "technical": {
                "question_text": "Describe a technical challenge you faced recently and how you solved it.",
                "question_type": "technical",
                "topic": "Problem Solving",
                "difficulty": "medium",
                "ideal_answer_points": [
                    "Clear problem description",
                    "Analysis approach",
                    "Solution implemented",
                    "Lessons learned",
                ],
            },
            "behavioral": {
                "question_text": "Tell me about a time when you had to work under pressure to meet a deadline.",
                "question_type": "behavioral",
                "topic": "Time Management",
                "difficulty": "medium",
                "ideal_answer_points": [
                    "Situation context",
                    "Actions taken",
                    "Results achieved",
                    "What you learned",
                ],
            },
            "coding": {
                "question_text": "Write a function to check if a string is a valid palindrome, considering only alphanumeric characters.",
                "question_type": "coding",
                "topic": "String Manipulation",
                "difficulty": "easy",
                "ideal_answer_points": [
                    "Handle edge cases",
                    "Efficient algorithm",
                    "Clean code",
                ],
                "coding_data": {
                    "problem_statement": "Check if a string is a valid palindrome (alphanumeric only, case insensitive)",
                    "expected_approach": "Two pointer technique or string reversal",
                    "code_solution": None,
                },
            },
            "system_design": {
                "question_text": "How would you design a URL shortener service like bit.ly?",
                "question_type": "system_design",
                "topic": "System Design",
                "difficulty": "medium",
                "ideal_answer_points": [
                    "Requirements clarification",
                    "High-level design",
                    "Database schema",
                    "Scalability considerations",
                ],
            },
        }
        
        return fallbacks.get(question_type, fallbacks["technical"])

    def get_available_roles(self) -> List[str]:
        """Get list of available roles."""
        return self._repository.get_available_roles()

    def get_topics_for_role(self, role: str) -> List[str]:
        """Get available topics for a specific role."""
        return self._repository.get_topics_for_role(role)

