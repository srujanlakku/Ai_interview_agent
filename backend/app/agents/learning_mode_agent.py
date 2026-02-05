"""
Post-Interview Learning Mode - Enables interactive learning after interview completion.

Features:
- Review weak answers with detailed explanations
- Interactive practice on identified skill gaps
- Follow-up questions for clarification
- Personalized learning recommendations
- Context-aware tutoring based on interview performance
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class LearningMode(Enum):
    """Types of learning activities available."""
    EXPLANATION = "explanation"        # Detailed explanation of concepts
    PRACTICE = "practice"              # Interactive practice problems
    CLARIFICATION = "clarification"    # Follow-up questions for understanding
    REVIEW = "review"                  # Review interview questions and answers


class SkillLevel(Enum):
    """Candidate's demonstrated skill level."""
    NOVICE = "novice"          # Fundamental gaps
    BEGINNER = "beginner"      # Basic understanding with gaps
    INTERMEDIATE = "intermediate"  # Solid foundation with room for growth
    ADVANCED = "advanced"      # Strong knowledge, minor refinements needed


@dataclass
class LearningRequest:
    """Request for learning assistance."""
    mode: LearningMode
    topic: str
    question_id: Optional[str] = None
    original_answer: Optional[str] = None
    evaluation: Optional[Dict[str, Any]] = None
    user_query: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "mode": self.mode.value,
            "topic": self.topic,
            "question_id": self.question_id,
            "original_answer": self.original_answer,
            "user_query": self.user_query
        }


@dataclass
class LearningResponse:
    """Response from learning mode."""
    mode: LearningMode
    content: str
    skill_level: SkillLevel
    next_steps: List[str]
    resources: List[str]
    estimated_time: int  # Minutes
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "mode": self.mode.value,
            "content": self.content,
            "skill_level": self.skill_level.value,
            "next_steps": self.next_steps,
            "resources": self.resources,
            "estimated_time": self.estimated_time
        }


class LearningModeAgent(BaseAgent):
    """
    Agent that provides post-interview learning experiences.
    
    Features:
    - Context-aware explanations based on interview performance
    - Interactive practice tailored to identified weaknesses
    - Follow-up Q&A for clarification
    - Personalized learning pathways
    - Resource recommendations
    """
    
    def __init__(self):
        super().__init__("LearningModeAgent")
        self.session_context: Dict[str, Any] = {}
        self.learning_history: List[LearningResponse] = []
    
    def initialize_session(self, interview_data: Dict[str, Any]) -> None:
        """
        Initialize learning mode with interview context.
        
        Args:
            interview_data: Complete interview session data including:
                - questions and answers
                - evaluations and scores
                - identified skill gaps
                - candidate profile
        """
        self.session_context = {
            "candidate_name": interview_data.get("candidate_name", "Candidate"),
            "role": interview_data.get("role", "Software Engineer"),
            "experience_level": interview_data.get("experience_level", "mid"),
            "interview_date": interview_data.get("interview_date"),
            "questions": interview_data.get("questions", []),
            "evaluations": interview_data.get("evaluations", []),
            "skill_gaps": interview_data.get("skill_gaps", []),
            "average_score": interview_data.get("average_score", 5.0),
            "strengths": interview_data.get("strengths", []),
            "weaknesses": interview_data.get("weaknesses", [])
        }
        
        logger.info(f"Learning mode initialized for {self.session_context['candidate_name']}")
    
    async def process_learning_request(self, request: LearningRequest) -> LearningResponse:
        """
        Process a learning request and generate appropriate response.
        
        Args:
            request: LearningRequest with mode, topic, and context
            
        Returns:
            LearningResponse with content and recommendations
        """
        try:
            # Build appropriate prompt based on learning mode
            prompt = self._build_learning_prompt(request)
            
            # Get response from LLM
            response = await self.call_llm(
                prompt,
                system_message=(
                    "You are an expert technical mentor and educator. Your role is to help "
                    "candidates understand concepts they struggled with during their interview. "
                    "Provide clear, actionable guidance that builds confidence and competence. "
                    "Be encouraging and focus on growth mindset."
                ),
                temperature=0.5,
                max_tokens=800
            )
            
            # Parse and structure response
            learning_data = self._parse_learning_response(response, request.mode)
            
            # Create response object
            result = LearningResponse(
                mode=request.mode,
                content=learning_data["content"],
                skill_level=SkillLevel(learning_data["skill_level"]),
                next_steps=learning_data["next_steps"],
                resources=learning_data["resources"],
                estimated_time=learning_data["estimated_time"]
            )
            
            # Store in history
            self.learning_history.append(result)
            
            logger.info(f"Learning response generated | Mode: {request.mode.value} | Topic: {request.topic}")
            
            return result
            
        except Exception as e:
            logger.error(f"LearningModeAgent failed: {str(e)}")
            return self._fallback_learning_response(request)
    
    def _build_learning_prompt(self, request: LearningRequest) -> str:
        """Build appropriate prompt based on learning mode."""
        candidate_info = (
            f"Candidate: {self.session_context.get('candidate_name', 'Anonymous')}\n"
            f"Role: {self.session_context.get('role', 'Software Engineer')}\n"
            f"Experience: {self.session_context.get('experience_level', 'mid-level')}\n"
        )
        
        if request.mode == LearningMode.EXPLANATION:
            return self._build_explanation_prompt(request, candidate_info)
        elif request.mode == LearningMode.PRACTICE:
            return self._build_practice_prompt(request, candidate_info)
        elif request.mode == LearningMode.CLARIFICATION:
            return self._build_clarification_prompt(request, candidate_info)
        elif request.mode == LearningMode.REVIEW:
            return self._build_review_prompt(request, candidate_info)
        else:
            raise ValueError(f"Unknown learning mode: {request.mode}")
    
    def _build_explanation_prompt(self, request: LearningRequest, candidate_info: str) -> str:
        """Build prompt for detailed explanations."""
        # Find relevant evaluation data
        relevant_eval = None
        if request.question_id:
            for eval_data in self.session_context.get("evaluations", []):
                if eval_data.get("question_id") == request.question_id:
                    relevant_eval = eval_data
                    break
        
        weaknesses = relevant_eval.get("weaknesses", []) if relevant_eval else []
        score = relevant_eval.get("score", 5) if relevant_eval else 5
        
        return f"""
{candidate_info}

LEARNING REQUEST: Detailed Explanation
Topic: {request.topic}

Context:
- The candidate scored {score}/10 on this topic
- Identified weaknesses: {', '.join(weaknesses) if weaknesses else 'None specified'}
- Original answer: "{request.original_answer or 'Not provided'}"

Please provide:
1. Clear, step-by-step explanation of the concept
2. Common misconceptions and how to avoid them
3. Practical examples and analogies
4. Skill level assessment (novice/beginner/intermediate/advanced)
5. Specific next steps for mastery
6. Recommended learning resources
7. Estimated time investment (in minutes)

Focus on building understanding from the candidate's current level.
"""

    def _build_practice_prompt(self, request: LearningRequest, candidate_info: str) -> str:
        """Build prompt for interactive practice."""
        avg_score = self.session_context.get("average_score", 5.0)
        skill_level = self._determine_skill_level(avg_score)
        
        return f"""
{candidate_info}

LEARNING REQUEST: Interactive Practice
Topic: {request.topic}
Candidate Skill Level: {skill_level.value}

Create an interactive learning experience:
1. Progressive practice problems (easy to challenging)
2. Immediate feedback mechanism
3. Hints and scaffolding for difficult concepts
4. Real-world application examples
5. Common pitfalls to watch for
6. Skill-building exercises

Format as interactive tutorial with clear instructions.
"""

    def _build_clarification_prompt(self, request: LearningRequest, candidate_info: str) -> str:
        """Build prompt for follow-up questions."""
        return f"""
{candidate_info}

LEARNING REQUEST: Clarification
Topic: {request.topic}
User Question: "{request.user_query}"

Provide a clear, direct answer to the candidate's specific question.
Include:
1. Direct answer to the question
2. Supporting context and examples
3. Related concepts that might help understanding
4. Pointers to additional resources if needed

Be concise but thorough.
"""

    def _build_review_prompt(self, request: LearningRequest, candidate_info: str) -> str:
        """Build prompt for interview review."""
        # Get all questions on this topic
        topic_questions = [
            q for q in self.session_context.get("questions", [])
            if q.get("topic", "").lower() == request.topic.lower()
        ]
        
        return f"""
{candidate_info}

LEARNING REQUEST: Interview Review
Topic: {request.topic}
Questions covered: {len(topic_questions)}

Provide comprehensive review of:
1. Key concepts tested in the interview
2. Candidate's performance analysis
3. Strengths demonstrated
4. Areas needing improvement
5. Industry best practices related to these concepts
6. Preparation tips for real interviews

Structure as detailed review session.
"""

    def _parse_learning_response(self, response: str, mode: LearningMode) -> Dict[str, Any]:
        """Parse LLM response into structured learning data."""
        try:
            # Look for JSON structure in response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                # Validate required fields
                required_fields = ["content", "skill_level", "next_steps", "resources", "estimated_time"]
                if all(field in data for field in required_fields):
                    return data
        except Exception as e:
            logger.warning(f"Failed to parse learning response: {str(e)}")
        
        # Fallback parsing - extract content and create structure
        content = response.strip()
        skill_level = self._infer_skill_level_from_content(content, mode)
        
        return {
            "content": content,
            "skill_level": skill_level.value,
            "next_steps": self._generate_next_steps(skill_level, mode),
            "resources": self._generate_resources(mode),
            "estimated_time": self._estimate_time(mode, skill_level)
        }
    
    def _infer_skill_level_from_content(self, content: str, mode: LearningMode) -> SkillLevel:
        """Infer skill level from response content."""
        content_lower = content.lower()
        
        if "fundamental" in content_lower or "basic" in content_lower:
            return SkillLevel.NOVICE
        elif "intermediate" in content_lower or "solid foundation" in content_lower:
            return SkillLevel.INTERMEDIATE
        elif "advanced" in content_lower or "expert" in content_lower:
            return SkillLevel.ADVANCED
        else:
            return SkillLevel.BEGINNER
    
    def _generate_next_steps(self, skill_level: SkillLevel, mode: LearningMode) -> List[str]:
        """Generate appropriate next steps based on skill level and mode."""
        base_steps = []
        
        if skill_level == SkillLevel.NOVICE:
            base_steps = [
                "Master fundamental concepts first",
                "Practice basic problems extensively",
                "Seek mentorship or tutoring"
            ]
        elif skill_level == SkillLevel.BEGINNER:
            base_steps = [
                "Review core concepts regularly",
                "Practice coding problems daily",
                "Join study groups or communities"
            ]
        elif skill_level == SkillLevel.INTERMEDIATE:
            base_steps = [
                "Focus on system design principles",
                "Practice real interview scenarios",
                "Contribute to open source projects"
            ]
        else:  # ADVANCED
            base_steps = [
                "Refine communication skills",
                "Practice leadership scenarios",
                "Stay current with industry trends"
            ]
        
        # Add mode-specific steps
        if mode == LearningMode.PRACTICE:
            base_steps.append("Complete additional practice problems")
        elif mode == LearningMode.EXPLANATION:
            base_steps.append("Review explanation multiple times")
        
        return base_steps[:3]  # Limit to 3 steps
    
    def _generate_resources(self, mode: LearningMode) -> List[str]:
        """Generate learning resources."""
        if mode == LearningMode.PRACTICE:
            return [
                "LeetCode - Coding practice platform",
                "HackerRank - Technical skills assessment",
                "Pramp - Mock interview practice"
            ]
        elif mode == LearningMode.EXPLANATION:
            return [
                "GeeksforGeeks - Concept explanations",
                "Educative.io - Interactive courses",
                "YouTube technical channels"
            ]
        else:
            return [
                "Cracking the Coding Interview book",
                "System Design Primer",
                "Tech interview handbooks"
            ]
    
    def _estimate_time(self, mode: LearningMode, skill_level: SkillLevel) -> int:
        """Estimate time needed for learning activity."""
        base_time = 0
        
        if mode == LearningMode.EXPLANATION:
            base_time = 30
        elif mode == LearningMode.PRACTICE:
            base_time = 45
        elif mode == LearningMode.CLARIFICATION:
            base_time = 15
        else:  # REVIEW
            base_time = 60
        
        # Adjust based on skill level
        if skill_level == SkillLevel.NOVICE:
            return base_time * 2
        elif skill_level == SkillLevel.ADVANCED:
            return max(15, base_time // 2)
        else:
            return base_time
    
    def _determine_skill_level(self, score: float) -> SkillLevel:
        """Determine skill level from interview score."""
        if score >= 8.0:
            return SkillLevel.ADVANCED
        elif score >= 6.0:
            return SkillLevel.INTERMEDIATE
        elif score >= 4.0:
            return SkillLevel.BEGINNER
        else:
            return SkillLevel.NOVICE
    
    def _fallback_learning_response(self, request: LearningRequest) -> LearningResponse:
        """Fallback response when LLM fails."""
        content = f"I'd be happy to help you with {request.topic}. "
        
        if request.mode == LearningMode.EXPLANATION:
            content += "Let me explain the key concepts step by step."
        elif request.mode == LearningMode.PRACTICE:
            content += "Here are some practice problems to reinforce your learning."
        elif request.mode == LearningMode.CLARIFICATION:
            content += "I'll address your specific question directly."
        else:
            content += "Let's review your interview performance on this topic."
        
        return LearningResponse(
            mode=request.mode,
            content=content,
            skill_level=SkillLevel.BEGINNER,
            next_steps=["Review fundamental concepts", "Practice regularly"],
            resources=["Online tutorials", "Practice platforms"],
            estimated_time=30
        )
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning activities."""
        if not self.learning_history:
            return {"message": "No learning activities recorded"}
        
        mode_counts = {}
        total_time = 0
        
        for activity in self.learning_history:
            mode = activity.mode.value
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
            total_time += activity.estimated_time
        
        return {
            "total_activities": len(self.learning_history),
            "total_estimated_time": total_time,
            "activities_by_mode": mode_counts,
            "recent_activities": [
                activity.to_dict() for activity in self.learning_history[-3:]
            ]
        }
    
    def reset(self) -> None:
        """Reset learning mode for new session."""
        self.session_context.clear()
        self.learning_history.clear()
        logger.info("LearningModeAgent reset for new session")