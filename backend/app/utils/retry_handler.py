"""
Retry Handler - Enterprise-grade retry logic with exponential backoff and circuit breaker pattern.
Provides robust error handling for LLM calls and external service interactions.
"""
from typing import Dict, Any, Optional, Callable, Type, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import time
import random
from datetime import datetime, timedelta
import logging
from functools import wraps


logger = logging.getLogger(__name__)


class CircuitState(str, Enum):
    """Circuit breaker states."""
    CLOSED = "closed"    # Normal operation
    OPEN = "open"        # Fail-fast mode
    HALF_OPEN = "half_open"  # Testing recovery


class RetryableError(Exception):
    """Base exception for retryable errors."""
    pass


class NonRetryableError(Exception):
    """Base exception for non-retryable errors."""
    pass


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    base_delay: float = 1.0  # seconds
    max_delay: float = 60.0  # seconds
    exponential_base: float = 2.0
    jitter: bool = True
    timeout: Optional[float] = 30.0  # seconds
    retryable_exceptions: Tuple[Type[Exception], ...] = (
        RetryableError,
        ConnectionError,
        TimeoutError,
        asyncio.TimeoutError,
    )
    
    def get_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number."""
        # Exponential backoff: base_delay * (exponential_base ^ attempt)
        delay = self.base_delay * (self.exponential_base ** attempt)
        
        # Cap at max_delay
        delay = min(delay, self.max_delay)
        
        # Add jitter to prevent thundering herd
        if self.jitter:
            delay = delay * (0.5 + random.random() * 0.5)
        
        return delay


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 5      # Number of failures to open circuit
    timeout: float = 60.0           # Time to stay open (seconds)
    success_threshold: int = 2      # Successes needed to close in half-open
    failure_window: float = 30.0    # Time window to count failures (seconds)


@dataclass
class CircuitMetrics:
    """Metrics for circuit breaker state."""
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    state_changed_at: datetime = field(default_factory=datetime.now)
    
    def reset(self):
        """Reset all metrics."""
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_success_time = None


class CircuitBreaker:
    """
    Circuit breaker implementation for preventing cascading failures.
    
    Features:
    - Fail-fast when service is likely down
    - Automatic recovery testing
    - Configurable failure thresholds
    - State transition logging
    """
    
    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.state = CircuitState.CLOSED
        self.metrics = CircuitMetrics()
        self._lock = asyncio.Lock()
    
    def is_open(self) -> bool:
        """Check if circuit is open (fail-fast mode)."""
        if self.state == CircuitState.OPEN:
            # Check if timeout has expired
            if (self.metrics.last_failure_time and 
                datetime.now() - self.metrics.last_failure_time > timedelta(seconds=self.config.timeout)):
                self._transition_to_half_open()
            return self.state == CircuitState.OPEN
        return False
    
    def is_half_open(self) -> bool:
        """Check if circuit is in half-open state."""
        return self.state == CircuitState.HALF_OPEN
    
    def can_execute(self) -> bool:
        """Check if operation can be executed."""
        return self.state in [CircuitState.CLOSED, CircuitState.HALF_OPEN]
    
    async def call(self, operation: Callable, *args, **kwargs) -> Any:
        """
        Execute operation with circuit breaker protection.
        
        Args:
            operation: Callable to execute
            *args: Arguments for operation
            **kwargs: Keyword arguments for operation
            
        Returns:
            Result of operation
            
        Raises:
            Exception: If circuit is open or operation fails
        """
        async with self._lock:
            if not self.can_execute():
                raise Exception(f"Circuit breaker '{self.name}' is OPEN - operation rejected")
        
        try:
            result = await operation(*args, **kwargs)
            await self._record_success()
            return result
        except Exception as e:
            await self._record_failure()
            raise e
    
    async def _record_success(self):
        """Record successful operation."""
        async with self._lock:
            self.metrics.success_count += 1
            self.metrics.last_success_time = datetime.now()
            
            if self.state == CircuitState.HALF_OPEN:
                if self.metrics.success_count >= self.config.success_threshold:
                    self._transition_to_closed()
            elif self.state == CircuitState.CLOSED:
                # Reset failure count on success in closed state
                if self._should_reset_failures():
                    self.metrics.failure_count = 0
    
    async def _record_failure(self):
        """Record failed operation."""
        async with self._lock:
            self.metrics.failure_count += 1
            self.metrics.last_failure_time = datetime.now()
            
            if self.state == CircuitState.HALF_OPEN:
                self._transition_to_open()
            elif self.state == CircuitState.CLOSED:
                if self.metrics.failure_count >= self.config.failure_threshold:
                    self._transition_to_open()
    
    def _transition_to_open(self):
        """Transition circuit to OPEN state."""
        old_state = self.state
        self.state = CircuitState.OPEN
        self.metrics.state_changed_at = datetime.now()
        logger.warning(
            f"Circuit breaker '{self.name}' transitioned from {old_state} to OPEN "
            f"after {self.metrics.failure_count} failures"
        )
    
    def _transition_to_half_open(self):
        """Transition circuit to HALF_OPEN state."""
        old_state = self.state
        self.state = CircuitState.HALF_OPEN
        self.metrics.success_count = 0  # Reset success count
        self.metrics.state_changed_at = datetime.now()
        logger.info(
            f"Circuit breaker '{self.name}' transitioned from {old_state} to HALF_OPEN "
            f"after timeout period"
        )
    
    def _transition_to_closed(self):
        """Transition circuit to CLOSED state."""
        old_state = self.state
        self.state = CircuitState.CLOSED
        self.metrics.reset()
        logger.info(
            f"Circuit breaker '{self.name}' transitioned from {old_state} to CLOSED "
            f"after {self.metrics.success_count} successful operations"
        )
    
    def _should_reset_failures(self) -> bool:
        """Check if failure count should be reset based on time window."""
        if not self.metrics.last_failure_time:
            return True
        
        time_since_failure = datetime.now() - self.metrics.last_failure_time
        return time_since_failure > timedelta(seconds=self.config.failure_window)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current circuit breaker status."""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.metrics.failure_count,
            "success_count": self.metrics.success_count,
            "last_failure": self.metrics.last_failure_time.isoformat() if self.metrics.last_failure_time else None,
            "last_success": self.metrics.last_success_time.isoformat() if self.metrics.last_success_time else None,
            "state_changed_at": self.metrics.state_changed_at.isoformat(),
            "can_execute": self.can_execute()
        }


class RetryHandler:
    """
    Enterprise-grade retry handler with circuit breaker integration.
    
    Features:
    - Configurable retry policies
    - Exponential backoff with jitter
    - Circuit breaker pattern
    - Comprehensive metrics and logging
    - Timeout handling
    """
    
    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.default_retry_config = RetryConfig()
        self.default_circuit_config = CircuitBreakerConfig()
    
    def get_circuit_breaker(self, name: str, config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
        """Get or create circuit breaker by name."""
        if name not in self.circuit_breakers:
            config = config or self.default_circuit_config
            self.circuit_breakers[name] = CircuitBreaker(name, config)
        return self.circuit_breakers[name]
    
    async def execute_with_retry(
        self,
        operation: Callable,
        *args,
        retry_config: Optional[RetryConfig] = None,
        circuit_breaker: Optional[CircuitBreaker] = None,
        operation_name: str = "operation",
        **kwargs
    ) -> Any:
        """
        Execute operation with retry logic and circuit breaker.
        
        Args:
            operation: Async callable to execute
            *args: Arguments for operation
            retry_config: Retry configuration
            circuit_breaker: Circuit breaker to use
            operation_name: Name for logging
            **kwargs: Keyword arguments for operation
            
        Returns:
            Result of successful operation
            
        Raises:
            Exception: If all retries fail or circuit is open
        """
        config = retry_config or self.default_retry_config
        
        last_exception = None
        
        for attempt in range(config.max_attempts):
            try:
                # Check circuit breaker if provided
                if circuit_breaker and circuit_breaker.is_open():
                    raise Exception(f"Circuit breaker '{circuit_breaker.name}' is OPEN")
                
                # Execute with timeout if specified
                if config.timeout:
                    result = await asyncio.wait_for(
                        operation(*args, **kwargs),
                        timeout=config.timeout
                    )
                else:
                    result = await operation(*args, **kwargs)
                
                # Record success in circuit breaker
                if circuit_breaker:
                    await circuit_breaker._record_success()
                
                logger.info(f"{operation_name} succeeded on attempt {attempt + 1}")
                return result
                
            except asyncio.TimeoutError as e:
                logger.warning(f"{operation_name} timed out on attempt {attempt + 1}")
                last_exception = e
                if circuit_breaker:
                    await circuit_breaker._record_failure()
                
            except Exception as e:
                logger.warning(f"{operation_name} failed on attempt {attempt + 1}: {str(e)}")
                last_exception = e
                
                # Check if exception is retryable
                if not isinstance(e, config.retryable_exceptions):
                    logger.error(f"{operation_name} failed with non-retryable error: {str(e)}")
                    if circuit_breaker:
                        await circuit_breaker._record_failure()
                    raise e
                
                # Record failure in circuit breaker
                if circuit_breaker:
                    await circuit_breaker._record_failure()
                
                # Don't delay on final attempt
                if attempt < config.max_attempts - 1:
                    delay = config.get_delay(attempt)
                    logger.info(f"Retrying {operation_name} in {delay:.2f} seconds...")
                    await asyncio.sleep(delay)
        
        # All retries exhausted
        logger.error(f"{operation_name} failed after {config.max_attempts} attempts")
        raise last_exception or Exception(f"{operation_name} failed after {config.max_attempts} attempts")
    
    def retry_decorator(
        self,
        retry_config: Optional[RetryConfig] = None,
        circuit_breaker_name: Optional[str] = None,
        circuit_config: Optional[CircuitBreakerConfig] = None
    ):
        """
        Decorator for adding retry logic to async functions.
        
        Args:
            retry_config: Retry configuration
            circuit_breaker_name: Name for circuit breaker
            circuit_config: Circuit breaker configuration
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Get or create circuit breaker
                circuit_breaker = None
                if circuit_breaker_name:
                    circuit_breaker = self.get_circuit_breaker(
                        circuit_breaker_name, 
                        circuit_config
                    )
                
                return await self.execute_with_retry(
                    func,
                    *args,
                    retry_config=retry_config,
                    circuit_breaker=circuit_breaker,
                    operation_name=func.__name__,
                    **kwargs
                )
            return wrapper
        return decorator
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get metrics for all circuit breakers."""
        return {
            name: breaker.get_status()
            for name, breaker in self.circuit_breakers.items()
        }
    
    def reset_all_circuits(self):
        """Reset all circuit breakers to CLOSED state."""
        for breaker in self.circuit_breakers.values():
            breaker.state = CircuitState.CLOSED
            breaker.metrics.reset()
        logger.info("All circuit breakers reset to CLOSED state")


# Global retry handler instance
retry_handler = RetryHandler()


# Convenience functions
async def retry_operation(
    operation: Callable,
    *args,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    timeout: Optional[float] = 30.0,
    circuit_breaker_name: Optional[str] = None,
    **kwargs
) -> Any:
    """
    Convenience function for retrying operations.
    
    Args:
        operation: Async callable to execute
        *args: Arguments for operation
        max_attempts: Maximum retry attempts
        base_delay: Base delay for exponential backoff
        max_delay: Maximum delay between retries
        timeout: Operation timeout
        circuit_breaker_name: Optional circuit breaker name
        **kwargs: Keyword arguments for operation
        
    Returns:
        Result of successful operation
    """
    config = RetryConfig(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=max_delay,
        timeout=timeout
    )
    
    circuit_breaker = None
    if circuit_breaker_name:
        circuit_breaker = retry_handler.get_circuit_breaker(circuit_breaker_name)
    
    return await retry_handler.execute_with_retry(
        operation,
        *args,
        retry_config=config,
        circuit_breaker=circuit_breaker,
        operation_name=operation.__name__ if hasattr(operation, '__name__') else 'operation',
        **kwargs
    )


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    timeout: Optional[float] = 30.0,
    circuit_breaker_name: Optional[str] = None
):
    """
    Decorator for adding retry logic to async functions.
    
    Args:
        max_attempts: Maximum retry attempts
        base_delay: Base delay for exponential backoff
        max_delay: Maximum delay between retries
        timeout: Operation timeout
        circuit_breaker_name: Optional circuit breaker name
    """
    config = RetryConfig(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=max_delay,
        timeout=timeout
    )
    
    circuit_config = None
    if circuit_breaker_name:
        circuit_config = CircuitBreakerConfig()
    
    return retry_handler.retry_decorator(
        retry_config=config,
        circuit_breaker_name=circuit_breaker_name,
        circuit_config=circuit_config
    )