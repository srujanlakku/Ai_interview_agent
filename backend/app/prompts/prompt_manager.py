"""
Prompt & Model Abstraction Layer - Centralized prompt management and model abstraction.

Features:
- Centralized prompt repository with versioning
- Easy model switching (OpenAI, Anthropic, etc.)
- Prompt templates with parameter substitution
- A/B testing framework
- Usage tracking and analytics
- No hardcoded prompts in business logic
"""
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime
import hashlib
from abc import ABC, abstractmethod
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class ModelProvider(Enum):
    """Supported AI model providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    COHERE = "cohere"


class PromptCategory(Enum):
    """Categories of prompts used in the system."""
    INTERVIEWER = "interviewer"
    EVALUATOR = "evaluator"
    QUESTION_SELECTOR = "question_selector"
    REFLECTION = "reflection"
    LEARNING = "learning"
    TERMINATION = "termination"
    COMPANY_AWARE = "company_aware"
    SAFETY = "safety"


@dataclass
class PromptTemplate:
    """Template for a prompt with metadata."""
    name: str
    category: PromptCategory
    version: str
    template: str
    parameters: List[str]
    provider: ModelProvider
    temperature: float = 0.7
    max_tokens: int = 1000
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "category": self.category.value,
            "version": self.version,
            "template": self.template,
            "parameters": self.parameters,
            "provider": self.provider.value,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "created_at": self.created_at.isoformat()
        }
    
    def render(self, **kwargs) -> str:
        """Render template with provided parameters."""
        # Validate required parameters
        missing_params = set(self.parameters) - set(kwargs.keys())
        if missing_params:
            raise ValueError(f"Missing required parameters: {missing_params}")
        
        # Render template
        rendered = self.template.format(**kwargs)
        return rendered
    
    def get_hash(self) -> str:
        """Get unique hash for this prompt version."""
        content = f"{self.name}_{self.version}_{self.template}"
        return hashlib.md5(content.encode()).hexdigest()[:8]


class ModelInterface(ABC):
    """Abstract interface for AI model providers."""
    
    @abstractmethod
    async def generate_completion(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate completion from the model."""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get provider name."""
        pass


class OpenAIModel(ModelInterface):
    """OpenAI model implementation."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client."""
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=self.api_key)
        except ImportError:
            logger.warning("OpenAI library not available")
            self.client = None
    
    async def generate_completion(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate completion using OpenAI."""
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Default model
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI completion failed: {str(e)}")
            raise
    
    def get_provider_name(self) -> str:
        return "openai"


class PromptManager:
    """
    Centralized prompt management system.
    
    Features:
    - Template-based prompt management
    - Version control for prompts
    - A/B testing capabilities
    - Usage tracking and analytics
    - Provider abstraction
    """
    
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self.models: Dict[ModelProvider, ModelInterface] = {}
        self.prompt_usage: Dict[str, int] = {}
        self.ab_tests: Dict[str, Dict[str, Any]] = {}
        self._load_default_templates()
        self._initialize_models()
    
    def _load_default_templates(self) -> None:
        """Load default prompt templates."""
        # Interviewer prompts
        self.register_template(PromptTemplate(
            name="interviewer_question",
            category=PromptCategory.INTERVIEWER,
            version="1.0",
            template="""You are conducting a technical interview for a {role} position.
Candidate experience level: {experience_level}

Ask exactly ONE technical question that tests {topic} knowledge.
Question should be {difficulty} difficulty level.

Return ONLY the question text, nothing else.

Question:""",
            parameters=["role", "experience_level", "topic", "difficulty"],
            provider=ModelProvider.OPENAI,
            temperature=0.6
        ))
        
        # Evaluator prompts
        self.register_template(PromptTemplate(
            name="evaluate_answer",
            category=PromptCategory.EVALUATOR,
            version="1.0",
            template="""Evaluate this interview answer:

Question: {question}
Answer: {answer}
Expected Level: {experience_level}

Provide evaluation in JSON format:
{{
    "score": 0-10,
    "feedback": "Constructive feedback",
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "correctness": 0-10,
    "depth": 0-10,
    "clarity": 0-10
}}""",
            parameters=["question", "answer", "experience_level"],
            provider=ModelProvider.OPENAI,
            temperature=0.3
        ))
        
        # Reflection prompts
        self.register_template(PromptTemplate(
            name="reflect_interaction",
            category=PromptCategory.REFLECTION,
            version="1.0",
            template="""Analyze this interview interaction:

Question: "{question}"
Answer: "{answer}"
Score: {score}/10

Was this question effective? What should be the next step?

Respond in JSON:
{{
    "effectiveness": "high|medium|low",
    "next_action": "deeper_probing|topic_switch|difficulty_adjustment|maintain_current",
    "reasoning": "Detailed explanation",
    "confidence": 0.0-1.0
}}""",
            parameters=["question", "answer", "score"],
            provider=ModelProvider.OPENAI,
            temperature=0.4
        ))
        
        # Learning mode prompts
        self.register_template(PromptTemplate(
            name="explain_concept",
            category=PromptCategory.LEARNING,
            version="1.0",
            template="""Explain this technical concept clearly:

Topic: {topic}
Candidate Level: {skill_level}
Performance: {score}/10

Provide a step-by-step explanation that builds from the candidate's current understanding.
Include examples and common pitfalls to avoid.""",
            parameters=["topic", "skill_level", "score"],
            provider=ModelProvider.OPENAI,
            temperature=0.5
        ))
        
        logger.info("Default prompt templates loaded")
    
    def _initialize_models(self) -> None:
        """Initialize model providers."""
        try:
            import os
            
            # OpenAI
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                self.models[ModelProvider.OPENAI] = OpenAIModel(openai_key)
                logger.info("OpenAI model initialized")
            
            # TODO: Add other providers (Anthropic, Gemini, etc.)
            
        except Exception as e:
            logger.error(f"Failed to initialize models: {str(e)}")
    
    def register_template(self, template: PromptTemplate) -> None:
        """Register a new prompt template."""
        template_id = f"{template.name}_v{template.version}"
        self.templates[template_id] = template
        logger.info(f"Registered template: {template_id}")
    
    def get_template(self, name: str, version: str = "latest") -> Optional[PromptTemplate]:
        """Get prompt template by name and version."""
        if version == "latest":
            # Find latest version
            matching_templates = [
                t for t in self.templates.values()
                if t.name == name
            ]
            if matching_templates:
                # Sort by version and return latest
                return sorted(matching_templates, key=lambda x: x.version)[-1]
        else:
            template_id = f"{name}_v{version}"
            return self.templates.get(template_id)
        
        return None
    
    async def render_and_execute(
        self,
        template_name: str,
        version: str = "latest",
        provider: Optional[ModelProvider] = None,
        **kwargs
    ) -> str:
        """
        Render prompt template and execute with specified model.
        
        Args:
            template_name: Name of template to use
            version: Template version (default: latest)
            provider: Model provider to use (default: template's provider)
            **kwargs: Template parameters
            
        Returns:
            Model completion result
        """
        # Get template
        template = self.get_template(template_name, version)
        if not template:
            raise ValueError(f"Template not found: {template_name} v{version}")
        
        # Determine provider
        target_provider = provider or template.provider
        
        # Check if provider is available
        if target_provider not in self.models:
            raise ValueError(f"Model provider not available: {target_provider.value}")
        
        # Render prompt
        try:
            rendered_prompt = template.render(**kwargs)
        except Exception as e:
            logger.error(f"Failed to render prompt {template_name}: {str(e)}")
            raise
        
        # Execute with model
        model = self.models[target_provider]
        try:
            result = await model.generate_completion(
                prompt=rendered_prompt,
                temperature=template.temperature,
                max_tokens=template.max_tokens
            )
            
            # Track usage
            self._track_prompt_usage(template.name)
            
            logger.debug(f"Executed prompt {template_name} with {target_provider.value}")
            return result
            
        except Exception as e:
            logger.error(f"Model execution failed for {template_name}: {str(e)}")
            raise
    
    def _track_prompt_usage(self, template_name: str) -> None:
        """Track prompt usage for analytics."""
        self.prompt_usage[template_name] = self.prompt_usage.get(template_name, 0) + 1
    
    def start_ab_test(
        self,
        test_name: str,
        template_a: str,
        template_b: str,
        traffic_split: float = 0.5
    ) -> None:
        """Start A/B test between two prompt templates."""
        self.ab_tests[test_name] = {
            "template_a": template_a,
            "template_b": template_b,
            "traffic_split": traffic_split,
            "started_at": datetime.now(),
            "results_a": {"renders": 0, "completions": 0},
            "results_b": {"renders": 0, "completions": 0}
        }
        logger.info(f"Started A/B test: {test_name}")
    
    def get_ab_test_results(self, test_name: str) -> Optional[Dict[str, Any]]:
        """Get results for A/B test."""
        return self.ab_tests.get(test_name)
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get prompt usage statistics."""
        total_usage = sum(self.prompt_usage.values())
        
        return {
            "total_calls": total_usage,
            "by_template": self.prompt_usage,
            "by_category": self._get_category_usage(),
            "active_templates": len(self.templates),
            "active_models": len(self.models)
        }
    
    def _get_category_usage(self) -> Dict[str, int]:
        """Get usage statistics by category."""
        category_usage = {}
        for template_name, count in self.prompt_usage.items():
            # Find template to get category
            template = None
            for t in self.templates.values():
                if t.name == template_name:
                    template = t
                    break
            
            if template:
                category = template.category.value
                category_usage[category] = category_usage.get(category, 0) + count
        
        return category_usage
    
    def export_templates(self) -> str:
        """Export all templates as JSON."""
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "templates": [t.to_dict() for t in self.templates.values()]
        }
        return json.dumps(export_data, indent=2)
    
    def import_templates(self, json_data: str) -> None:
        """Import templates from JSON."""
        try:
            data = json.loads(json_data)
            for template_data in data.get("templates", []):
                template = PromptTemplate(
                    name=template_data["name"],
                    category=PromptCategory(template_data["category"]),
                    version=template_data["version"],
                    template=template_data["template"],
                    parameters=template_data["parameters"],
                    provider=ModelProvider(template_data["provider"]),
                    temperature=template_data.get("temperature", 0.7),
                    max_tokens=template_data.get("max_tokens", 1000),
                    created_at=datetime.fromisoformat(template_data["created_at"])
                )
                self.register_template(template)
            
            logger.info(f"Imported {len(data.get('templates', []))} templates")
            
        except Exception as e:
            logger.error(f"Failed to import templates: {str(e)}")
            raise


# Global prompt manager instance
prompt_manager = PromptManager()


def get_prompt_manager() -> PromptManager:
    """Get global prompt manager instance."""
    return prompt_manager