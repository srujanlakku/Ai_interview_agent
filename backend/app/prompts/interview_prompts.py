"""
Centralized prompts for the AI Interview Agent.
Contains all system prompts and prompt templates for consistent behavior.
"""
from typing import Dict, Optional


# ============================================================================
# SYSTEM PROMPTS
# ============================================================================

INTERVIEWER_SYSTEM_PROMPT = """You are a professional technical interviewer conducting a mock interview.

RULES:
1. Ask exactly ONE question at a time
2. NEVER answer your own questions
3. Maintain a professional but friendly tone
4. Adapt your language complexity to the candidate's experience level
5. Stay in character as an interviewer at all times

Your goal is to assess the candidate's technical knowledge, problem-solving ability, and communication skills."""


QUESTION_SELECTOR_PROMPT = """You are a senior technical recruiter selecting interview questions.

Your task is to select appropriate questions that:
1. Match the candidate's target role and experience level
2. Progressively increase in difficulty based on performance
3. Cover diverse topics without repetition
4. Test both theoretical knowledge and practical application

Select questions that would realistically be asked in actual technical interviews."""


EVALUATOR_SYSTEM_PROMPT = """You are an expert interview evaluator providing constructive feedback.

When evaluating answers:
1. Be fair and objective in your assessment
2. Consider the candidate's experience level
3. Identify specific strengths and areas for improvement
4. Provide actionable feedback
5. Score based on technical accuracy, depth of understanding, and communication clarity

Your evaluation should help candidates improve their interview performance."""


SUMMARY_PROMPT = """You are a career mentor providing a comprehensive interview assessment.

Your summary should:
1. Highlight key strengths demonstrated during the interview
2. Identify specific areas needing improvement
3. Provide an overall readiness assessment
4. Offer actionable next steps for the candidate
5. Be encouraging while being honest about areas to work on

Remember: Your goal is to help the candidate succeed in their job search."""


# ============================================================================
# ROLE-SPECIFIC CONTEXT
# ============================================================================

ROLE_CONTEXTS: Dict[str, str] = {
    "Software Engineer": """
Focus areas: Data structures, algorithms, system design basics, coding practices, debugging skills.
Key competencies: Problem-solving, code quality, technical communication, collaboration.
Common topics: Arrays, strings, trees, graphs, databases, APIs, testing.""",

    "Backend Developer": """
Focus areas: Server-side programming, databases, APIs, scalability, security.
Key competencies: System design, database optimization, API design, performance tuning.
Common topics: REST/GraphQL, SQL/NoSQL, caching, microservices, authentication.""",

    "Frontend Developer": """
Focus areas: UI/UX implementation, JavaScript frameworks, performance, accessibility.
Key competencies: Component design, state management, responsive design, browser APIs.
Common topics: React/Vue/Angular, CSS, DOM manipulation, testing, build tools.""",

    "Full Stack Developer": """
Focus areas: End-to-end development, frontend-backend integration, deployment.
Key competencies: Versatility, system architecture, full application lifecycle.
Common topics: Frontend frameworks, backend services, databases, DevOps basics.""",

    "Data Engineer": """
Focus areas: Data pipelines, ETL processes, data warehousing, big data tools.
Key competencies: SQL expertise, pipeline design, data modeling, optimization.
Common topics: Spark, Airflow, data lakes, streaming, data quality.""",

    "Data Scientist": """
Focus areas: Machine learning, statistics, data analysis, model deployment.
Key competencies: Statistical analysis, ML algorithms, data visualization, experimentation.
Common topics: Regression, classification, clustering, feature engineering, A/B testing.""",

    "AI/ML Engineer": """
Focus areas: ML systems, deep learning, model optimization, MLOps.
Key competencies: Algorithm implementation, model training, deployment pipelines.
Common topics: Neural networks, NLP, computer vision, model serving, monitoring.""",

    "DevOps Engineer": """
Focus areas: CI/CD, infrastructure as code, containerization, monitoring.
Key competencies: Automation, reliability engineering, cloud platforms, security.
Common topics: Docker, Kubernetes, Terraform, Jenkins, AWS/GCP/Azure.""",

    "QA/Automation Engineer": """
Focus areas: Test automation, quality processes, testing strategies.
Key competencies: Test design, automation frameworks, bug analysis, coverage.
Common topics: Selenium, pytest, API testing, performance testing, CI integration.""",

    "Product Manager": """
Focus areas: Product strategy, user research, roadmap planning, stakeholder management.
Key competencies: Prioritization, communication, data-driven decisions, user empathy.
Common topics: Product lifecycle, metrics, A/B testing, agile methodology.""",
}


EXPERIENCE_LEVEL_MODIFIERS: Dict[str, str] = {
    "fresher": """
Adjust for entry-level candidates:
- Focus on fundamentals and theoretical knowledge
- Ask about projects and academic experience
- Evaluate learning ability and potential
- Be patient with nervousness
- Look for enthusiasm and willingness to learn""",

    "mid": """
Adjust for mid-level candidates (2-5 years):
- Balance theory with practical experience
- Ask about real-world problem solving
- Evaluate independence and ownership
- Expect knowledge of best practices
- Look for growth trajectory and leadership potential""",

    "senior": """
Adjust for senior candidates (5+ years):
- Focus on architecture and system design
- Ask about leadership and mentoring experience
- Evaluate strategic thinking and decision making
- Expect deep expertise in core areas
- Look for ability to handle ambiguity and complexity""",
}


DIFFICULTY_MODIFIERS: Dict[str, str] = {
    "easy": """
Easy difficulty guidelines:
- Straightforward questions with clear answers
- Focus on fundamentals and basics
- One-step problem solving
- Clear requirements with little ambiguity""",

    "medium": """
Medium difficulty guidelines:
- Questions requiring analysis and reasoning
- Multiple concepts or steps involved
- Some trade-offs to consider
- Real-world scenarios with practical constraints""",

    "hard": """
Hard difficulty guidelines:
- Complex problems with multiple valid approaches
- System design and architecture considerations
- Edge cases and optimization requirements
- Ambiguous requirements needing clarification""",
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_role_context(role: str) -> str:
    """
    Get the context description for a specific role.
    
    Args:
        role: The target role name
        
    Returns:
        Role-specific context string
    """
    # Try exact match first
    if role in ROLE_CONTEXTS:
        return ROLE_CONTEXTS[role]
    
    # Try partial match
    role_lower = role.lower()
    for key, context in ROLE_CONTEXTS.items():
        if key.lower() in role_lower or role_lower in key.lower():
            return context
    
    # Default to Software Engineer context
    return ROLE_CONTEXTS["Software Engineer"]


def get_experience_modifier(level: str) -> str:
    """
    Get experience level modifier for prompts.
    
    Args:
        level: Experience level (fresher, mid, senior)
        
    Returns:
        Experience-specific modifier string
    """
    return EXPERIENCE_LEVEL_MODIFIERS.get(level.lower(), EXPERIENCE_LEVEL_MODIFIERS["mid"])


def get_difficulty_modifier(difficulty: str) -> str:
    """
    Get difficulty level modifier for prompts.
    
    Args:
        difficulty: Difficulty level (easy, medium, hard)
        
    Returns:
        Difficulty-specific modifier string
    """
    return DIFFICULTY_MODIFIERS.get(difficulty.lower(), DIFFICULTY_MODIFIERS["medium"])


def build_evaluation_prompt(
    question: str,
    answer: str,
    question_type: str,
    experience_level: str,
    ideal_points: Optional[list] = None,
) -> str:
    """
    Build a complete evaluation prompt.
    
    Args:
        question: The interview question
        answer: The candidate's answer
        question_type: Type of question
        experience_level: Candidate's experience level
        ideal_points: Expected key points in answer
        
    Returns:
        Complete evaluation prompt
    """
    points_str = ""
    if ideal_points:
        points_str = f"\nExpected key points:\n- " + "\n- ".join(ideal_points)
    
    exp_modifier = get_experience_modifier(experience_level)
    
    return f"""
Evaluate this {question_type} interview answer.

{exp_modifier}

Question: {question}

Candidate's Answer: {answer}
{points_str}

Provide evaluation in JSON format:
{{
    "score": <0-10>,
    "technical_accuracy": <0-10>,
    "depth_of_understanding": <0-10>,
    "communication_clarity": <0-10>,
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "feedback": "Constructive feedback",
    "improvement_suggestions": ["suggestion1", "suggestion2"]
}}
"""


def build_summary_prompt(
    role: str,
    experience_level: str,
    total_questions: int,
    average_score: float,
    category_scores: dict,
    strengths: list,
    weaknesses: list,
) -> str:
    """
    Build the final summary prompt.
    
    Args:
        role: Target role
        experience_level: Candidate's experience level
        total_questions: Number of questions asked
        average_score: Overall average score
        category_scores: Scores by category
        strengths: List of identified strengths
        weaknesses: List of identified weaknesses
        
    Returns:
        Complete summary prompt
    """
    return f"""
Generate a comprehensive interview assessment summary.

Interview Details:
- Role: {role}
- Experience Level: {experience_level}
- Questions Asked: {total_questions}
- Average Score: {average_score:.1f}/10

Category Scores:
- Technical: {category_scores.get('technical', 0):.1f}/10
- Behavioral: {category_scores.get('behavioral', 0):.1f}/10
- Coding: {category_scores.get('coding', 0):.1f}/10

Key Strengths: {', '.join(strengths[:5]) if strengths else 'None identified'}
Areas for Improvement: {', '.join(weaknesses[:5]) if weaknesses else 'None identified'}

Provide a comprehensive assessment in JSON format:
{{
    "overall_assessment": "2-3 paragraph narrative assessment",
    "readiness_level": "Not Ready | Almost Ready | Interview Ready",
    "top_strengths": ["strength1", "strength2", "strength3"],
    "priority_improvements": ["improvement1", "improvement2", "improvement3"],
    "recommended_focus_areas": ["area1", "area2"],
    "next_steps": ["actionable step 1", "actionable step 2", "actionable step 3"],
    "encouragement": "Brief encouraging message"
}}
"""
