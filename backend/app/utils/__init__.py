"""
Utility modules for the Interview Agent system.
"""
from app.utils.database import init_db, get_db
from app.utils.logging_config import setup_logging, get_logger
from app.utils.structured_logging import (
    set_correlation_context,
    generate_correlation_id,
    log_interview_start,
    log_interview_end,
    log_question_generated,
    log_answer_evaluated,
    log_topic_coverage,
    log_difficulty_adjustment,
    log_skill_gap_identified,
    log_question_selected,
    log_llm_call,
    log_error,
    log_system_health
)
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
    get_current_user
)
from app.utils.speech_recognition import SpeechRecognizer, transcribe_audio
from app.utils.exceptions import (
    InterviewPilotException,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    DuplicateError,
    LLMError,
    SpeechRecognitionError,
    ResearchError
)

__all__ = [
    # Database
    "init_db",
    "get_db",
    
    # Logging
    "setup_logging",
    "get_logger",
    "set_correlation_context",
    "generate_correlation_id",
    "log_interview_start",
    "log_interview_end",
    "log_question_generated",
    "log_answer_evaluated",
    "log_topic_coverage",
    "log_difficulty_adjustment",
    "log_skill_gap_identified",
    "log_question_selected",
    "log_llm_call",
    "log_error",
    "log_system_health",
    
    # Security
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_token",
    "get_current_user",
    
    # Speech Recognition
    "SpeechRecognizer",
    "transcribe_audio",
    
    # Exceptions
    "InterviewPilotException",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "NotFoundError",
    "DuplicateError",
    "LLMError",
    "SpeechRecognitionError",
    "ResearchError"
]
