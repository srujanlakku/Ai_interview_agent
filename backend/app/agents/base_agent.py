"""
Base agent class and utilities for all AI agents
"""
import os
import asyncio
import json
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from app.utils.logging_config import get_logger
from app.utils.exceptions import LLMError
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = get_logger(__name__)

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
PREFERRED_LLM = os.getenv("PREFERRED_LLM", "openai")
FALLBACK_LLM = os.getenv("FALLBACK_LLM", "anthropic")


class BaseAgent(ABC):
    """Base class for all AI agents"""

    def __init__(self, name: str):
        self.name = name
        self.retry_count = 3
        self.timeout = 30

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute agent task"""
        pass

    async def call_llm(self, prompt: str, system_message: Optional[str] = None,
                       temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Call LLM with fallback support"""
        try:
            if PREFERRED_LLM == "openai":
                return await self._call_openai(prompt, system_message, temperature, max_tokens)
            else:
                return await self._call_anthropic(prompt, system_message, temperature, max_tokens)
        except Exception as e:
            logger.warning(f"Primary LLM ({PREFERRED_LLM}) failed: {str(e)}, trying fallback")
            try:
                if FALLBACK_LLM == "anthropic":
                    return await self._call_anthropic(prompt, system_message, temperature, max_tokens)
                else:
                    return await self._call_openai(prompt, system_message, temperature, max_tokens)
            except Exception as fallback_error:
                logger.error(f"Both LLMs failed: {str(fallback_error)}")
                raise LLMError("Failed to get response from LLM services")

    async def _call_openai(self, prompt: str, system_message: Optional[str] = None,
                          temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Call OpenAI API"""
        try:
            if not OPENAI_API_KEY:
                raise LLMError("OpenAI API key not configured")

            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }

            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenAI API error: {e.status_code} - {e.response.text}")
            raise LLMError(f"OpenAI API error: {e.status_code}")
        except Exception as e:
            logger.error(f"Error calling OpenAI: {str(e)}")
            raise LLMError(f"OpenAI call failed: {str(e)}")

    async def _call_anthropic(self, prompt: str, system_message: Optional[str] = None,
                             temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Call Anthropic API"""
        try:
            if not ANTHROPIC_API_KEY:
                raise LLMError("Anthropic API key not configured")

            headers = {
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }

            payload = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": max_tokens,
                "system": system_message or "",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                return result["content"][0]["text"]
        except httpx.HTTPStatusError as e:
            logger.error(f"Anthropic API error: {e.status_code}")
            raise LLMError(f"Anthropic API error: {e.status_code}")
        except Exception as e:
            logger.error(f"Error calling Anthropic: {str(e)}")
            raise LLMError(f"Anthropic call failed: {str(e)}")

    async def retry_with_fallback(self, func, max_retries: int = None):
        """Execute function with retry logic"""
        retries = max_retries or self.retry_count
        last_error = None

        for attempt in range(retries):
            try:
                logger.info(f"{self.name} attempt {attempt + 1}/{retries}")
                return await func()
            except Exception as e:
                last_error = e
                if attempt < retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"{self.name} failed, retrying in {wait_time}s: {str(e)}")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"{self.name} failed after {retries} attempts: {str(e)}")

        raise last_error or LLMError(f"{self.name} failed after {retries} attempts")
