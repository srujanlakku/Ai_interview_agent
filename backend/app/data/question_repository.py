"""
Question Repository for the AI Interview Agent.
Loads, normalizes, and provides access to interview questions.
"""
import random
import hashlib
from typing import List, Optional, Dict, Any
from app.schemas.question_schema import InterviewQuestion, QuestionFilter, CodingProblem
from app.data.interview_seed_data import (
    INTERVIEW_QUESTIONS_DATA,
    ROLES_DATA,
    COMPANIES_DATA,
)


class QuestionRepository:
    """Repository for managing interview questions with filtering and selection."""
    
    # Role ID to display name mapping
    ROLE_MAPPING = {
        "sde": "Software Engineer",
        "backend": "Backend Developer",
        "frontend": "Frontend Developer",
        "fullstack": "Full Stack Developer",
        "dataeng": "Data Engineer",
        "datascientist": "Data Scientist",
        "mleng": "AI/ML Engineer",
        "devops": "DevOps Engineer",
        "qa": "QA/Automation Engineer",
        "sysdesign": "System Design",
        "pm": "Product Manager",
    }
    
    # Reverse mapping for lookup
    ROLE_ID_MAPPING = {v.lower(): k for k, v in ROLE_MAPPING.items()}
    
    def __init__(self):
        """Initialize the repository by loading and normalizing questions."""
        self._questions: List[InterviewQuestion] = []
        self._roles: List[Dict[str, Any]] = ROLES_DATA
        self._companies: List[Dict[str, Any]] = COMPANIES_DATA
        self._load_questions()
        self._add_fallback_questions()
    
    def _load_questions(self) -> None:
        """Load and normalize questions from seed data."""
        for idx, q_data in enumerate(INTERVIEW_QUESTIONS_DATA):
            try:
                # Generate unique ID
                q_id = hashlib.md5(
                    f"{q_data.get('question_text', '')}_{idx}".encode()
                ).hexdigest()[:12]
                
                # Determine question type
                category = q_data.get("category", "Technical").lower()
                if category == "system design":
                    q_type = "system_design"
                elif category == "behavioral" or category == "hr":
                    q_type = "behavioral"
                elif "coding" in q_data.get("topics", "").lower():
                    q_type = "coding"
                else:
                    q_type = "technical"
                
                # Map difficulty
                difficulty_map = {"Easy": "easy", "Medium": "medium", "Hard": "hard"}
                difficulty = difficulty_map.get(q_data.get("difficulty", "Medium"), "medium")
                
                # Get role name
                role_id = q_data.get("role_id", "sde")
                role_name = self.ROLE_MAPPING.get(role_id, "Software Engineer")
                
                # Parse ideal answer points from guidelines
                guidelines = q_data.get("answer_guidelines", "")
                ideal_points = [p.strip() for p in guidelines.split(".") if p.strip()][:5]
                
                # Create coding data if applicable
                coding_data = None
                if q_type == "coding":
                    coding_data = CodingProblem(
                        problem_statement=q_data.get("question_text", ""),
                        expected_approach=guidelines,
                        code_solution=None,
                    )
                
                question = InterviewQuestion(
                    question_id=q_id,
                    question_text=q_data.get("question_text", ""),
                    question_type=q_type,
                    role=role_name,
                    difficulty=difficulty,
                    topic=q_data.get("topics", "General").split(",")[0].strip(),
                    ideal_answer_points=ideal_points if ideal_points else ["Provide clear explanation"],
                    coding_data=coding_data,
                    company=q_data.get("company_id"),
                    frequency_score=q_data.get("frequency_score", 5),
                    answer_guidelines=guidelines,
                )
                self._questions.append(question)
            except Exception as e:
                # Skip malformed questions
                continue
    
    def _add_fallback_questions(self) -> None:
        """Add generic fallback questions for all roles."""
        fallback_questions = [
            {
                "text": "Tell me about yourself and your experience.",
                "type": "behavioral",
                "topic": "Introduction",
                "difficulty": "easy",
                "points": ["Background summary", "Relevant experience", "Career goals"],
            },
            {
                "text": "Describe a challenging technical problem you solved recently.",
                "type": "technical",
                "topic": "Problem Solving",
                "difficulty": "medium",
                "points": ["Problem context", "Approach taken", "Solution implemented", "Outcome"],
            },
            {
                "text": "How do you approach learning new technologies?",
                "type": "behavioral",
                "topic": "Learning",
                "difficulty": "easy",
                "points": ["Learning strategy", "Resources used", "Practical application"],
            },
            {
                "text": "Explain a concept from your domain to someone non-technical.",
                "type": "technical",
                "topic": "Communication",
                "difficulty": "medium",
                "points": ["Clear explanation", "Use of analogies", "Audience awareness"],
            },
            {
                "text": "What are your strengths and areas for improvement?",
                "type": "behavioral",
                "topic": "Self-awareness",
                "difficulty": "easy",
                "points": ["Honest self-assessment", "Growth mindset", "Concrete examples"],
            },
            {
                "text": "Describe how you handle tight deadlines and pressure.",
                "type": "behavioral",
                "topic": "Time Management",
                "difficulty": "medium",
                "points": ["Prioritization", "Stress management", "Communication"],
            },
            {
                "text": "Walk me through your approach to debugging a complex issue.",
                "type": "technical",
                "topic": "Debugging",
                "difficulty": "medium",
                "points": ["Systematic approach", "Tools used", "Root cause analysis"],
            },
            {
                "text": "How do you ensure code quality in your projects?",
                "type": "technical",
                "topic": "Code Quality",
                "difficulty": "medium",
                "points": ["Testing practices", "Code reviews", "Documentation"],
            },
        ]
        
        for role_name in self.ROLE_MAPPING.values():
            for idx, fb in enumerate(fallback_questions):
                q_id = hashlib.md5(f"fallback_{role_name}_{idx}".encode()).hexdigest()[:12]
                question = InterviewQuestion(
                    question_id=q_id,
                    question_text=fb["text"],
                    question_type=fb["type"],
                    role=role_name,
                    difficulty=fb["difficulty"],
                    topic=fb["topic"],
                    ideal_answer_points=fb["points"],
                    frequency_score=7,
                )
                self._questions.append(question)
    
    def get_questions(
        self,
        filter_criteria: Optional[QuestionFilter] = None,
        limit: Optional[int] = None,
        randomize: bool = True,
    ) -> List[InterviewQuestion]:
        """
        Get questions matching the filter criteria.
        
        Args:
            filter_criteria: Optional filter to apply
            limit: Maximum number of questions to return
            randomize: Whether to randomize the order
            
        Returns:
            List of matching questions
        """
        questions = self._questions.copy()
        
        if filter_criteria:
            # Filter by role
            if filter_criteria.role:
                role_lower = filter_criteria.role.lower()
                questions = [
                    q for q in questions 
                    if q.role.lower() == role_lower or role_lower in q.role.lower()
                ]
            
            # Filter by company
            if filter_criteria.company:
                company_lower = filter_criteria.company.lower()
                questions = [
                    q for q in questions 
                    if q.company and company_lower in q.company.lower()
                ]
            
            # Filter by difficulty
            if filter_criteria.difficulty:
                questions = [
                    q for q in questions 
                    if q.difficulty == filter_criteria.difficulty
                ]
            
            # Filter by question type
            if filter_criteria.question_type:
                questions = [
                    q for q in questions 
                    if q.question_type == filter_criteria.question_type
                ]
            
            # Filter by topic
            if filter_criteria.topic:
                topic_lower = filter_criteria.topic.lower()
                questions = [
                    q for q in questions 
                    if topic_lower in q.topic.lower()
                ]
            
            # Exclude specific questions
            if filter_criteria.exclude_questions:
                questions = [
                    q for q in questions 
                    if q.question_id not in filter_criteria.exclude_questions
                ]
        
        if randomize:
            random.shuffle(questions)
        
        if limit:
            questions = questions[:limit]
        
        return questions
    
    def get_question_by_id(self, question_id: str) -> Optional[InterviewQuestion]:
        """Get a specific question by ID."""
        for q in self._questions:
            if q.question_id == question_id:
                return q
        return None
    
    def get_available_roles(self) -> List[str]:
        """Get list of available roles."""
        return list(self.ROLE_MAPPING.values())
    
    def get_available_companies(self) -> List[str]:
        """Get list of available companies."""
        return [c["name"] for c in self._companies]
    
    def get_topics_for_role(self, role: str) -> List[str]:
        """Get available topics for a specific role."""
        questions = self.get_questions(
            QuestionFilter(role=role),
            randomize=False
        )
        topics = list(set(q.topic for q in questions))
        return sorted(topics)
    
    def select_next_question(
        self,
        role: str,
        difficulty: str,
        asked_questions: List[str],
        asked_topics: List[str],
        prefer_type: Optional[str] = None,
        resume_skills: Optional[List[str]] = None,
        resume_projects: Optional[List[str]] = None,
    ) -> Optional[InterviewQuestion]:
        """
        Intelligently select the next question avoiding repetition.
        
        Args:
            role: Target role
            difficulty: Desired difficulty level
            asked_questions: List of already asked question IDs
            asked_topics: List of already covered topics
            prefer_type: Preferred question type (optional)
            resume_skills: Skills from candidate's resume (optional)
            resume_projects: Projects from candidate's resume (optional)
            
        Returns:
            Selected question or None if no suitable question found
        """
        # Build filter
        filter_criteria = QuestionFilter(
            role=role,
            difficulty=difficulty,
            exclude_questions=asked_questions,
        )
        
        if prefer_type:
            filter_criteria.question_type = prefer_type
        
        candidates = self.get_questions(filter_criteria, randomize=True)
        
        # Prefer questions with topics not yet covered
        uncovered_topic_questions = [
            q for q in candidates 
            if q.topic.lower() not in [t.lower() for t in asked_topics]
        ]
        
        if uncovered_topic_questions:
            # Sort by frequency score (higher = more commonly asked)
            uncovered_topic_questions.sort(key=lambda x: x.frequency_score, reverse=True)
            return uncovered_topic_questions[0]
        
        # If all topics covered, return any candidate
        if candidates:
            return candidates[0]
        
        # Fallback: relax difficulty constraint
        filter_criteria.difficulty = None
        candidates = self.get_questions(filter_criteria, randomize=True)
        
        if candidates:
            return candidates[0]
        
        return None


# Singleton instance
_repository_instance: Optional[QuestionRepository] = None


def get_question_repository() -> QuestionRepository:
    """Get or create the singleton question repository instance."""
    global _repository_instance
    if _repository_instance is None:
        _repository_instance = QuestionRepository()
    return _repository_instance
