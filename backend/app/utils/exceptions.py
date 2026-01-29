"""
Exception classes for InterviewPilot
"""


class InterviewPilotException(Exception):
    """Base exception for InterviewPilot"""
    def __init__(self, message: str, error_code: str = "GENERAL_ERROR", status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(InterviewPilotException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTH_ERROR", 401)


class AuthorizationError(InterviewPilotException):
    """Raised when authorization fails"""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, "AUTHZ_ERROR", 403)


class ValidationError(InterviewPilotException):
    """Raised when validation fails"""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, "VALIDATION_ERROR", 400)


class NotFoundError(InterviewPilotException):
    """Raised when resource is not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "NOT_FOUND", 404)


class DuplicateError(InterviewPilotException):
    """Raised when trying to create a duplicate resource"""
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, "DUPLICATE_ERROR", 409)


class LLMError(InterviewPilotException):
    """Raised when LLM service fails"""
    def __init__(self, message: str = "LLM service error"):
        super().__init__(message, "LLM_ERROR", 503)


class SpeechRecognitionError(InterviewPilotException):
    """Raised when speech recognition fails"""
    def __init__(self, message: str = "Speech recognition failed"):
        super().__init__(message, "SPEECH_ERROR", 503)


class ResearchError(InterviewPilotException):
    """Raised when research operation fails"""
    def __init__(self, message: str = "Research failed"):
        super().__init__(message, "RESEARCH_ERROR", 503)
