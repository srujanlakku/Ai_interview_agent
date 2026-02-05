"""
Production Error Handler for AI Interview Agent
Graceful error handling with user-friendly messages and recovery options
"""
import streamlit as st
from typing import Optional, Dict, Any, Callable
import traceback
from datetime import datetime
from .structured_logging import get_logger
from ..components.ui_components import show_error, show_info_card

logger = get_logger(__name__)

class ProductionErrorHandler:
    """Handles errors gracefully with user-friendly messaging"""
    
    ERROR_TEMPLATES = {
        "api_timeout": {
            "title": "Connection Timeout",
            "message": "The AI service is taking longer than expected to respond.",
            "solution": "Please check your internet connection and try again.",
            "retry_allowed": True
        },
        "api_unauthorized": {
            "title": "Authentication Error",
            "message": "There was an issue connecting to the AI service.",
            "solution": "This has been logged and will be investigated.",
            "retry_allowed": False
        },
        "api_rate_limit": {
            "title": "Service Busy",
            "message": "Too many requests are being processed right now.",
            "solution": "Please wait a moment and try again.",
            "retry_allowed": True,
            "delay_seconds": 30
        },
        "validation_error": {
            "title": "Input Error",
            "message": "There was an issue with the provided information.",
            "solution": "Please check your input and try again.",
            "retry_allowed": True
        },
        "network_error": {
            "title": "Network Connection Issue",
            "message": "Unable to connect to the service.",
            "solution": "Please check your internet connection.",
            "retry_allowed": True
        },
        "generic": {
            "title": "Something Went Wrong",
            "message": "An unexpected error occurred.",
            "solution": "Our team has been notified and is working on it.",
            "retry_allowed": True
        }
    }
    
    @classmethod
    def handle_error(cls, error: Exception, context: str = "", user_friendly: bool = True):
        """Handle error with appropriate logging and user messaging"""
        error_type = cls._classify_error(error)
        template = cls.ERROR_TEMPLATES.get(error_type, cls.ERROR_TEMPLATES["generic"])
        
        # Log the error with full context
        logger.error(f"Error in {context}: {str(error)}", extra={
            "error_type": error_type,
            "context": context,
            "traceback": traceback.format_exc(),
            "user_agent": st.session_state.get("__user_agent", "unknown")
        })
        
        if user_friendly:
            cls._show_user_friendly_error(template, error, context)
        else:
            # For development/debugging
            st.exception(error)
    
    @classmethod
    def _classify_error(cls, error: Exception) -> str:
        """Classify error type for appropriate handling"""
        error_str = str(error).lower()
        
        if "timeout" in error_str or "timed out" in error_str:
            return "api_timeout"
        elif "unauthorized" in error_str or "401" in error_str:
            return "api_unauthorized"
        elif "rate limit" in error_str or "429" in error_str:
            return "api_rate_limit"
        elif "validation" in error_str or "invalid" in error_str:
            return "validation_error"
        elif "connection" in error_str or "network" in error_str:
            return "network_error"
        else:
            return "generic"
    
    @classmethod
    def _show_user_friendly_error(cls, template: Dict, error: Exception, context: str):
        """Display user-friendly error message"""
        show_error(
            template["title"],
            f"{template['message']} ({context})"
        )
        
        # Show solution
        show_info_card(
            "💡 Suggested Action",
            template["solution"],
            icon="🔧"
        )
        
        # Show retry option if allowed
        if template.get("retry_allowed", False):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                delay = template.get("delay_seconds", 5)
                if st.button(f"🔄 Try Again (in {delay}s)", use_container_width=True):
                    import time
                    with st.spinner(f"Retrying in {delay} seconds..."):
                        time.sleep(delay)
                    st.rerun()
    
    @classmethod
    def safe_execute(cls, func: Callable, *args, error_context: str = "", default_return=None, **kwargs):
        """Safely execute function with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            cls.handle_error(e, error_context)
            return default_return
    
    @classmethod
    def with_retry(cls, func: Callable, max_retries: int = 3, delay: float = 1.0, 
                   error_context: str = "") -> Callable:
        """Decorator for functions that should retry on failure"""
        import time
        from functools import wraps
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                    else:
                        cls.handle_error(e, f"{error_context} (after {max_retries} attempts)")
                        raise last_exception
            return None
        return wrapper

class RecoveryManager:
    """Manages error recovery and system health"""
    
    @staticmethod
    def check_system_health() -> Dict[str, Any]:
        """Check overall system health"""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        # Check API connectivity
        try:
            # Simulate API health check
            health_status["components"]["api"] = "healthy"
        except Exception as e:
            health_status["components"]["api"] = f"unhealthy: {str(e)}"
            logger.error(f"API health check failed: {str(e)}")
        
        # Check session state
        try:
            session_state = st.session_state.to_dict()
            health_status["components"]["session"] = "healthy" if session_state else "degraded"
        except Exception as e:
            health_status["components"]["session"] = f"unhealthy: {str(e)}"
        
        return health_status
    
    @staticmethod
    def offer_recovery_options(error_type: str):
        """Offer appropriate recovery options based on error type"""
        recovery_options = {
            "api_timeout": ["Retry connection", "Continue offline", "Contact support"],
            "network_error": ["Check connection", "Retry", "Use cached data"],
            "generic": ["Restart session", "Go to homepage", "Contact support"]
        }
        
        options = recovery_options.get(error_type, recovery_options["generic"])
        
        st.markdown("### Recovery Options")
        for i, option in enumerate(options, 1):
            if st.button(f"{i}. {option}", key=f"recovery_{i}"):
                RecoveryManager._execute_recovery(option)
    
    @staticmethod
    def _execute_recovery(option: str):
        """Execute selected recovery action"""
        logger.info(f"Executing recovery: {option}")
        
        if "Restart session" in option:
            st.session_state.clear()
            st.rerun()
        elif "Go to homepage" in option:
            st.session_state.page = "home"
            st.rerun()
        elif "Retry" in option:
            st.rerun()
        else:
            show_info_card(
                "Support Contact",
                "Please email support@interviewagent.com with details about your issue.",
                icon="📧"
            )

# Convenience functions
def handle_exception(error: Exception, context: str = ""):
    """Handle exception gracefully"""
    ProductionErrorHandler.handle_error(error, context)

def safe_call(func: Callable, *args, error_context: str = "", default_return=None, **kwargs):
    """Safely call function with error handling"""
    return ProductionErrorHandler.safe_execute(func, *args, error_context=error_context, 
                                              default_return=default_return, **kwargs)

def with_retry_logic(max_retries: int = 3, delay: float = 1.0, error_context: str = ""):
    """Decorator for retry logic"""
    return ProductionErrorHandler.with_retry

def check_system_status():
    """Check overall system health"""
    return RecoveryManager.check_system_health()

def show_recovery_options(error_type: str):
    """Show appropriate recovery options"""
    RecoveryManager.offer_recovery_options(error_type)