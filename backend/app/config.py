"""
Enhanced Configuration module for InterviewPilot
Enterprise-grade configuration with retry settings and observability features.
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Enhanced application settings with enterprise features."""
    
    # App
    APP_TITLE: str = "InterviewPilot"
    APP_VERSION: str = "2.0.0"  # Updated for enterprise features
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./interview_pilot.db")
    SQLITE_URL: str = os.getenv("SQLITE_URL", "sqlite:///./interview_pilot.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_SEARCH_API_KEY: str = os.getenv("GOOGLE_SEARCH_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # AI Model
    PREFERRED_LLM: str = os.getenv("PREFERRED_LLM", "openai")
    FALLBACK_LLM: str = os.getenv("FALLBACK_LLM", "anthropic")
    
    # Interview Settings
    INTERVIEW_MAX_QUESTIONS: int = int(os.getenv("INTERVIEW_MAX_QUESTIONS", "8"))
    DEFAULT_DIFFICULTY: str = os.getenv("DEFAULT_DIFFICULTY", "medium")
    
    # Enhanced Retry Configuration
    RETRY_MAX_ATTEMPTS: int = int(os.getenv("RETRY_MAX_ATTEMPTS", "3"))
    RETRY_BASE_DELAY: float = float(os.getenv("RETRY_BASE_DELAY", "1.0"))
    RETRY_MAX_DELAY: float = float(os.getenv("RETRY_MAX_DELAY", "60.0"))
    RETRY_TIMEOUT: float = float(os.getenv("RETRY_TIMEOUT", "30.0"))
    RETRY_EXPONENTIAL_BASE: float = float(os.getenv("RETRY_EXPONENTIAL_BASE", "2.0"))
    RETRY_JITTER: bool = os.getenv("RETRY_JITTER", "True").lower() == "true"
    
    # Circuit Breaker Configuration
    CIRCUIT_FAILURE_THRESHOLD: int = int(os.getenv("CIRCUIT_FAILURE_THRESHOLD", "5"))
    CIRCUIT_TIMEOUT_SECONDS: float = float(os.getenv("CIRCUIT_TIMEOUT_SECONDS", "60.0"))
    CIRCUIT_SUCCESS_THRESHOLD: int = int(os.getenv("CIRCUIT_SUCCESS_THRESHOLD", "2"))
    CIRCUIT_FAILURE_WINDOW: float = float(os.getenv("CIRCUIT_FAILURE_WINDOW", "30.0"))
    
    # Enhanced Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/app.log")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "detailed")  # simple, detailed, json
    LOG_MAX_SIZE: int = int(os.getenv("LOG_MAX_SIZE", "10485760"))  # 10MB
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "10"))
    LOG_ENABLE_CORRELATION: bool = os.getenv("LOG_ENABLE_CORRELATION", "True").lower() == "true"
    
    # Observability
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "True").lower() == "true"
    ENABLE_TRACING: bool = os.getenv("ENABLE_TRACING", "False").lower() == "true"
    METRICS_EXPORT_INTERVAL: int = int(os.getenv("METRICS_EXPORT_INTERVAL", "60"))  # seconds
    TRACING_SAMPLING_RATE: float = float(os.getenv("TRACING_SAMPLING_RATE", "0.1"))
    
    # Performance Settings
    MAX_CONCURRENT_OPERATIONS: int = int(os.getenv("MAX_CONCURRENT_OPERATIONS", "10"))
    OPERATION_TIMEOUT: float = float(os.getenv("OPERATION_TIMEOUT", "300.0"))  # 5 minutes
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))  # 1 hour
    ENABLE_RESPONSE_CACHING: bool = os.getenv("ENABLE_RESPONSE_CACHING", "True").lower() == "true"
    
    # Media
    SPEECH_RECOGNITION_TIMEOUT: int = int(os.getenv("SPEECH_RECOGNITION_TIMEOUT", "30"))
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "52428800"))  # 50MB
    TEMP_FILE_DIR: str = os.getenv("TEMP_FILE_DIR", "./temp")
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Enterprise Features
    ENABLE_AUDIT_LOGGING: bool = os.getenv("ENABLE_AUDIT_LOGGING", "True").lower() == "true"
    ENABLE_RATE_LIMITING: bool = os.getenv("ENABLE_RATE_LIMITING", "True").lower() == "true"
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
    ENABLE_HEALTH_CHECKS: bool = os.getenv("ENABLE_HEALTH_CHECKS", "True").lower() == "true"
    
    # Session and State Management
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "120"))
    ENABLE_SESSION_PERSISTENCE: bool = os.getenv("ENABLE_SESSION_PERSISTENCE", "True").lower() == "true"
    STATE_STORAGE_BACKEND: str = os.getenv("STATE_STORAGE_BACKEND", "memory")  # memory, redis, database
    
    # Interview Intelligence Settings
    MIN_QUESTIONS_FOR_ANALYSIS: int = int(os.getenv("MIN_QUESTIONS_FOR_ANALYSIS", "3"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    SKILL_GAP_SEVERITY_THRESHOLD: float = float(os.getenv("SKILL_GAP_SEVERITY_THRESHOLD", "2.0"))
    TOPIC_COVERAGE_GOAL: float = float(os.getenv("TOPIC_COVERAGE_GOAL", "0.8"))  # 80%
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from environment


settings = Settings()
