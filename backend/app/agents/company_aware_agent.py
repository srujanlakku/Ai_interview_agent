"""
Company-Aware Interview Tracks - Adapts interview style and expectations based on target company type.

Features:
- Generic interviews (standard technical assessment)
- Product-based company interviews (scalability, user focus)
- Startup-focused interviews (agility, full-stack thinking)
- Company culture and technical stack awareness
- Role-specific adaptations
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class CompanyType(Enum):
    """Types of companies with different interview approaches."""
    GENERIC = "generic"           # Standard technical interviews
    PRODUCT = "product"           # Product-focused companies (Google, Meta, etc.)
    STARTUP = "startup"           # Startup environments (speed, versatility)
    ENTERPRISE = "enterprise"     # Large enterprise (process, architecture)


class InterviewStyle(Enum):
    """Different interview styles based on company culture."""
    TECHNICAL_DEPTH = "technical_depth"      # Deep computer science fundamentals
    SYSTEM_DESIGN = "system_design"          # Scalability and architecture focus
    PRACTICAL_APPLICATION = "practical_app"  # Real-world problem solving
    CULTURAL_FIT = "cultural_fit"            # Teamwork and communication emphasis


@dataclass
class CompanyProfile:
    """Profile defining company characteristics."""
    company_type: CompanyType
    name: str
    interview_focus: List[InterviewStyle]
    technical_stack: List[str]
    culture_traits: List[str]
    question_modifiers: Dict[str, float]  # Adjust question weights/selection
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "company_type": self.company_type.value,
            "name": self.name,
            "interview_focus": [f.value for f in self.interview_focus],
            "technical_stack": self.technical_stack,
            "culture_traits": self.culture_traits,
            "question_modifiers": self.question_modifiers
        }


class CompanyAwareAgent:
    """
    Agent that adapts interview approach based on target company characteristics.
    
    Features:
    - Company type recognition and adaptation
    - Style-appropriate question selection
    - Cultural expectation alignment
    - Technical stack relevance
    - Role-specific customization
    """
    
    def __init__(self):
        self.company_profiles: Dict[str, CompanyProfile] = {}
        self.active_profile: Optional[CompanyProfile] = None
        self._initialize_company_profiles()
    
    def _initialize_company_profiles(self) -> None:
        """Initialize predefined company profiles."""
        # Generic/Standard Profile
        self.company_profiles["generic"] = CompanyProfile(
            company_type=CompanyType.GENERIC,
            name="Generic Technical Interview",
            interview_focus=[
                InterviewStyle.TECHNICAL_DEPTH,
                InterviewStyle.PRACTICAL_APPLICATION
            ],
            technical_stack=["Fundamentals", "Problem Solving", "Communication"],
            culture_traits=["Technical Excellence", "Clear Communication"],
            question_modifiers={
                "dsa_weight": 1.0,
                "system_design_weight": 0.7,
                "behavioral_weight": 0.8,
                "practical_weight": 1.0
            }
        )
        
        # Product Company Profile (Google, Meta, Amazon, etc.)
        self.company_profiles["product"] = CompanyProfile(
            company_type=CompanyType.PRODUCT,
            name="Product-Focused Company",
            interview_focus=[
                InterviewStyle.SYSTEM_DESIGN,
                InterviewStyle.TECHNICAL_DEPTH,
                InterviewStyle.CULTURAL_FIT
            ],
            technical_stack=["Scalability", "Distributed Systems", "User Experience"],
            culture_traits=["Innovation", "Scale Mindset", "User Focus"],
            question_modifiers={
                "dsa_weight": 0.8,
                "system_design_weight": 1.2,
                "behavioral_weight": 1.0,
                "practical_weight": 0.9
            }
        )
        
        # Startup Profile
        self.company_profiles["startup"] = CompanyProfile(
            company_type=CompanyType.STARTUP,
            name="Startup Environment",
            interview_focus=[
                InterviewStyle.PRACTICAL_APPLICATION,
                InterviewStyle.CULTURAL_FIT,
                InterviewStyle.TECHNICAL_DEPTH
            ],
            technical_stack=["Full-Stack", "Speed", "Resourcefulness", "Adaptability"],
            culture_traits=["Velocity", "Versatility", "Ownership", "Scrappiness"],
            question_modifiers={
                "dsa_weight": 0.7,
                "system_design_weight": 0.8,
                "behavioral_weight": 1.2,
                "practical_weight": 1.3
            }
        )
        
        # Enterprise Profile
        self.company_profiles["enterprise"] = CompanyProfile(
            company_type=CompanyType.ENTERPRISE,
            name="Enterprise Organization",
            interview_focus=[
                InterviewStyle.SYSTEM_DESIGN,
                InterviewStyle.TECHNICAL_DEPTH,
                InterviewStyle.CULTURAL_FIT
            ],
            technical_stack=["Architecture", "Security", "Process", "Reliability"],
            culture_traits=["Process Orientation", "Risk Management", "Stability"],
            question_modifiers={
                "dsa_weight": 0.9,
                "system_design_weight": 1.1,
                "behavioral_weight": 0.9,
                "practical_weight": 0.8
            }
        )
        
        logger.info("Company profiles initialized")
    
    def set_company_context(self, company_name: str, role: str = "Software Engineer") -> CompanyProfile:
        """
        Set the active company context for interview adaptation.
        
        Args:
            company_name: Name of target company or company type
            role: Target role (affects adaptation strategy)
            
        Returns:
            Active company profile
        """
        # Normalize company name for lookup
        normalized_name = company_name.lower().strip()
        
        # Direct match
        if normalized_name in self.company_profiles:
            self.active_profile = self.company_profiles[normalized_name]
        else:
            # Try to infer company type from name
            inferred_type = self._infer_company_type(normalized_name, role)
            self.active_profile = self.company_profiles[inferred_type]
        
        logger.info(f"Company context set: {self.active_profile.name} ({self.active_profile.company_type.value})")
        return self.active_profile
    
    def _infer_company_type(self, company_name: str, role: str) -> str:
        """Infer company type from company name and role."""
        company_name_lower = company_name.lower()
        
        # Known product companies
        product_keywords = ["google", "meta", "facebook", "amazon", "microsoft", "apple", "netflix", "uber", "airbnb"]
        if any(keyword in company_name_lower for keyword in product_keywords):
            return "product"
        
        # Startup indicators
        startup_indicators = ["inc", "llc", "startup", "venture", "seed", "series"]
        if any(indicator in company_name_lower for indicator in startup_indicators):
            return "startup"
        
        # Enterprise indicators
        enterprise_indicators = ["bank", "financial", "insurance", "consulting", "corp", "incorporated"]
        if any(indicator in company_name_lower for indicator in enterprise_indicators):
            return "enterprise"
        
        # Default to generic
        return "generic"
    
    def adapt_question_selection(self, base_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt question selection context based on company profile.
        
        Args:
            base_context: Original question selection context
            
        Returns:
            Adapted context with company-aware modifications
        """
        if not self.active_profile:
            return base_context
        
        adapted_context = base_context.copy()
        
        # Apply question weight modifiers
        modifiers = self.active_profile.question_modifiers
        adapted_context["weight_modifiers"] = modifiers
        
        # Adjust topic priorities based on company focus
        focus_areas = self._get_focus_areas()
        adapted_context["priority_topics"] = focus_areas
        
        # Modify difficulty expectations
        adapted_context["difficulty_expectations"] = self._get_difficulty_expectations()
        
        # Add company-specific constraints
        adapted_context["company_constraints"] = self._get_company_constraints()
        
        logger.debug(f"Question selection adapted for {self.active_profile.name}")
        return adapted_context
    
    def adapt_evaluation_criteria(self, base_evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt evaluation criteria based on company culture and expectations.
        
        Args:
            base_evaluation: Original evaluation criteria
            
        Returns:
            Adapted evaluation with company-aware criteria
        """
        if not self.active_profile:
            return base_evaluation
        
        adapted_evaluation = base_evaluation.copy()
        
        # Adjust scoring weights based on company priorities
        style_weights = self._get_style_weights()
        adapted_evaluation["style_weights"] = style_weights
        
        # Add company-specific evaluation dimensions
        adapted_evaluation["company_dimensions"] = self._get_company_dimensions()
        
        # Modify feedback tone and content
        adapted_evaluation["feedback_style"] = self._get_feedback_style()
        
        logger.debug(f"Evaluation criteria adapted for {self.active_profile.name}")
        return adapted_evaluation
    
    def _get_focus_areas(self) -> List[str]:
        """Get priority topics based on company focus."""
        if not self.active_profile:
            return []
        
        focus_map = {
            CompanyType.GENERIC: ["Data Structures", "Algorithms", "System Design Basics"],
            CompanyType.PRODUCT: ["Scalability", "Distributed Systems", "Product Sense"],
            CompanyType.STARTUP: ["Full-Stack Development", "Speed Optimization", "Resource Constraints"],
            CompanyType.ENTERPRISE: ["Enterprise Architecture", "Security", "Process Compliance"]
        }
        
        return focus_map.get(self.active_profile.company_type, [])
    
    def _get_difficulty_expectations(self) -> Dict[str, Any]:
        """Get difficulty expectations for different company types."""
        if not self.active_profile:
            return {}
        
        expectations = {
            CompanyType.GENERIC: {
                "dsa_expectation": "solid_fundamentals",
                "system_design_expectation": "basic_understanding",
                "coding_expectation": "clean_implementation"
            },
            CompanyType.PRODUCT: {
                "dsa_expectation": "advanced_optimization",
                "system_design_expectation": "scalable_architecture",
                "coding_expectation": "production_ready"
            },
            CompanyType.STARTUP: {
                "dsa_expectation": "practical_solutions",
                "system_design_expectation": "iterative_approach",
                "coding_expectation": "working_prototype"
            },
            CompanyType.ENTERPRISE: {
                "dsa_expectation": "robust_solutions",
                "system_design_expectation": "enterprise_grade",
                "coding_expectation": "secure_maintainable"
            }
        }
        
        return expectations.get(self.active_profile.company_type, {})
    
    def _get_company_constraints(self) -> Dict[str, Any]:
        """Get company-specific constraints and preferences."""
        if not self.active_profile:
            return {}
        
        constraints = {
            CompanyType.GENERIC: {
                "time_pressure": "moderate",
                "code_quality": "important",
                "communication": "essential"
            },
            CompanyType.PRODUCT: {
                "time_pressure": "high",
                "code_quality": "critical",
                "scalability": "mandatory"
            },
            CompanyType.STARTUP: {
                "time_pressure": "very_high",
                "code_quality": "functional_first",
                "adaptability": "crucial"
            },
            CompanyType.ENTERPRISE: {
                "time_pressure": "low_moderate",
                "code_quality": "security_first",
                "documentation": "required"
            }
        }
        
        return constraints.get(self.active_profile.company_type, {})
    
    def _get_style_weights(self) -> Dict[str, float]:
        """Get evaluation weight adjustments for different interview styles."""
        focus = self.active_profile.interview_focus if self.active_profile else []
        
        weights = {
            "technical_depth": 1.0,
            "system_design": 1.0,
            "practical_application": 1.0,
            "cultural_fit": 1.0
        }
        
        # Boost weights for company focus areas
        boost_factor = 1.3
        for style in focus:
            if style == InterviewStyle.TECHNICAL_DEPTH:
                weights["technical_depth"] = boost_factor
            elif style == InterviewStyle.SYSTEM_DESIGN:
                weights["system_design"] = boost_factor
            elif style == InterviewStyle.PRACTICAL_APPLICATION:
                weights["practical_application"] = boost_factor
            elif style == InterviewStyle.CULTURAL_FIT:
                weights["cultural_fit"] = boost_factor
        
        return weights
    
    def _get_company_dimensions(self) -> List[str]:
        """Get additional evaluation dimensions specific to company type."""
        if not self.active_profile:
            return []
        
        dimension_map = {
            CompanyType.GENERIC: ["Problem Solving", "Communication"],
            CompanyType.PRODUCT: ["Scalability Thinking", "User Impact"],
            CompanyType.STARTUP: ["Speed", "Resourcefulness", "Ownership"],
            CompanyType.ENTERPRISE: ["Process Awareness", "Risk Management"]
        }
        
        return dimension_map.get(self.active_profile.company_type, [])
    
    def _get_feedback_style(self) -> str:
        """Get appropriate feedback style for company culture."""
        if not self.active_profile:
            return "balanced"
        
        style_map = {
            CompanyType.GENERIC: "balanced",      # Mix of constructive and positive
            CompanyType.PRODUCT: "challenging",   # Push for excellence and innovation
            CompanyType.STARTUP: "encouraging",   # Focus on potential and growth
            CompanyType.ENTERPRISE: "structured"  # Formal, process-oriented feedback
        }
        
        return style_map.get(self.active_profile.company_type, "balanced")
    
    def get_company_guidance(self) -> Dict[str, Any]:
        """Get guidance about company-specific interview approach."""
        if not self.active_profile:
            return {"message": "No company context set"}
        
        return {
            "company_type": self.active_profile.company_type.value,
            "company_name": self.active_profile.name,
            "what_to_expect": self._generate_expectations(),
            "preparation_tips": self._generate_preparation_tips(),
            "success_factors": self._generate_success_factors()
        }
    
    def _generate_expectations(self) -> str:
        """Generate expectations based on company type."""
        if not self.active_profile:
            return ""
        
        expectations = {
            CompanyType.GENERIC: (
                "Expect a balanced assessment of technical fundamentals and problem-solving skills. "
                "Questions will cover data structures, algorithms, and basic system design."
            ),
            CompanyType.PRODUCT: (
                "Prepare for deep technical discussions with emphasis on scalability and large-scale systems. "
                "You'll likely encounter complex system design problems and optimization challenges."
            ),
            CompanyType.STARTUP: (
                "Be ready for practical, hands-on problems that test your versatility and speed. "
                "Expect questions about full-stack development and resource-constrained solutions."
            ),
            CompanyType.ENTERPRISE: (
                "Anticipate rigorous assessment of enterprise architecture, security considerations, "
                "and process adherence. Emphasis on robust, maintainable solutions."
            )
        }
        
        return expectations.get(self.active_profile.company_type, "")
    
    def _generate_preparation_tips(self) -> List[str]:
        """Generate preparation tips for the company type."""
        if not self.active_profile:
            return []
        
        tip_map = {
            CompanyType.GENERIC: [
                "Review core computer science fundamentals",
                "Practice common data structure and algorithm problems",
                "Prepare clear explanations of your problem-solving approach"
            ],
            CompanyType.PRODUCT: [
                "Study distributed systems and scalability patterns",
                "Practice large-scale system design problems",
                "Understand trade-offs in system architecture decisions"
            ],
            CompanyType.STARTUP: [
                "Brush up on full-stack development skills",
                "Practice rapid prototyping and iterative solutions",
                "Prepare examples of shipping products quickly"
            ],
            CompanyType.ENTERPRISE: [
                "Review enterprise architecture patterns",
                "Study security best practices and compliance",
                "Prepare for detailed discussion of past projects"
            ]
        }
        
        return tip_map.get(self.active_profile.company_type, [])
    
    def _generate_success_factors(self) -> List[str]:
        """Generate key success factors for the company type."""
        if not self.active_profile:
            return []
        
        success_map = {
            CompanyType.GENERIC: [
                "Strong fundamentals in CS core areas",
                "Clear communication of technical concepts",
                "Systematic problem-solving approach"
            ],
            CompanyType.PRODUCT: [
                "Deep understanding of scalability challenges",
                "Ability to design systems for massive scale",
                "Innovation and creative problem-solving"
            ],
            CompanyType.STARTUP: [
                "Versatility across tech stack",
                "Speed and efficiency in delivery",
                "Entrepreneurial mindset and ownership"
            ],
            CompanyType.ENTERPRISE: [
                "Architectural thinking and design skills",
                "Attention to security and reliability",
                "Process orientation and documentation"
            ]
        }
        
        return success_map.get(self.active_profile.company_type, [])
    
    def reset(self) -> None:
        """Reset company context for new interview."""
        self.active_profile = None
        logger.info("CompanyAwareAgent reset for new session")