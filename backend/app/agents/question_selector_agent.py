"""
Question Selector Agent - Selects next question based on role, company, and stage.
"""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.utils.logging_config import get_logger
import json

logger = get_logger(__name__)

class QuestionSelectorAgent(BaseAgent):
    """Agent responsible for selecting the next interview question"""

    def __init__(self):
        super().__init__("QuestionSelectorAgent")

    async def execute(self, 
                      role: str, 
                      company: str, 
                      interview_stage: str, 
                      previous_questions: List[Dict[str, Any]],
                      difficulty_level: str) -> Dict[str, Any]:
        """
        Selects the next question for the interview.
        """
        try:
            # Build context from previous questions to avoid repetition
            past_topics = [q.get("topic", "General") for q in previous_questions]
            past_questions = [q.get("question_text", "") for q in previous_questions]
            
            prompt = f"""
            As a QuestionSelectorAgent, your task is to select the next interview question.
            
            Target Role: {role}
            Target Company: {company}
            Interview Stage: {interview_stage}
            Current Difficulty: {difficulty_level}
            
            Previously Asked Topics: {', '.join(set(past_topics))}
            Previously Asked Questions: {json.dumps(past_questions)}
            
            Requirements:
            1. Dynamically mix question types: 'soft_skill', 'technical', or 'coding'.
            2. For 'coding' questions, provide structured problem data.
            3. Ensure the question is relevant to the stage ({interview_stage}).
            4. Do NOT repeat previous topics or questions.
            
            Return the output in JSON format:
            {{
                "question_text": "The question or problem statement",
                "question_type": "soft_skill | technical | coding",
                "topic": "The specific topic (e.g., React, System Design, Behavioral)",
                "difficulty": "{difficulty_level}",
                "coding_data": {{  // Only for coding questions
                    "problem_statement": "Detailed problem",
                    "expected_approach": "Optimal approach",
                    "code_solution": "Sample solution code",
                    "difficulty_level": "{difficulty_level}"
                }},
                "ideal_answer_points": ["point 1", "point 2"] // Key points expected in answer
            }}
            """

            response = await self.call_llm(
                prompt,
                system_message="You are a senior recruiter and technical architect. You select high-quality, role-specific interview questions.",
                temperature=0.8,
                max_tokens=1000
            )

            result = self._extract_json(response)
            return result

        except Exception as e:
            logger.error(f"QuestionSelectorAgent failed: {str(e)}")
            return {
                "question_text": "Tell me about a challenging technical problem you solved recently.",
                "question_type": "technical",
                "topic": "General Technical",
                "difficulty": difficulty_level,
                "ideal_answer_points": ["Problem context", "Implementation details", "Outcome/Impact"]
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
