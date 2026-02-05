"""
Centralized prompts for the AI Interview Agent.
"""
from app.prompts.interview_prompts import (
    INTERVIEWER_SYSTEM_PROMPT,
    QUESTION_SELECTOR_PROMPT,
    EVALUATOR_SYSTEM_PROMPT,
    SUMMARY_PROMPT,
    get_role_context,
    get_difficulty_modifier,
)

__all__ = [
    "INTERVIEWER_SYSTEM_PROMPT",
    "QUESTION_SELECTOR_PROMPT", 
    "EVALUATOR_SYSTEM_PROMPT",
    "SUMMARY_PROMPT",
    "get_role_context",
    "get_difficulty_modifier",
]
