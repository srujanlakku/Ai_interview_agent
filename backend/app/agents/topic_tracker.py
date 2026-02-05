"""
Enhanced Topic Tracker - Tracks interview topics with familiarity scoring and balanced coverage.
Provides intelligent topic selection with adaptive depth and reinforcement learning.
"""
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math


class TopicCategory(str, Enum):
    """Main topic categories for technical interviews."""
    DSA = "Data Structures & Algorithms"
    SYSTEM_DESIGN = "System Design"
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    DATABASES = "Databases"
    API_DESIGN = "API Design"
    CLOUD = "Cloud & Infrastructure"
    SECURITY = "Security"
    TESTING = "Testing"
    BEHAVIORAL = "Behavioral"
    ML_AI = "Machine Learning & AI"
    DEVOPS = "DevOps & CI/CD"
    NETWORKING = "Networking"
    OS_CONCEPTS = "Operating Systems"
    CONCURRENCY = "Concurrency & Parallelism"


@dataclass
class TopicScore:
    """Enhanced topic tracking with familiarity scoring and adaptive learning."""
    topic: str
    category: TopicCategory
    questions_asked: int = 0
    total_score: float = 0.0
    scores: List[float] = field(default_factory=list)
    first_exposure: Optional[datetime] = None
    last_exposure: Optional[datetime] = None
    familiarity_score: float = 0.0  # 0.0 to 1.0, tracks how well-versed candidate is
    confidence_trend: List[float] = field(default_factory=list)  # Recent confidence levels
    reinforcement_needed: bool = False
    depth_level: int = 1  # Current depth level (1=surface, 2=intermediate, 3=deep)
    
    def __post_init__(self):
        if not self.first_exposure:
            self.first_exposure = datetime.now()
        self.last_exposure = datetime.now()
    
    @property
    def average_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)
    
    @property
    def is_weak(self) -> bool:
        """Topic is weak if average score < 5 or shows declining trend."""
        if not self.scores:
            return False
        return (self.average_score < 5.0 and self.questions_asked > 0) or self._has_declining_trend()
    
    @property
    def is_strong(self) -> bool:
        """Topic is strong if average score >= 7 and shows improving/stable trend."""
        if not self.scores:
            return False
        return self.average_score >= 7.0 and self.questions_asked > 0 and not self._has_declining_trend()
    
    @property
    def is_moderate(self) -> bool:
        """Topic shows moderate performance (5-7 range)."""
        return not self.is_weak and not self.is_strong
    
    def _has_declining_trend(self) -> bool:
        """Check if there's a declining performance trend."""
        if len(self.scores) < 3:
            return False
        
        # Compare first half vs second half
        mid = len(self.scores) // 2
        first_avg = sum(self.scores[:mid]) / mid
        second_avg = sum(self.scores[mid:]) / (len(self.scores) - mid)
        
        return second_avg < first_avg - 1.0  # Significant decline
    
    def add_score(self, score: float, confidence: Optional[float] = None) -> None:
        """Add a new score and update familiarity metrics."""
        self.questions_asked += 1
        self.total_score += score
        self.scores.append(score)
        self.last_exposure = datetime.now()
        
        # Update confidence trend
        if confidence is not None:
            self.confidence_trend.append(confidence)
            if len(self.confidence_trend) > 5:  # Keep only recent 5
                self.confidence_trend = self.confidence_trend[-5:]
        
        # Update familiarity score based on performance and exposure
        self._update_familiarity_score()
        
        # Determine if reinforcement is needed
        self._assess_reinforcement_need()
    
    def _update_familiarity_score(self) -> None:
        """Update familiarity score based on performance history."""
        if not self.scores:
            self.familiarity_score = 0.0
            return
        
        # Base familiarity on average score and number of questions
        score_component = self.average_score / 10.0  # Normalize to 0-1
        exposure_component = min(1.0, self.questions_asked / 5.0)  # Cap at 5 questions
        
        # Weight more recent performance higher
        if len(self.scores) >= 3:
            recent_avg = sum(self.scores[-3:]) / 3
            recency_bonus = (recent_avg - self.average_score) / 10.0
        else:
            recency_bonus = 0.0
        
        self.familiarity_score = min(1.0, (score_component * 0.6 + exposure_component * 0.4 + recency_bonus))
    
    def _assess_reinforcement_need(self) -> None:
        """Determine if this topic needs reinforcement."""
        if len(self.scores) < 2:
            self.reinforcement_needed = False
            return
        
        # Reinforcement needed if:
        # 1. Recent performance is worse than average
        # 2. Performance is volatile
        # 3. Topic is weak
        recent_scores = self.scores[-2:]
        recent_avg = sum(recent_scores) / len(recent_scores)
        
        performance_drop = self.average_score - recent_avg
        volatility = self._calculate_volatility()
        
        self.reinforcement_needed = (
            performance_drop > 1.5 or 
            volatility > 2.0 or 
            self.is_weak
        )
    
    def _calculate_volatility(self) -> float:
        """Calculate score volatility (standard deviation)."""
        if len(self.scores) < 2:
            return 0.0
        
        avg = self.average_score
        variance = sum((s - avg) ** 2 for s in self.scores) / len(self.scores)
        return math.sqrt(variance)
    
    def get_suggested_depth(self) -> int:
        """Suggest appropriate depth level based on familiarity."""
        if self.familiarity_score >= 0.8 and self.is_strong:
            return 3  # Deep dive
        elif self.familiarity_score >= 0.5:
            return 2  # Intermediate
        else:
            return 1  # Surface level
    
    def get_reinforcement_priority(self) -> float:
        """Calculate priority for reinforcement (higher = more urgent)."""
        if not self.reinforcement_needed:
            return 0.0
        
        priority = 0.0
        
        # Base priority on weakness
        if self.is_weak:
            priority += 0.5
        
        # Add priority for declining trend
        if self._has_declining_trend():
            priority += 0.3
        
        # Add priority for high volatility
        volatility = self._calculate_volatility()
        if volatility > 2.0:
            priority += min(0.3, volatility / 10.0)
        
        # Time decay factor (more urgent if not recently addressed)
        if self.last_exposure:
            days_since = (datetime.now() - self.last_exposure).days
            time_factor = min(1.0, days_since / 7.0)  # Cap at 1 week
            priority += time_factor * 0.2
        
        return min(1.0, priority)


@dataclass
class TopicCoverage:
    """Enhanced topic coverage tracking with balanced selection and adaptive learning."""
    target_topics: List[TopicCategory]
    covered_topics: Dict[TopicCategory, TopicScore] = field(default_factory=dict)
    asked_questions: Set[str] = field(default_factory=set)
    semantic_cache: List[str] = field(default_factory=list)  # For semantic similarity check
    coverage_goals: Dict[TopicCategory, float] = field(default_factory=dict)  # Target coverage percentage
    topic_frequencies: Dict[TopicCategory, int] = field(default_factory=dict)  # How often each topic was selected
    last_topic_sequence: List[TopicCategory] = field(default_factory=list)  # Recent topic sequence
    
    def __post_init__(self):
        # Set default coverage goals (80% for target topics)
        for topic in self.target_topics:
            self.coverage_goals[topic] = 0.8
    
    def record_question(
        self,
        topic: str,
        category: TopicCategory,
        question_id: str,
        question_text: str,
        difficulty: str = "medium"
    ) -> None:
        """Record that a question was asked on a topic."""
        if category not in self.covered_topics:
            self.covered_topics[category] = TopicScore(topic=topic, category=category)
        
        self.asked_questions.add(question_id)
        # Store question text for semantic similarity (first 100 chars)
        self.semantic_cache.append(question_text[:100].lower())
        
        # Update frequency tracking
        self.topic_frequencies[category] = self.topic_frequencies.get(category, 0) + 1
        
        # Update topic sequence (keep last 3)
        self.last_topic_sequence.append(category)
        if len(self.last_topic_sequence) > 3:
            self.last_topic_sequence = self.last_topic_sequence[-3:]
    
    def record_score(self, category: TopicCategory, score: float, confidence: Optional[float] = None) -> None:
        """Record a score for a topic category."""
        if category in self.covered_topics:
            self.covered_topics[category].add_score(score, confidence)
    
    def get_uncovered_categories(self) -> List[TopicCategory]:
        """Get categories not yet covered or under-covered."""
        uncovered = []
        for category in self.target_topics:
            if category not in self.covered_topics:
                uncovered.append(category)
            else:
                # Check if coverage goal is met
                current_coverage = len([q for q in self.asked_questions 
                                      if self._question_category_matches(q, category)]) / max(1, len(self.asked_questions))
                if current_coverage < self.coverage_goals.get(category, 0.8):
                    uncovered.append(category)
        return uncovered
    
    def get_weak_categories(self) -> List[TopicCategory]:
        """Get categories where candidate is weak."""
        return [cat for cat, score in self.covered_topics.items() if score.is_weak]
    
    def get_strong_categories(self) -> List[TopicCategory]:
        """Get categories where candidate is strong."""
        return [cat for cat, score in self.covered_topics.items() if score.is_strong]
    
    def get_moderate_categories(self) -> List[TopicCategory]:
        """Get categories with moderate performance."""
        return [cat for cat, score in self.covered_topics.items() if score.is_moderate]
    
    def get_categories_needing_reinforcement(self) -> List[Tuple[TopicCategory, float]]:
        """Get categories that need reinforcement, sorted by priority."""
        reinforcement_list = []
        for category, score in self.covered_topics.items():
            if score.reinforcement_needed:
                priority = score.get_reinforcement_priority()
                reinforcement_list.append((category, priority))
        
        # Sort by priority (highest first)
        reinforcement_list.sort(key=lambda x: x[1], reverse=True)
        return reinforcement_list
    
    def get_coverage_percentage(self) -> float:
        """Get percentage of target topics adequately covered."""
        if not self.target_topics:
            return 100.0
        
        covered_count = 0
        for category in self.target_topics:
            if category in self.covered_topics:
                score = self.covered_topics[category]
                # Consider covered if familiarity score > 0.3 or questions asked > 1
                if score.familiarity_score > 0.3 or score.questions_asked > 1:
                    covered_count += 1
        
        return (covered_count / len(self.target_topics)) * 100
    
    def get_balanced_topic_selection(self) -> Optional[TopicCategory]:
        """
        Intelligently select next topic for balanced coverage.
        
        Strategy:
        1. Prioritize uncovered/under-covered topics
        2. Address weak areas needing reinforcement
        3. Avoid recent topic repetition
        4. Balance strong and moderate topics
        """
        # 1. Check for uncovered topics first
        uncovered = self.get_uncovered_categories()
        if uncovered:
            # Prefer topics that haven't been asked recently
            for category in uncovered:
                if category not in self.last_topic_sequence[-2:]:  # Not in last 2 topics
                    return category
            return uncovered[0]  # Fallback to first uncovered
        
        # 2. Check for reinforcement needs
        reinforcement_needed = self.get_categories_needing_reinforcement()
        if reinforcement_needed:
            # Return highest priority reinforcement topic
            # But avoid immediate repetition
            for category, _ in reinforcement_needed:
                if category not in self.last_topic_sequence[-1:]:  # Not last topic
                    return category
        
        # 3. Balance existing coverage
        # Find least frequently asked topic among covered ones
        if self.covered_topics:
            # Get categories sorted by frequency (ascending)
            sorted_by_frequency = sorted(
                self.covered_topics.keys(),
                key=lambda c: self.topic_frequencies.get(c, 0)
            )
            
            # Avoid recent repetition
            for category in sorted_by_frequency:
                if category not in self.last_topic_sequence[-2:]:
                    return category
            
            # Final fallback
            return sorted_by_frequency[0]
        
        # 4. Default to first target topic
        return self.target_topics[0] if self.target_topics else None
    
    def get_adaptive_depth_suggestion(self, category: TopicCategory) -> int:
        """Get suggested depth level for a topic."""
        if category in self.covered_topics:
            return self.covered_topics[category].get_suggested_depth()
        return 1  # Default to surface level
    
    def is_question_similar(self, question_text: str, threshold: float = 0.7) -> bool:
        """Enhanced semantic similarity check."""
        if not self.semantic_cache:
            return False
            
        new_words = set(question_text.lower().split())
        
        for cached in self.semantic_cache[-5:]:  # Check only recent questions
            cached_words = set(cached.split())
            if cached_words and new_words:
                similarity = len(new_words & cached_words) / max(len(new_words | cached_words), 1)
                if similarity > threshold:
                    return True
        return False
    
    def get_next_priority_category(self) -> Optional[TopicCategory]:
        """Enhanced priority category selection."""
        return self.get_balanced_topic_selection()
    
    def get_coverage_balance_report(self) -> Dict[str, Any]:
        """Get detailed coverage balance analysis."""
        total_questions = len(self.asked_questions)
        
        category_stats = {}
        for category, score in self.covered_topics.items():
            category_stats[category.value] = {
                "questions_asked": score.questions_asked,
                "average_score": round(score.average_score, 2),
                "familiarity_score": round(score.familiarity_score, 2),
                "is_weak": score.is_weak,
                "is_strong": score.is_strong,
                "reinforcement_needed": score.reinforcement_needed,
                "reinforcement_priority": round(score.get_reinforcement_priority(), 2),
                "suggested_depth": score.get_suggested_depth(),
                "frequency": self.topic_frequencies.get(category, 0)
            }
        
        # Coverage metrics
        uncovered_cats = [cat.value for cat in self.get_uncovered_categories()]
        weak_cats = [cat.value for cat in self.get_weak_categories()]
        strong_cats = [cat.value for cat in self.get_strong_categories()]
        reinforcement_cats = [cat.value for cat, _ in self.get_categories_needing_reinforcement()]
        
        return {
            "total_questions": total_questions,
            "categories_covered": len(self.covered_topics),
            "target_categories": len(self.target_topics),
            "coverage_percentage": round(self.get_coverage_percentage(), 1),
            "coverage_balance": round(self._calculate_coverage_balance(), 2),
            "uncovered_areas": uncovered_cats,
            "weak_areas": weak_cats,
            "strong_areas": strong_cats,
            "reinforcement_priorities": reinforcement_cats,
            "recent_topic_sequence": [cat.value for cat in self.last_topic_sequence],
            "category_detailed_stats": category_stats
        }
    
    def _calculate_coverage_balance(self) -> float:
        """Calculate how well coverage is balanced across topics."""
        if not self.covered_topics:
            return 0.0
        
        frequencies = list(self.topic_frequencies.values())
        if len(frequencies) < 2:
            return 1.0  # Perfectly balanced if only one topic
        
        # Calculate coefficient of variation (lower = more balanced)
        mean_freq = sum(frequencies) / len(frequencies)
        if mean_freq == 0:
            return 1.0
            
        variance = sum((f - mean_freq) ** 2 for f in frequencies) / len(frequencies)
        std_dev = math.sqrt(variance)
        cv = std_dev / mean_freq if mean_freq > 0 else 0
        
        # Convert to balance score (0-1, where 1 is perfectly balanced)
        return max(0.0, 1.0 - min(1.0, cv))
    
    def _question_category_matches(self, question_id: str, category: TopicCategory) -> bool:
        """Check if a question belongs to a specific category."""
        # This would need to be implemented based on your question storage
        # For now, we'll assume it matches if the category has been recorded
        return category in self.covered_topics


class TopicTracker:
    """
    Main topic tracking service for interview sessions.
    Maintains topic coverage and provides recommendations.
    """
    
    # Role to topics mapping
    ROLE_TOPICS: Dict[str, List[TopicCategory]] = {
        "Backend Engineer": [
            TopicCategory.DSA, TopicCategory.SYSTEM_DESIGN, TopicCategory.DATABASES,
            TopicCategory.API_DESIGN, TopicCategory.PYTHON, TopicCategory.CONCURRENCY,
            TopicCategory.BEHAVIORAL
        ],
        "Frontend Engineer": [
            TopicCategory.DSA, TopicCategory.JAVASCRIPT, TopicCategory.API_DESIGN,
            TopicCategory.TESTING, TopicCategory.SYSTEM_DESIGN, TopicCategory.BEHAVIORAL
        ],
        "Full Stack Developer": [
            TopicCategory.DSA, TopicCategory.SYSTEM_DESIGN, TopicCategory.DATABASES,
            TopicCategory.API_DESIGN, TopicCategory.JAVASCRIPT, TopicCategory.PYTHON,
            TopicCategory.BEHAVIORAL
        ],
        "DevOps Engineer": [
            TopicCategory.CLOUD, TopicCategory.DEVOPS, TopicCategory.NETWORKING,
            TopicCategory.SECURITY, TopicCategory.OS_CONCEPTS, TopicCategory.BEHAVIORAL
        ],
        "AI/ML Engineer": [
            TopicCategory.ML_AI, TopicCategory.PYTHON, TopicCategory.DSA,
            TopicCategory.SYSTEM_DESIGN, TopicCategory.DATABASES, TopicCategory.BEHAVIORAL
        ],
        "Data Engineer": [
            TopicCategory.DATABASES, TopicCategory.PYTHON, TopicCategory.SYSTEM_DESIGN,
            TopicCategory.CLOUD, TopicCategory.DSA, TopicCategory.BEHAVIORAL
        ],
        "Security Engineer": [
            TopicCategory.SECURITY, TopicCategory.NETWORKING, TopicCategory.OS_CONCEPTS,
            TopicCategory.CLOUD, TopicCategory.DSA, TopicCategory.BEHAVIORAL
        ],
    }
    
    # Default topics for roles not explicitly mapped
    DEFAULT_TOPICS = [
        TopicCategory.DSA, TopicCategory.SYSTEM_DESIGN, TopicCategory.DATABASES,
        TopicCategory.API_DESIGN, TopicCategory.BEHAVIORAL
    ]
    
    def __init__(self):
        self._sessions: Dict[str, TopicCoverage] = {}
    
    def create_coverage(self, session_id: str, role: str) -> TopicCoverage:
        """Create topic coverage tracker for a session."""
        topics = self.ROLE_TOPICS.get(role, self.DEFAULT_TOPICS)
        coverage = TopicCoverage(target_topics=topics)
        self._sessions[session_id] = coverage
        return coverage
    
    def get_coverage(self, session_id: str) -> Optional[TopicCoverage]:
        """Get topic coverage for a session."""
        return self._sessions.get(session_id)
    
    def suggest_next_topic(self, session_id: str) -> Optional[TopicCategory]:
        """Enhanced topic suggestion with balanced coverage."""
        coverage = self.get_coverage(session_id)
        if coverage:
            return coverage.get_balanced_topic_selection()
        return None
    
    def suggest_difficulty(self, session_id: str, category: TopicCategory) -> str:
        """Enhanced difficulty suggestion based on familiarity and performance."""
        coverage = self.get_coverage(session_id)
        if not coverage or category not in coverage.covered_topics:
            return "medium"
        
        score = coverage.covered_topics[category]
        
        # Consider multiple factors for difficulty
        if score.is_strong and score.familiarity_score >= 0.7:
            # Strong performance with high familiarity - increase difficulty
            return "hard"
        elif score.is_weak or score.reinforcement_needed:
            # Weak performance or needs reinforcement - decrease difficulty
            return "easy"
        elif score.familiarity_score >= 0.5:
            # Moderate familiarity - maintain medium
            return "medium"
        else:
            # Low familiarity - start easy
            return "easy"
    
    def get_coverage_balance_report(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed coverage balance analysis for a session."""
        coverage = self.get_coverage(session_id)
        if coverage:
            return coverage.get_coverage_balance_report()
        return None
    
    def get_adaptive_depth_suggestion(self, session_id: str, category: TopicCategory) -> int:
        """Get suggested depth level for adaptive questioning."""
        coverage = self.get_coverage(session_id)
        if coverage:
            return coverage.get_adaptive_depth_suggestion(category)
        return 1  # Default to surface level
    
    def record_detailed_performance(
        self,
        session_id: str,
        category: TopicCategory,
        score: float,
        confidence: Optional[float] = None,
        topic: Optional[str] = None
    ) -> None:
        """Record detailed performance with confidence tracking."""
        coverage = self.get_coverage(session_id)
        if coverage:
            coverage.record_score(category, score, confidence)
    
    def map_topic_to_category(self, topic: str) -> TopicCategory:
        """Map a topic string to a category."""
        topic_lower = topic.lower()
        
        mappings = {
            "python": TopicCategory.PYTHON,
            "javascript": TopicCategory.JAVASCRIPT,
            "js": TopicCategory.JAVASCRIPT,
            "react": TopicCategory.JAVASCRIPT,
            "database": TopicCategory.DATABASES,
            "sql": TopicCategory.DATABASES,
            "nosql": TopicCategory.DATABASES,
            "mongodb": TopicCategory.DATABASES,
            "postgresql": TopicCategory.DATABASES,
            "system design": TopicCategory.SYSTEM_DESIGN,
            "architecture": TopicCategory.SYSTEM_DESIGN,
            "scalability": TopicCategory.SYSTEM_DESIGN,
            "api": TopicCategory.API_DESIGN,
            "rest": TopicCategory.API_DESIGN,
            "graphql": TopicCategory.API_DESIGN,
            "algorithm": TopicCategory.DSA,
            "data structure": TopicCategory.DSA,
            "array": TopicCategory.DSA,
            "tree": TopicCategory.DSA,
            "graph": TopicCategory.DSA,
            "sorting": TopicCategory.DSA,
            "cloud": TopicCategory.CLOUD,
            "aws": TopicCategory.CLOUD,
            "azure": TopicCategory.CLOUD,
            "gcp": TopicCategory.CLOUD,
            "kubernetes": TopicCategory.DEVOPS,
            "docker": TopicCategory.DEVOPS,
            "ci/cd": TopicCategory.DEVOPS,
            "security": TopicCategory.SECURITY,
            "authentication": TopicCategory.SECURITY,
            "encryption": TopicCategory.SECURITY,
            "testing": TopicCategory.TESTING,
            "unit test": TopicCategory.TESTING,
            "behavioral": TopicCategory.BEHAVIORAL,
            "teamwork": TopicCategory.BEHAVIORAL,
            "leadership": TopicCategory.BEHAVIORAL,
            "machine learning": TopicCategory.ML_AI,
            "deep learning": TopicCategory.ML_AI,
            "neural": TopicCategory.ML_AI,
            "ml": TopicCategory.ML_AI,
            "ai": TopicCategory.ML_AI,
            "networking": TopicCategory.NETWORKING,
            "tcp": TopicCategory.NETWORKING,
            "http": TopicCategory.NETWORKING,
            "concurrency": TopicCategory.CONCURRENCY,
            "threading": TopicCategory.CONCURRENCY,
            "async": TopicCategory.CONCURRENCY,
            "parallel": TopicCategory.CONCURRENCY,
            "operating system": TopicCategory.OS_CONCEPTS,
            "process": TopicCategory.OS_CONCEPTS,
            "memory": TopicCategory.OS_CONCEPTS,
        }
        
        for keyword, category in mappings.items():
            if keyword in topic_lower:
                return category
        
        return TopicCategory.DSA  # Default fallback


# Singleton instance
_topic_tracker: Optional[TopicTracker] = None


def get_topic_tracker() -> TopicTracker:
    """Get singleton topic tracker instance."""
    global _topic_tracker
    if _topic_tracker is None:
        _topic_tracker = TopicTracker()
    return _topic_tracker
