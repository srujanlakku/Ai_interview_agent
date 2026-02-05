"""
Question schema definitions for the AI Interview Agent.
Provides validated data structures for interview questions.
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class CodingProblem(BaseModel):
    """Schema for coding problem details."""
    problem_statement: str = Field(..., description="Detailed problem statement")
    expected_approach: str = Field(..., description="Expected solution approach")
    code_solution: Optional[str] = Field(None, description="Sample solution code")
    test_cases: Optional[List[str]] = Field(default_factory=list, description="Test cases")
    time_complexity: Optional[str] = Field(None, description="Expected time complexity")
    space_complexity: Optional[str] = Field(None, description="Expected space complexity")


class InterviewQuestion(BaseModel):
    """Schema for an interview question."""
    question_id: Optional[str] = Field(None, description="Unique question identifier")
    question_text: str = Field(..., description="The question text")
    question_type: Literal["technical", "coding", "behavioral", "system_design"] = Field(
        ..., description="Type of question"
    )
    role: str = Field(..., description="Target role for this question")
    difficulty: Literal["easy", "medium", "hard"] = Field(
        "medium", description="Question difficulty level"
    )
    topic: str = Field(..., description="Question topic/category")
    ideal_answer_points: List[str] = Field(
        default_factory=list, description="Key points expected in answer"
    )
    coding_data: Optional[CodingProblem] = Field(
        None, description="Coding problem details if applicable"
    )
    company: Optional[str] = Field(None, description="Company this question is associated with")
    frequency_score: int = Field(5, ge=1, le=10, description="How frequently asked (1-10)")
    answer_guidelines: Optional[str] = Field(None, description="Guidelines for evaluating answer")


class QuestionFilter(BaseModel):
    """Filter criteria for selecting questions."""
    role: Optional[str] = None
    company: Optional[str] = None
    difficulty: Optional[Literal["easy", "medium", "hard"]] = None
    question_type: Optional[Literal["technical", "coding", "behavioral", "system_design"]] = None
    topic: Optional[str] = None
    exclude_questions: List[str] = Field(default_factory=list, description="Question IDs to exclude")


class QAPair(BaseModel):
    """Question-Answer pair with evaluation."""
    question: InterviewQuestion
    answer: str = Field(..., description="User's answer")
    score: Optional[float] = Field(None, ge=0, le=10, description="Score for this answer")
    feedback: Optional[str] = Field(None, description="Feedback for this answer")
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)


class InterviewConfig(BaseModel):
    """Configuration for an interview session."""
    role: str = Field(..., description="Target role")
    experience_level: Literal["fresher", "mid", "senior"] = Field(
        "mid", description="Experience level"
    )
    company: Optional[str] = Field(None, description="Target company")
    max_questions: int = Field(8, ge=3, le=15, description="Maximum number of questions")
    initial_difficulty: Literal["easy", "medium", "hard"] = Field(
        "medium", description="Starting difficulty"
    )
    include_coding: bool = Field(True, description="Include coding questions")
    include_system_design: bool = Field(True, description="Include system design questions")
