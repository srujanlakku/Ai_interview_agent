"""
Error Handler - Centralized error management with graceful degradation and fallback responses.
Provides comprehensive error handling for enterprise-grade reliability.
"""
from typing import Dict, Any, Optional, Callable, Type, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import traceback
from datetime import datetime
import json
from functools import wraps


logger = logging.getLogger(__name__)


class ErrorSeverity(str, Enum):
    """Error severity levels."""
    LOW = "low"          # Minor issues, can continue
    MEDIUM = "medium"    # Significant issues, degraded functionality
    HIGH = "high"        # Critical issues, partial failure
    CRITICAL = "critical"  # System-wide failure


class ErrorCategory(str, Enum):
    """Error category classification."""
    VALIDATION = "validation"      # Input validation errors
    AUTHENTICATION = "authentication"  # Auth-related errors
    AUTHORIZATION = "authorization"   # Permission errors
    NETWORK = "network"        # Network connectivity issues
    TIMEOUT = "timeout"        # Operation timeouts
    RESOURCE = "resource"      # Resource exhaustion
    BUSINESS = "business"      # Business logic errors
    EXTERNAL = "external"      # External service failures
    INTERNAL = "internal"      # Internal system errors
    UNKNOWN = "unknown"        # Unclassified errors


@dataclass
class ErrorContext:
    """Context information for error handling."""
    operation: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    additional_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat(),
            "additional_data": self.additional_data
        }


@dataclass
class ErrorReport:
    """Structured error report for logging and monitoring."""
    error_id: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    category: ErrorCategory
    context: ErrorContext
    stack_trace: Optional[str] = None
    recovery_action: Optional[str] = None
    affected_components: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_id": self.error_id,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "severity": self.severity.value,
            "category": self.category.value,
            "context": self.context.to_dict(),
            "stack_trace": self.stack_trace,
            "recovery_action": self.recovery_action,
            "affected_components": self.affected_components,
            "timestamp": self.timestamp.isoformat()
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class FallbackResponse:
    """Standardized fallback response structure."""
    
    def __init__(self, data: Any = None, message: str = "Operation completed with limitations"):
        self.data = data
        self.message = message
        self.is_fallback = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "message": self.message,
            "is_fallback": True,
            "timestamp": datetime.now().isoformat()
        }


class ErrorHandler:
    """
    Enterprise-grade error handler with centralized management.
    
    Features:
    - Structured error reporting
    - Graceful degradation
    - Fallback response generation
    - Error categorization and metrics
    - Recovery action suggestions
    """
    
    def __init__(self):
        self.error_counts: Dict[ErrorCategory, int] = {}
        self.recent_errors: List[ErrorReport] = []
        self.max_recent_errors = 100
        self.fallback_handlers: Dict[str, Callable] = {}
    
    def register_fallback_handler(self, operation_name: str, handler: Callable):
        """Register a fallback handler for an operation."""
        self.fallback_handlers[operation_name] = handler
    
    def handle_error(
        self,
        exception: Exception,
        context: ErrorContext,
        default_severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        default_category: ErrorCategory = ErrorCategory.INTERNAL
    ) -> ErrorReport:
        """
        Handle an error with structured reporting.
        
        Args:
            exception: The exception that occurred
            context: Error context information
            default_severity: Default severity if not determined
            default_category: Default category if not determined
            
        Returns:
            ErrorReport with structured information
        """
        # Determine error characteristics
        error_type = type(exception).__name__
        error_message = str(exception)
        severity = self._determine_severity(exception, default_severity)
        category = self._determine_category(exception, default_category)
        
        # Generate error ID
        error_id = f"{context.operation}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(exception)) % 10000:04d}"
        
        # Capture stack trace for internal errors
        stack_trace = None
        if category == ErrorCategory.INTERNAL:
            stack_trace = traceback.format_exc()
        
        # Create error report
        error_report = ErrorReport(
            error_id=error_id,
            error_type=error_type,
            error_message=error_message,
            severity=severity,
            category=category,
            context=context,
            stack_trace=stack_trace,
            affected_components=[context.operation]
        )
        
        # Update metrics
        self._update_metrics(category)
        self._add_to_recent_errors(error_report)
        
        # Log the error
        self._log_error(error_report)
        
        return error_report
    
    def _determine_severity(self, exception: Exception, default: ErrorSeverity) -> ErrorSeverity:
        """Determine error severity based on exception type."""
        severity_mapping = {
            # Low severity - minor issues
            "ValueError": ErrorSeverity.LOW,
            "TypeError": ErrorSeverity.LOW,
            "AttributeError": ErrorSeverity.LOW,
            
            # Medium severity - significant issues
            "TimeoutError": ErrorSeverity.MEDIUM,
            "ConnectionError": ErrorSeverity.MEDIUM,
            "ValidationError": ErrorSeverity.MEDIUM,
            
            # High severity - critical issues
            "RuntimeError": ErrorSeverity.HIGH,
            "MemoryError": ErrorSeverity.HIGH,
            "DatabaseError": ErrorSeverity.HIGH,
            
            # Critical severity - system failures
            "SystemExit": ErrorSeverity.CRITICAL,
            "KeyboardInterrupt": ErrorSeverity.CRITICAL,
        }
        
        return severity_mapping.get(type(exception).__name__, default)
    
    def _determine_category(self, exception: Exception, default: ErrorCategory) -> ErrorCategory:
        """Determine error category based on exception type."""
        category_mapping = {
            # Validation errors
            "ValidationError": ErrorCategory.VALIDATION,
            "ValueError": ErrorCategory.VALIDATION,
            "TypeError": ErrorCategory.VALIDATION,
            
            # Authentication/Authorization
            "AuthenticationError": ErrorCategory.AUTHENTICATION,
            "AuthorizationError": ErrorCategory.AUTHORIZATION,
            
            # Network/Timeout
            "TimeoutError": ErrorCategory.TIMEOUT,
            "ConnectionError": ErrorCategory.NETWORK,
            "NetworkError": ErrorCategory.NETWORK,
            
            # External services
            "LLMError": ErrorCategory.EXTERNAL,
            "ExternalServiceError": ErrorCategory.EXTERNAL,
            
            # Resource issues
            "MemoryError": ErrorCategory.RESOURCE,
            "ResourceExhausted": ErrorCategory.RESOURCE,
        }
        
        return category_mapping.get(type(exception).__name__, default)
    
    def _update_metrics(self, category: ErrorCategory):
        """Update error metrics."""
        self.error_counts[category] = self.error_counts.get(category, 0) + 1
    
    def _add_to_recent_errors(self, error_report: ErrorReport):
        """Add error to recent errors list."""
        self.recent_errors.append(error_report)
        if len(self.recent_errors) > self.max_recent_errors:
            self.recent_errors.pop(0)  # Remove oldest error
    
    def _log_error(self, error_report: ErrorReport):
        """Log error with appropriate level based on severity."""
        log_message = f"Error {error_report.error_id}: {error_report.error_type} - {error_report.error_message}"
        context_data = error_report.context.to_dict()
        
        if error_report.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message, extra={"error_report": error_report.to_dict(), "context": context_data})
        elif error_report.severity == ErrorSeverity.HIGH:
            logger.error(log_message, extra={"error_report": error_report.to_dict(), "context": context_data})
        elif error_report.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message, extra={"error_report": error_report.to_dict(), "context": context_data})
        else:
            logger.info(log_message, extra={"error_report": error_report.to_dict(), "context": context_data})
    
    def get_fallback_response(
        self,
        operation_name: str,
        error_report: ErrorReport,
        default_response: Any = None
    ) -> FallbackResponse:
        """
        Get appropriate fallback response for an operation.
        
        Args:
            operation_name: Name of the operation
            error_report: Error report for context
            default_response: Default fallback data
            
        Returns:
            FallbackResponse with appropriate data
        """
        # Check for custom fallback handler
        if operation_name in self.fallback_handlers:
            try:
                custom_fallback = self.fallback_handlers[operation_name](error_report)
                return FallbackResponse(
                    data=custom_fallback,
                    message=f"Operation '{operation_name}' completed with fallback response due to: {error_report.error_message}"
                )
            except Exception as e:
                logger.warning(f"Custom fallback handler failed for {operation_name}: {str(e)}")
        
        # Default fallback responses based on operation type
        default_fallbacks = {
            "question_generation": {
                "question": "Tell me about your experience with the technologies relevant to this role.",
                "category": "Behavioral",
                "difficulty": "medium",
                "estimated_time": 120
            },
            "answer_evaluation": {
                "score": 5.0,
                "feedback": "Unable to evaluate at this time. Please try again.",
                "strengths": ["Response received"],
                "weaknesses": ["Evaluation temporarily unavailable"]
            },
            "interview_completion": {
                "status": "completed",
                "message": "Interview completed with system limitations",
                "scores": [5.0] * 3  # Default scores
            }
        }
        
        fallback_data = default_fallbacks.get(operation_name, default_response)
        
        return FallbackResponse(
            data=fallback_data,
            message=f"Operation '{operation_name}' completed with limited functionality due to: {error_report.error_message}"
        )
    
    def should_retry(self, error_report: ErrorReport) -> bool:
        """Determine if operation should be retried based on error."""
        # Don't retry critical errors or validation errors
        if error_report.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]:
            return False
        
        if error_report.category in [ErrorCategory.VALIDATION, ErrorCategory.AUTHENTICATION]:
            return False
        
        # Retry network, timeout, and external service errors
        if error_report.category in [ErrorCategory.NETWORK, ErrorCategory.TIMEOUT, ErrorCategory.EXTERNAL]:
            return True
        
        # Retry medium severity internal errors
        if error_report.severity == ErrorSeverity.MEDIUM and error_report.category == ErrorCategory.INTERNAL:
            return True
        
        return False
    
    def get_recovery_suggestion(self, error_report: ErrorReport) -> str:
        """Get recovery action suggestion for an error."""
        suggestions = {
            ErrorCategory.NETWORK: "Check network connectivity and retry the operation",
            ErrorCategory.TIMEOUT: "Increase timeout duration or retry with exponential backoff",
            ErrorCategory.EXTERNAL: "Verify external service status and retry after brief delay",
            ErrorCategory.RESOURCE: "Free up system resources and retry operation",
            ErrorCategory.VALIDATION: "Correct input data and resubmit request",
            ErrorCategory.AUTHENTICATION: "Verify credentials and authentication tokens",
            ErrorCategory.AUTHORIZATION: "Check user permissions and access rights",
            ErrorCategory.INTERNAL: "Contact system administrator for assistance",
        }
        
        return suggestions.get(error_report.category, "Review error details and take appropriate action")
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get current system health status based on recent errors."""
        if not self.recent_errors:
            return {"status": "healthy", "error_rate": 0.0, "message": "No recent errors"}
        
        # Calculate error rate (errors per minute)
        recent_errors = self.recent_errors[-10:]  # Last 10 errors
        if len(recent_errors) < 2:
            error_rate = 0.0
        else:
            time_span = (recent_errors[-1].timestamp - recent_errors[0].timestamp).total_seconds() / 60
            error_rate = len(recent_errors) / max(1.0, time_span)
        
        # Determine health status
        critical_errors = sum(1 for e in recent_errors if e.severity == ErrorSeverity.CRITICAL)
        high_errors = sum(1 for e in recent_errors if e.severity == ErrorSeverity.HIGH)
        
        if critical_errors > 0:
            status = "critical"
            message = f"Critical errors detected: {critical_errors}"
        elif high_errors > 2 or error_rate > 5.0:
            status = "degraded"
            message = f"High error rate: {error_rate:.2f} errors/minute"
        elif error_rate > 2.0:
            status = "warning"
            message = f"Elevated error rate: {error_rate:.2f} errors/minute"
        else:
            status = "healthy"
            message = f"Normal operation with {len(recent_errors)} recent errors"
        
        return {
            "status": status,
            "error_rate": round(error_rate, 2),
            "total_errors": len(self.recent_errors),
            "recent_error_count": len(recent_errors),
            "critical_errors": critical_errors,
            "high_severity_errors": high_errors,
            "category_breakdown": {
                cat.value: count for cat, count in self.error_counts.items()
            },
            "message": message
        }
    
    def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get error summary for specified time period."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        period_errors = [e for e in self.recent_errors if e.timestamp >= cutoff_time]
        
        if not period_errors:
            return {"message": f"No errors in the last {hours} hours"}
        
        # Group by category and severity
        category_counts = {}
        severity_counts = {}
        
        for error in period_errors:
            category_counts[error.category.value] = category_counts.get(error.category.value, 0) + 1
            severity_counts[error.severity.value] = severity_counts.get(error.severity.value, 0) + 1
        
        # Most common errors
        error_types = {}
        for error in period_errors:
            error_types[error.error_type] = error_types.get(error.error_type, 0) + 1
        
        most_common = sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "period_hours": hours,
            "total_errors": len(period_errors),
            "unique_error_types": len(error_types),
            "category_distribution": category_counts,
            "severity_distribution": severity_counts,
            "most_common_errors": [
                {"type": error_type, "count": count} 
                for error_type, count in most_common
            ],
            "first_error": period_errors[0].timestamp.isoformat(),
            "last_error": period_errors[-1].timestamp.isoformat()
        }


# Global error handler instance
error_handler = ErrorHandler()


# Convenience decorator for error handling
def handle_errors(
    operation_name: str,
    context_provider: Optional[Callable] = None,
    fallback_response: Any = None
):
    """
    Decorator for adding centralized error handling to async functions.
    
    Args:
        operation_name: Name of the operation for logging
        context_provider: Optional function to provide error context
        fallback_response: Default fallback response data
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create error context
            if context_provider:
                context = context_provider(*args, **kwargs)
            else:
                context = ErrorContext(operation=operation_name)
            
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                # Handle the error
                error_report = error_handler.handle_error(e, context)
                
                # Log the error
                logger.error(f"Error in {operation_name}: {str(e)}", exc_info=True)
                
                # Return fallback response if available
                if error_handler.should_retry(error_report):
                    # Could implement retry logic here
                    pass
                
                fallback = error_handler.get_fallback_response(
                    operation_name, 
                    error_report, 
                    fallback_response
                )
                return fallback.to_dict()
        
        return wrapper
    return decorator


# Import for timedelta (needed for error summary)
from datetime import timedelta