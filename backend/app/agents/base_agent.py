"""
Base agent class for the AI Interview Agent.
Provides OpenAI integration with retry logic and graceful error handling.
"""
import os
import asyncio
import json
import re
from typing import Optional, Dict, Any, List, TypeVar, Callable
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import logging, but don't fail if not available
try:
    from app.utils.logging_config import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# Import structured logging
try:
    from app.utils.structured_logging import get_logger as get_structured_logger
except ImportError:
    from app.utils.logging_config import get_logger as get_structured_logger

# Import error handler for fallback responses
try:
    from app.utils.error_handler import error_handler
except ImportError:
    error_handler = None

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

T = TypeVar('T')


class LLMError(Exception):
    """Exception raised for LLM-related errors."""
    pass


class BaseAgent(ABC):
    """
    Base class for all AI agents in the interview system.
    
    Provides:
    - OpenAI API integration with retry logic
    - Structured JSON extraction
    - Graceful error handling
    - Exponential backoff for retries
    """

    def __init__(self, name: str):
        """
        Initialize the agent.
        
        Args:
            name: Agent name for logging and identification
        """
        self.name = name
        self.retry_count = 3
        self.timeout = 60
        self.base_delay = 1  # Base delay for exponential backoff
        self.use_fallback = False  # Will be set based on API key validity
        self._check_api_key_validity()
    
    def _check_api_key_validity(self):
        """Check if API key is valid and set fallback mode accordingly."""
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
            logger.warning(f"{self.name}: OpenAI API key not configured. Using fallback responses.")
            self.use_fallback = True
        else:
            self.use_fallback = False

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute the agent's main task. Must be implemented by subclasses."""
        pass

    async def call_llm(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        json_mode: bool = False,
    ) -> str:
        """
        Call OpenAI API with retry logic and error handling.
        
        Args:
            prompt: User prompt to send
            system_message: Optional system message
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            json_mode: Whether to request JSON output
            
        Returns:
            LLM response text
            
        Raises:
            LLMError: If all retries fail
        """
        # Use fallback if API key is not configured properly
        if self.use_fallback or not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
            logger.info(f"{self.name}: Using fallback response due to missing/invalid API key")
            return self._get_fallback_response(prompt)
        
        last_error = None
        
        for attempt in range(self.retry_count):
            try:
                return await self._call_openai(
                    prompt, system_message, temperature, max_tokens, json_mode
                )
            except Exception as e:
                last_error = e
                if attempt < self.retry_count - 1:
                    delay = self.base_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(
                        f"{self.name}: Attempt {attempt + 1} failed: {str(e)}. "
                        f"Retrying in {delay}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"{self.name}: All {self.retry_count} attempts failed: {str(e)}")
        
        raise LLMError(f"LLM call failed after {self.retry_count} attempts: {str(last_error)}")

    async def _call_openai(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        json_mode: bool = False,
    ) -> str:
        """
        Make actual OpenAI API call using httpx.
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            json_mode: Request JSON output
            
        Returns:
            Response text
        """
        import httpx
        from app.utils.structured_logging import log_llm_call
        
        start_time = asyncio.get_event_loop().time()
        
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers
            )
            
            end_time = asyncio.get_event_loop().time()
            duration_ms = (end_time - start_time) * 1000
            
            # Log the LLM call
            log_llm_call(
                prompt_length=len(prompt),
                response_length=len(response.text),
                duration_ms=duration_ms
            )
            
            if response.status_code == 429:
                # Rate limited - extract retry-after if available
                retry_after = response.headers.get("retry-after", "60")
                raise LLMError(f"Rate limited. Retry after {retry_after}s")
            
            if response.status_code >= 500:
                raise LLMError(f"OpenAI server error: {response.status_code}")
            
            response.raise_for_status()
            result = response.json()
            
            return result["choices"][0]["message"]["content"]

    def extract_json(self, response: str) -> Dict[str, Any]:
        """
        Extract JSON from LLM response, handling various formats.
        
        Args:
            response: Raw LLM response text
            
        Returns:
            Parsed JSON dictionary, or empty dict if parsing fails
        """
        if not response:
            return {}
        
        # Try direct parsing first
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON in code blocks
        code_block_patterns = [
            r'```json\s*([\s\S]*?)\s*```',
            r'```\s*([\s\S]*?)\s*```',
        ]
        
        for pattern in code_block_patterns:
            match = re.search(pattern, response)
            if match:
                try:
                    return json.loads(match.group(1).strip())
                except json.JSONDecodeError:
                    continue
        
        # Try to find JSON object pattern
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        logger.warning(f"{self.name}: Failed to extract JSON from response")
        return {}

    def extract_json_with_default(
        self,
        response: str,
        default: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extract JSON with fallback to default values.
        
        Args:
            response: Raw LLM response
            default: Default dictionary to return on failure
            
        Returns:
            Parsed JSON or default
        """
        result = self.extract_json(response)
        if not result:
            return default
        
        # Merge with defaults for missing keys
        for key, value in default.items():
            if key not in result:
                result[key] = value
        
        return result

    async def retry_with_backoff(
        self,
        func: Callable[[], T],
        max_retries: Optional[int] = None,
    ) -> T:
        """
        Execute a function with exponential backoff retry.
        
        Args:
            func: Async function to execute
            max_retries: Maximum retry attempts (default: self.retry_count)
            
        Returns:
            Function result
            
        Raises:
            Last exception if all retries fail
        """
        retries = max_retries or self.retry_count
        last_error = None

        for attempt in range(retries):
            try:
                logger.info(f"{self.name}: Attempt {attempt + 1}/{retries}")
                return await func()
            except Exception as e:
                last_error = e
                if attempt < retries - 1:
                    delay = self.base_delay * (2 ** attempt)
                    logger.warning(
                        f"{self.name}: Failed, retrying in {delay}s: {str(e)}"
                    )
                    await asyncio.sleep(delay)

        raise last_error or LLMError(f"{self.name}: All retries exhausted")

    def validate_response(
        self,
        response: Dict[str, Any],
        required_fields: List[str],
    ) -> bool:
        """
        Validate that response contains required fields.
        
        Args:
            response: Response dictionary to validate
            required_fields: List of required field names
            
        Returns:
            True if all fields present, False otherwise
        """
        for field in required_fields:
            if field not in response:
                logger.warning(f"{self.name}: Missing required field: {field}")
                return False
        return True

    def _get_fallback_response(self, prompt: str) -> str:
        """
        Generate fallback response when API is unavailable.
        
        Args:
            prompt: Original prompt that would have been sent to LLM
            
        Returns:
            Fallback response text
        """
        # Determine response type based on prompt content
        prompt_lower = prompt.lower()
        
        if "evaluate" in prompt_lower or "score" in prompt_lower:
            # Evaluation-type prompt
            return json.dumps({
                "score": 5.0,
                "feedback": "Unable to evaluate at this time due to system limitations. Please try again later.",
                "strengths": ["Response provided"],
                "weaknesses": ["System currently unavailable"],
                "correctness_score": 5.0,
                "depth_score": 5.0,
                "clarity_score": 5.0,
                "explanation": "Using fallback evaluation due to system limitations."
            })
        elif "question" in prompt_lower or "ask" in prompt_lower:
            # Question generation prompt
            return json.dumps({
                "question": "Can you tell me about your experience with the technologies relevant to this role?",
                "category": "Behavioral",
                "difficulty": "medium",
                "estimated_time": 120,
                "topic": "General Experience"
            })
        else:
            # Generic fallback
            return "I'm currently unable to process your request due to system limitations. Please try again later."

