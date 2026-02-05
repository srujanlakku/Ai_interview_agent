"""
Safety & Input Guardrails - Protects against malicious input and ensures safe operation.

Features:
- Prompt injection protection
- Offensive content filtering
- Input sanitization and validation
- Rate limiting and abuse detection
- Graceful error handling and redirection
- Content moderation
"""
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re
import json
from datetime import datetime, timedelta
from collections import defaultdict, deque
import asyncio
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class SafetyLevel(Enum):
    """Levels of safety enforcement."""
    STRICT = "strict"      # Maximum protection, may block legitimate input
    BALANCED = "balanced"  # Good balance of protection and usability
    LENIENT = "lenient"    # Minimal protection, prioritize usability


class ThreatType(Enum):
    """Types of security threats detected."""
    PROMPT_INJECTION = "prompt_injection"
    OFFENSIVE_CONTENT = "offensive_content"
    MALFORMED_INPUT = "malformed_input"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_PATTERN = "suspicious_pattern"


@dataclass
class SafetyViolation:
    """Record of a safety violation."""
    threat_type: ThreatType
    input_text: str
    severity: str  # low, medium, high
    detected_at: datetime
    action_taken: str  # blocked, sanitized, warned
    confidence: float  # 0.0 to 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "threat_type": self.threat_type.value,
            "input_text": self.input_text[:100] + "..." if len(self.input_text) > 100 else self.input_text,
            "severity": self.severity,
            "detected_at": self.detected_at.isoformat(),
            "action_taken": self.action_taken,
            "confidence": round(self.confidence, 2)
        }


class InputGuardrails:
    """
    Comprehensive input protection system.
    
    Features:
    - Multi-layered security checks
    - Real-time threat detection
    - Adaptive protection levels
    - Usage monitoring and rate limiting
    - Graceful degradation
    """
    
    def __init__(self, safety_level: SafetyLevel = SafetyLevel.BALANCED):
        self.safety_level = safety_level
        self.violation_history: List[SafetyViolation] = []
        self.user_rates: Dict[str, deque] = defaultdict(deque)
        self.blocked_users: Dict[str, datetime] = {}
        
        # Protection patterns
        self._initialize_patterns()
        
        # Rate limiting config
        self.rate_limits = {
            "requests_per_minute": 10,
            "requests_per_hour": 50,
            "block_duration_minutes": 30
        }
    
    def _initialize_patterns(self) -> None:
        """Initialize security patterns and filters."""
        # Prompt injection patterns
        self.injection_patterns = [
            r"(?i)(system|assistant|user):\s*",  # Role impersonation
            r"(?i)ignore\s+(all\s+)?(previous\s+)?instructions",
            r"(?i)you\s+are\s+(now\s+)?(an?\s+)?(helpful\s+)?assistant",
            r"(?i)disregard\s+(the\s+)?(above|previous)",
            r"(?i)override\s+(the\s+)?(following\s+)?(instructions|rules)",
            r"(?i)as\s+(an?\s+)?expert",
            r"(?i)from\s+now\s+on",
            r"(?i)new\s+instruction(s?)\s*:",
            r"(?i)your\s+new\s+task",
            r'"""(?:[^"\\]|\\.)*"""',  # Triple quote blocks
            r"'''(?:[^'\\]|\\.)*'''",  # Triple single quote blocks
        ]
        
        # Offensive content patterns (basic)
        self.offensive_patterns = [
            r"(?i)\b(fuck|shit|damn|hell)\b",
            r"(?i)\b(idiot|stupid|dumb)\b",
            r"(?i)\b(hate|hating)\s+(you|this)",
        ]
        
        # Suspicious patterns
        self.suspicious_patterns = [
            r"[^\x00-\x7F]+",  # Non-ASCII characters
            r"(.)\1{10,}",     # Repeated characters
            r"[a-zA-Z]{50,}",  # Very long words
            r"\[[^\]]{100,}\]", # Very long bracketed content
        ]
    
    async def validate_input(
        self,
        input_text: str,
        user_id: str = "anonymous",
        context: str = "general"
    ) -> Tuple[bool, str, Optional[SafetyViolation]]:
        """
        Validate input against safety rules.
        
        Args:
            input_text: Text to validate
            user_id: Identifier for rate limiting
            context: Context of input (interview_answer, question, etc.)
            
        Returns:
            Tuple of (is_safe, sanitized_text, violation_record)
        """
        # Check if user is blocked
        if self._is_user_blocked(user_id):
            violation = SafetyViolation(
                threat_type=ThreatType.RATE_LIMIT_EXCEEDED,
                input_text=input_text,
                severity="high",
                detected_at=datetime.now(),
                action_taken="blocked",
                confidence=1.0
            )
            self.violation_history.append(violation)
            return False, "", violation
        
        # Rate limiting check
        if not self._check_rate_limit(user_id):
            violation = SafetyViolation(
                threat_type=ThreatType.RATE_LIMIT_EXCEEDED,
                input_text=input_text,
                severity="medium",
                detected_at=datetime.now(),
                action_taken="rate_limited",
                confidence=0.9
            )
            self.violation_history.append(violation)
            self._block_user(user_id)
            return False, "Rate limit exceeded. Please try again later.", violation
        
        # Length check
        if len(input_text) > 5000:  # Max 5000 characters
            violation = SafetyViolation(
                threat_type=ThreatType.MALFORMED_INPUT,
                input_text=input_text,
                severity="low",
                detected_at=datetime.now(),
                action_taken="truncated",
                confidence=0.8
            )
            input_text = input_text[:5000]
            self.violation_history.append(violation)
        
        # Security checks
        is_safe, sanitized_text, violation = self._perform_security_checks(input_text, context)
        
        if not is_safe and violation:
            self.violation_history.append(violation)
            
            # Block user for serious violations
            if violation.severity == "high":
                self._block_user(user_id)
        
        return is_safe, sanitized_text, violation
    
    def _perform_security_checks(
        self,
        input_text: str,
        context: str
    ) -> Tuple[bool, str, Optional[SafetyViolation]]:
        """Perform comprehensive security checks."""
        sanitized_text = input_text
        
        # Check for prompt injection
        injection_result = self._check_prompt_injection(input_text, context)
        if injection_result:
            return False, sanitized_text, injection_result
        
        # Check for offensive content
        offensive_result = self._check_offensive_content(input_text)
        if offensive_result:
            # Sanitize offensive content instead of blocking
            sanitized_text = self._sanitize_offensive_content(input_text)
            # Still record violation but allow through
            return True, sanitized_text, offensive_result
        
        # Check for suspicious patterns
        suspicious_result = self._check_suspicious_patterns(input_text)
        if suspicious_result:
            return True, sanitized_text, suspicious_result  # Warn but allow
        
        return True, sanitized_text, None
    
    def _check_prompt_injection(self, text: str, context: str) -> Optional[SafetyViolation]:
        """Check for prompt injection attempts."""
        text_lower = text.lower()
        
        for pattern in self.injection_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return SafetyViolation(
                    threat_type=ThreatType.PROMPT_INJECTION,
                    input_text=text,
                    severity="high",
                    detected_at=datetime.now(),
                    action_taken="blocked",
                    confidence=0.95
                )
        
        # Context-specific checks
        if context == "interview_answer":
            # Check for instruction-like content in answers
            instruction_patterns = [
                r"(?i)^instruction",
                r"(?i)^task:",
                r"(?i)^goal:",
                r"(?i)^(you should|please)"
            ]
            
            for pattern in instruction_patterns:
                if re.match(pattern, text.strip()):
                    return SafetyViolation(
                        threat_type=ThreatType.PROMPT_INJECTION,
                        input_text=text,
                        severity="medium",
                        detected_at=datetime.now(),
                        action_taken="warned",
                        confidence=0.8
                    )
        
        return None
    
    def _check_offensive_content(self, text: str) -> Optional[SafetyViolation]:
        """Check for offensive content."""
        text_lower = text.lower()
        
        offense_count = 0
        for pattern in self.offensive_patterns:
            matches = re.findall(pattern, text_lower)
            offense_count += len(matches)
        
        if offense_count > 0:
            severity = "high" if offense_count > 3 else "medium" if offense_count > 1 else "low"
            confidence = min(0.9, offense_count * 0.3)
            
            return SafetyViolation(
                threat_type=ThreatType.OFFENSIVE_CONTENT,
                input_text=text,
                severity=severity,
                detected_at=datetime.now(),
                action_taken="sanitized",
                confidence=confidence
            )
        
        return None
    
    def _sanitize_offensive_content(self, text: str) -> str:
        """Sanitize offensive content."""
        # Simple replacement - in production, use more sophisticated filtering
        sanitized = text
        replacements = {
            r"(?i)\bfuck\b": "f***",
            r"(?i)\bshit\b": "s***",
            r"(?i)\bidiot\b": "not knowledgeable",
            r"(?i)\bstupid\b": "mistaken"
        }
        
        for pattern, replacement in replacements.items():
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    def _check_suspicious_patterns(self, text: str) -> Optional[SafetyViolation]:
        """Check for suspicious patterns."""
        for pattern in self.suspicious_patterns:
            if re.search(pattern, text):
                return SafetyViolation(
                    threat_type=ThreatType.SUSPICIOUS_PATTERN,
                    input_text=text,
                    severity="low",
                    detected_at=datetime.now(),
                    action_taken="logged",
                    confidence=0.6
                )
        
        return None
    
    def _check_rate_limit(self, user_id: str) -> bool:
        """Check if user has exceeded rate limits."""
        now = datetime.now()
        user_requests = self.user_rates[user_id]
        
        # Remove old requests (older than 1 hour)
        cutoff = now - timedelta(hours=1)
        while user_requests and user_requests[0] < cutoff:
            user_requests.popleft()
        
        # Check minute limit
        minute_cutoff = now - timedelta(minutes=1)
        recent_requests = [req for req in user_requests if req >= minute_cutoff]
        
        if len(recent_requests) >= self.rate_limits["requests_per_minute"]:
            return False
        
        # Check hour limit
        if len(user_requests) >= self.rate_limits["requests_per_hour"]:
            return False
        
        # Add current request
        user_requests.append(now)
        return True
    
    def _is_user_blocked(self, user_id: str) -> bool:
        """Check if user is currently blocked."""
        if user_id in self.blocked_users:
            unblock_time = self.blocked_users[user_id]
            if datetime.now() < unblock_time:
                return True
            else:
                # Unblock expired
                del self.blocked_users[user_id]
        return False
    
    def _block_user(self, user_id: str) -> None:
        """Block user for violation."""
        block_duration = timedelta(minutes=self.rate_limits["block_duration_minutes"])
        self.blocked_users[user_id] = datetime.now() + block_duration
        logger.warning(f"Blocked user {user_id} for {block_duration}")
    
    def get_safety_report(self) -> Dict[str, Any]:
        """Get comprehensive safety report."""
        if not self.violation_history:
            return {"message": "No violations recorded"}
        
        # Statistics
        threat_counts = {}
        severity_counts = {}
        action_counts = {}
        
        for violation in self.violation_history:
            threat = violation.threat_type.value
            severity = violation.severity
            action = violation.action_taken
            
            threat_counts[threat] = threat_counts.get(threat, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            action_counts[action] = action_counts.get(action, 0) + 1
        
        # Recent violations
        recent_violations = [
            v.to_dict() for v in self.violation_history[-10:]
        ]
        
        # Blocked users
        active_blocks = {
            user_id: unblock_time.isoformat()
            for user_id, unblock_time in self.blocked_users.items()
            if datetime.now() < unblock_time
        }
        
        return {
            "total_violations": len(self.violation_history),
            "threat_distribution": threat_counts,
            "severity_distribution": severity_counts,
            "action_distribution": action_counts,
            "active_blocks": len(active_blocks),
            "recent_violations": recent_violations,
            "current_safety_level": self.safety_level.value
        }
    
    def set_safety_level(self, level: SafetyLevel) -> None:
        """Change safety enforcement level."""
        old_level = self.safety_level
        self.safety_level = level
        logger.info(f"Safety level changed from {old_level.value} to {level.value}")
    
    def reset_user_rate(self, user_id: str) -> None:
        """Reset rate limit for specific user."""
        if user_id in self.user_rates:
            self.user_rates[user_id].clear()
        if user_id in self.blocked_users:
            del self.blocked_users[user_id]
        logger.info(f"Reset rate limit for user {user_id}")


class SafeInputProcessor:
    """
    High-level interface for safe input processing.
    
    Provides easy-to-use methods for common safety operations.
    """
    
    def __init__(self):
        self.guardrails = InputGuardrails()
    
    async def process_interview_answer(
        self,
        answer: str,
        user_id: str = "anonymous"
    ) -> Tuple[bool, str, str]:
        """
        Safely process interview answer.
        
        Returns:
            Tuple of (is_valid, processed_answer, feedback_message)
        """
        is_safe, sanitized_answer, violation = await self.guardrails.validate_input(
            answer, user_id, "interview_answer"
        )
        
        if not is_safe:
            if violation and violation.threat_type == ThreatType.RATE_LIMIT_EXCEEDED:
                return False, "", "Too many requests. Please wait before submitting again."
            elif violation and violation.threat_type == ThreatType.PROMPT_INJECTION:
                return False, "", "Invalid input detected. Please provide a genuine answer."
            else:
                # For offensive content, we sanitize and allow through
                return True, sanitized_answer, "Some content was filtered for appropriateness."
        
        return True, sanitized_answer, ""
    
    async def process_question_input(
        self,
        question: str,
        user_id: str = "anonymous"
    ) -> Tuple[bool, str, str]:
        """
        Safely process question input.
        
        Returns:
            Tuple of (is_valid, processed_question, feedback_message)
        """
        is_safe, sanitized_question, violation = await self.guardrails.validate_input(
            question, user_id, "question"
        )
        
        if not is_safe:
            if violation and violation.threat_type == ThreatType.RATE_LIMIT_EXCEEDED:
                return False, "", "Rate limit exceeded. Please try again later."
            else:
                return False, "", "Invalid question format detected."
        
        return True, sanitized_question, ""
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current safety system status."""
        return self.guardrails.get_safety_report()


# Global instance
safe_processor = SafeInputProcessor()


def get_safe_processor() -> SafeInputProcessor:
    """Get global safe input processor instance."""
    return safe_processor