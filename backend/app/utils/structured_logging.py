"""
Enhanced Structured Logging - Enterprise-grade logging with correlation IDs and metrics.
Provides comprehensive observability for interview assessment system.
"""
import logging
import logging.handlers
import os
import json
import time
import uuid
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from contextvars import ContextVar
from functools import wraps


# Context variables for correlation tracking
correlation_id: ContextVar[str] = ContextVar('correlation_id', default='')
session_id: ContextVar[str] = ContextVar('session_id', default='')
user_id: ContextVar[str] = ContextVar('user_id', default='')


class CorrelationFilter(logging.Filter):
    """Add correlation context to log records."""
    
    def filter(self, record):
        record.correlation_id = correlation_id.get()
        record.session_id = session_id.get()
        record.user_id = user_id.get()
        return True


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for better parsing and analysis."""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, 'correlation_id', ''),
            "session_id": getattr(record, 'session_id', ''),
            "user_id": getattr(record, 'user_id', ''),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'metrics'):
            log_entry["metrics"] = record.metrics
        if hasattr(record, 'operation'):
            log_entry["operation"] = record.operation
        if hasattr(record, 'duration'):
            log_entry["duration_ms"] = record.duration
        
        return json.dumps(log_entry, ensure_ascii=False)


class DetailedFormatter(logging.Formatter):
    """Detailed human-readable formatter with context information."""
    
    def format(self, record):
        # Add correlation context to message
        context_parts = []
        if getattr(record, 'correlation_id', ''):
            context_parts.append(f"corr_id={record.correlation_id}")
        if getattr(record, 'session_id', ''):
            context_parts.append(f"session={record.session_id}")
        if getattr(record, 'user_id', ''):
            context_parts.append(f"user={record.user_id}")
        
        context_str = f"[{' '.join(context_parts)}] " if context_parts else ""
        
        # Format the main message
        message = super().format(record)
        
        # Add metrics if present
        if hasattr(record, 'metrics'):
            metrics_str = " | ".join([f"{k}={v}" for k, v in record.metrics.items()])
            message += f" | Metrics: {metrics_str}"
        
        # Add duration if present
        if hasattr(record, 'duration'):
            message += f" | Duration: {record.duration:.2f}ms"
        
        return f"{context_str}{message}"


def setup_logging():
    """Setup enhanced application logging configuration."""
    # Create logs directory if it doesn't exist
    LOG_DIR = Path("./logs")
    LOG_DIR.mkdir(exist_ok=True)
    
    # Get configuration
    from app.config import settings
    LOG_LEVEL = settings.LOG_LEVEL
    LOG_FILE = settings.LOG_FILE
    LOG_FORMAT = settings.LOG_FORMAT
    LOG_MAX_SIZE = settings.LOG_MAX_SIZE
    LOG_BACKUP_COUNT = settings.LOG_BACKUP_COUNT
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_SIZE,
        backupCount=LOG_BACKUP_COUNT
    )
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # Add correlation filter to both handlers
    correlation_filter = CorrelationFilter()
    file_handler.addFilter(correlation_filter)
    console_handler.addFilter(correlation_filter)
    
    # Set formatters based on configuration
    if LOG_FORMAT == "json":
        formatter = JSONFormatter()
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
    elif LOG_FORMAT == "detailed":
        formatter = DetailedFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
    else:  # simple format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
    
    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Log startup
    logger = logging.getLogger(__name__)
    logger.info(
        "Enhanced logging initialized",
        extra={
            "metrics": {
                "log_level": LOG_LEVEL,
                "log_format": LOG_FORMAT,
                "max_file_size": LOG_MAX_SIZE,
                "backup_count": LOG_BACKUP_COUNT
            }
        }
    )
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


def set_correlation_context(
    correlation_id_value: Optional[str] = None,
    session_id_value: Optional[str] = None,
    user_id_value: Optional[str] = None
):
    """Set correlation context for current execution context."""
    if correlation_id_value:
        correlation_id.set(correlation_id_value)
    if session_id_value:
        session_id.set(session_id_value)
    if user_id_value:
        user_id.set(user_id_value)


def generate_correlation_id() -> str:
    """Generate a new correlation ID."""
    return str(uuid.uuid4())


def log_with_context(
    logger: logging.Logger,
    level: str,
    message: str,
    metrics: Optional[Dict[str, Any]] = None,
    operation: Optional[str] = None,
    **kwargs
):
    """Log message with context and metrics."""
    extra = {}
    
    if metrics:
        extra["metrics"] = metrics
    if operation:
        extra["operation"] = operation
    
    extra.update(kwargs)
    
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message, extra=extra)


def log_interview_start(
    session_id: str,
    candidate_name: str,
    role: str,
    experience_level: str,
    company: Optional[str] = None
):
    """Log interview session start."""
    logger = get_logger("interview.session")
    
    set_correlation_context(
        correlation_id_value=generate_correlation_id(),
        session_id_value=session_id
    )
    
    log_with_context(
        logger,
        "INFO",
        f"Interview session started for {candidate_name}",
        operation="interview_start",
        metrics={
            "candidate_name": candidate_name,
            "role": role,
            "experience_level": experience_level,
            "company": company or "Not specified",
            "session_id": session_id
        }
    )


def log_interview_end(
    session_id: str,
    final_score: float,
    total_questions: int,
    duration_minutes: Optional[float] = None
):
    """Log interview session end."""
    logger = get_logger("interview.session")
    
    log_with_context(
        logger,
        "INFO",
        f"Interview session completed",
        operation="interview_end",
        metrics={
            "session_id": session_id,
            "final_score": round(final_score, 2),
            "total_questions": total_questions,
            "duration_minutes": round(duration_minutes, 1) if duration_minutes else None,
            "status": "completed"
        }
    )


def log_question_generated(
    session_id: str,
    question_id: str,
    category: str,
    difficulty: str,
    generation_time_ms: float
):
    """Log question generation event."""
    logger = get_logger("interview.question")
    
    log_with_context(
        logger,
        "INFO",
        f"Question generated: {question_id}",
        operation="question_generation",
        metrics={
            "session_id": session_id,
            "question_id": question_id,
            "category": category,
            "difficulty": difficulty,
            "generation_time_ms": round(generation_time_ms, 2)
        }
    )


def log_answer_evaluated(
    session_id: str,
    question_id: str,
    score: float,
    evaluation_time_ms: float,
    confidence_band: str
):
    """Log answer evaluation event."""
    logger = get_logger("interview.evaluation")
    
    log_with_context(
        logger,
        "INFO",
        f"Answer evaluated for question: {question_id}",
        operation="answer_evaluation",
        metrics={
            "session_id": session_id,
            "question_id": question_id,
            "score": round(score, 2),
            "confidence_band": confidence_band,
            "evaluation_time_ms": round(evaluation_time_ms, 2)
        }
    )


def log_topic_coverage(
    session_id: str,
    coverage_percentage: float,
    categories_covered: int,
    total_categories: int
):
    """Log topic coverage metrics."""
    logger = get_logger("interview.coverage")
    
    log_with_context(
        logger,
        "INFO",
        f"Topic coverage updated",
        operation="topic_coverage",
        metrics={
            "session_id": session_id,
            "coverage_percentage": round(coverage_percentage, 1),
            "categories_covered": categories_covered,
            "total_categories": total_categories,
            "coverage_ratio": f"{categories_covered}/{total_categories}"
        }
    )


def log_difficulty_adjustment(
    session_id: str,
    old_difficulty: str,
    new_difficulty: str,
    reason: str,
    confidence: float
):
    """Log difficulty adjustment event."""
    logger = get_logger("interview.difficulty")
    
    log_with_context(
        logger,
        "INFO",
        f"Difficulty adjusted: {old_difficulty} → {new_difficulty}",
        operation="difficulty_adjustment",
        metrics={
            "session_id": session_id,
            "old_difficulty": old_difficulty,
            "new_difficulty": new_difficulty,
            "reason": reason,
            "confidence": round(confidence, 2)
        }
    )


def log_skill_gap_identified(
    session_id: str,
    category: str,
    severity: str,
    gap_size: float,
    current_level: float
):
    """Log identified skill gap."""
    logger = get_logger("interview.analysis")
    
    log_with_context(
        logger,
        "INFO" if severity == "Low" else "WARNING" if severity == "Medium" else "ERROR",
        f"Skill gap identified in {category}",
        operation="skill_gap_analysis",
        metrics={
            "session_id": session_id,
            "category": category,
            "severity": severity,
            "gap_size": round(gap_size, 2),
            "current_level": round(current_level, 2)
        }
    )


def log_question_selected(session_id: str, question_topic: str, difficulty: str):
    """Log question selection."""
    agent_logger = get_logger("agents")
    log_with_context(
        agent_logger,
        "DEBUG",
        f"Question selected",
        operation="question_selection",
        metrics={
            "session_id": session_id,
            "question_topic": question_topic,
            "difficulty": difficulty
        }
    )





def log_llm_call(prompt_length: int, response_length: int, duration_ms: float):
    """Log LLM API call."""
    llm_logger = get_logger("llm")
    log_with_context(
        llm_logger,
        "DEBUG",
        f"LLM call completed",
        operation="llm_call",
        metrics={
            "prompt_length": prompt_length,
            "response_length": response_length,
            "duration_ms": round(duration_ms, 2)
        }
    )


def log_error(error: Exception, context: str = ""):
    """Log an error with context."""
    logger = get_logger(__name__)
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_system_health(
    status: str,
    error_rate: float,
    active_sessions: int,
    memory_usage_mb: Optional[float] = None
):
    """Log system health metrics."""
    logger = get_logger("system.health")
    
    log_with_context(
        logger,
        "INFO" if status == "healthy" else "WARNING" if status == "degraded" else "ERROR",
        f"System health status: {status}",
        operation="system_health_check",
        metrics={
            "status": status,
            "error_rate": round(error_rate, 2),
            "active_sessions": active_sessions,
            "memory_usage_mb": round(memory_usage_mb, 2) if memory_usage_mb else None
        }
    )