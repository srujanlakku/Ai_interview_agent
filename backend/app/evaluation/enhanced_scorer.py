"""
Enhanced Scorer - Enterprise-grade evaluation with explainable scoring and confidence bands.
Provides structured evaluation with correctness, depth, and clarity scores.
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime


class ConfidenceBand(str, Enum):
    """Confidence level for evaluation scores."""
    STRONG = "Strong"
    MEDIUM = "Medium" 
    WEAK = "Weak"


class SkillCategory(str, Enum):
    """Technical skill categories for gap analysis."""
    DSA = "Data Structures & Algorithms"
    SYSTEM_DESIGN = "System Design"
    DATABASES = "Databases"
    NETWORKING = "Networking"
    OPERATING_SYSTEMS = "Operating Systems"
    SECURITY = "Security"
    CLOUD = "Cloud Computing"
    DEVOPS = "DevOps"
    TESTING = "Testing"
    CONCURRENCY = "Concurrency"
    API_DESIGN = "API Design"
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    COMMUNICATION = "Communication"
    PROBLEM_SOLVING = "Problem Solving"


@dataclass
class DetailedScore:
    """Structured score with detailed breakdown."""
    correctness: float = 0.0  # 0-10 scale
    depth: float = 0.0        # 0-10 scale  
    clarity: float = 0.0      # 0-10 scale
    overall: float = 0.0      # Calculated overall score
    confidence_band: ConfidenceBand = ConfidenceBand.MEDIUM
    explanation: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    def calculate_overall(self) -> float:
        """Calculate weighted overall score."""
        weights = {
            "correctness": 0.5,
            "depth": 0.3,
            "clarity": 0.2
        }
        return (
            self.correctness * weights["correctness"] +
            self.depth * weights["depth"] +
            self.clarity * weights["clarity"]
        )
    
    def determine_confidence_band(self) -> ConfidenceBand:
        """Determine confidence band based on score consistency."""
        scores = [self.correctness, self.depth, self.clarity]
        avg_score = sum(scores) / len(scores)
        score_variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
        
        if avg_score >= 8.0 and score_variance <= 1.0:
            return ConfidenceBand.STRONG
        elif avg_score >= 5.0 and score_variance <= 2.0:
            return ConfidenceBand.MEDIUM
        else:
            return ConfidenceBand.WEAK
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "correctness": round(self.correctness, 1),
            "depth": round(self.depth, 1),
            "clarity": round(self.clarity, 1),
            "overall": round(self.overall, 1),
            "confidence_band": self.confidence_band.value,
            "explanation": self.explanation,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class SkillGap:
    """Represents a skill gap identified in evaluation."""
    category: SkillCategory
    severity: str  # High, Medium, Low
    current_level: float  # 0-10
    target_level: float   # 0-10
    gap_size: float       # target - current
    recommendations: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "category": self.category.value,
            "severity": self.severity,
            "current_level": round(self.current_level, 1),
            "target_level": round(self.target_level, 1),
            "gap_size": round(self.gap_size, 1),
            "recommendations": self.recommendations,
            "resources": self.resources
        }


class EnhancedScorer:
    """
    Enterprise-grade scoring engine with explainable evaluation.
    
    Features:
    - Structured 3-dimensional scoring (correctness, depth, clarity)
    - Confidence band calculation
    - Skill gap identification
    - Learning recommendation generation
    """
    
    # Scoring thresholds
    SCORE_THRESHOLDS = {
        "excellent": 8.5,
        "good": 7.0,
        "average": 5.5,
        "poor": 4.0
    }
    
    # Skill gap severity thresholds
    GAP_THRESHOLDS = {
        "high": 4.0,    # Gap of 4+ points
        "medium": 2.0,  # Gap of 2-4 points
        "low": 0.1      # Gap of 0.1-2 points
    }
    
    def __init__(self):
        self.evaluation_history: List[DetailedScore] = []
        self.skill_gaps: List[SkillGap] = []
    
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        question_category: str,
        evaluation_data: Dict[str, Any]
    ) -> DetailedScore:
        """
        Create detailed evaluation from raw evaluation data.
        
        Args:
            question: The interview question
            answer: Candidate's answer
            question_category: Category of the question
            evaluation_data: Raw evaluation from LLM
            
        Returns:
            DetailedScore with structured breakdown
        """
        # Extract scores from evaluation data
        correctness = evaluation_data.get("correctness_score", 5.0)
        depth = evaluation_data.get("depth_score", 5.0)
        clarity = evaluation_data.get("clarity_score", 5.0)
        explanation = evaluation_data.get("explanation", "No explanation provided")
        
        # Create detailed score
        score = DetailedScore(
            correctness=correctness,
            depth=depth,
            clarity=clarity,
            explanation=explanation
        )
        
        # Calculate overall score and confidence band
        score.overall = score.calculate_overall()
        score.confidence_band = score.determine_confidence_band()
        
        # Add to history
        self.evaluation_history.append(score)
        
        return score
    
    def identify_skill_gaps(
        self,
        scores_history: List[DetailedScore],
        role: str,
        experience_level: str
    ) -> List[SkillGap]:
        """
        Identify skill gaps based on evaluation history.
        
        Args:
            scores_history: List of detailed scores
            role: Target role
            experience_level: Experience level
            
        Returns:
            List of identified skill gaps
        """
        if not scores_history:
            return []
        
        # Group scores by dimension
        correctness_scores = [s.correctness for s in scores_history]
        depth_scores = [s.depth for s in scores_history]
        clarity_scores = [s.clarity for s in scores_history]
        
        # Calculate averages
        avg_correctness = sum(correctness_scores) / len(correctness_scores)
        avg_depth = sum(depth_scores) / len(depth_scores)
        avg_clarity = sum(clarity_scores) / len(clarity_scores)
        
        # Define target levels based on role and experience
        target_levels = self._get_target_levels(role, experience_level)
        
        gaps = []
        
        # Check each dimension for gaps
        dimensions = [
            ("correctness", avg_correctness, SkillCategory.PROBLEM_SOLVING),
            ("depth", avg_depth, SkillCategory.SYSTEM_DESIGN),
            ("clarity", avg_clarity, SkillCategory.COMMUNICATION)
        ]
        
        for dimension_name, current_score, skill_category in dimensions:
            target_score = target_levels.get(dimension_name, 7.0)
            gap_size = target_score - current_score
            
            if gap_size > self.GAP_THRESHOLDS["low"]:
                severity = self._determine_gap_severity(gap_size)
                gap = SkillGap(
                    category=skill_category,
                    severity=severity,
                    current_level=current_score,
                    target_level=target_score,
                    gap_size=gap_size,
                    recommendations=self._generate_recommendations(
                        skill_category, severity, current_score
                    ),
                    resources=self._get_learning_resources(skill_category)
                )
                gaps.append(gap)
        
        self.skill_gaps = gaps
        return gaps
    
    def _get_target_levels(self, role: str, experience_level: str) -> Dict[str, float]:
        """Get target score levels based on role and experience."""
        base_targets = {
            "fresher": {"correctness": 6.0, "depth": 5.0, "clarity": 6.0},
            "mid": {"correctness": 7.5, "depth": 6.5, "clarity": 7.0},
            "senior": {"correctness": 8.5, "depth": 8.0, "clarity": 8.0}
        }
        
        return base_targets.get(experience_level, base_targets["mid"])
    
    def _determine_gap_severity(self, gap_size: float) -> str:
        """Determine severity level of a skill gap."""
        if gap_size >= self.GAP_THRESHOLDS["high"]:
            return "High"
        elif gap_size >= self.GAP_THRESHOLDS["medium"]:
            return "Medium"
        else:
            return "Low"
    
    def _generate_recommendations(
        self,
        category: SkillCategory,
        severity: str,
        current_level: float
    ) -> List[str]:
        """Generate learning recommendations for a skill gap."""
        recommendations = []
        
        if category == SkillCategory.PROBLEM_SOLVING:
            if severity == "High":
                recommendations.extend([
                    "Practice 50+ coding problems on LeetCode/HackerRank",
                    "Focus on fundamental algorithms and data structures",
                    "Review time/space complexity analysis",
                    "Practice explaining your approach before coding"
                ])
            elif severity == "Medium":
                recommendations.extend([
                    "Solve 20-30 medium-difficulty problems",
                    "Study common problem patterns and techniques",
                    "Practice whiteboard-style explanations",
                    "Review solutions and optimize approaches"
                ])
            else:
                recommendations.extend([
                    "Solve 10-15 easy problems to build confidence",
                    "Focus on clear problem understanding",
                    "Practice basic algorithm implementation"
                ])
        
        elif category == SkillCategory.SYSTEM_DESIGN:
            if severity == "High":
                recommendations.extend([
                    "Study system design fundamentals (scalability, availability)",
                    "Practice designing 10+ systems from scratch",
                    "Learn about databases, caching, and load balancing",
                    "Read design case studies from major tech companies"
                ])
            elif severity == "Medium":
                recommendations.extend([
                    "Design 5-7 systems with focus on key components",
                    "Study architectural patterns and best practices",
                    "Practice trade-off analysis and decision making",
                    "Review system design interviews on YouTube"
                ])
            else:
                recommendations.extend([
                    "Study 3-5 basic system designs",
                    "Focus on understanding key design principles",
                    "Practice explaining design decisions"
                ])
        
        elif category == SkillCategory.COMMUNICATION:
            if severity == "High":
                recommendations.extend([
                    "Practice explaining technical concepts to non-technical people",
                    "Record yourself answering questions and review",
                    "Join mock interview groups or find interview partners",
                    "Focus on structured responses (STAR method for behavioral)"
                ])
            elif severity == "Medium":
                recommendations.extend([
                    "Practice clear, concise explanations",
                    "Work on reducing filler words and pauses",
                    "Structure answers with clear beginning, middle, end",
                    "Get feedback from peers or mentors"
                ])
            else:
                recommendations.extend([
                    "Practice speaking clearly and confidently",
                    "Focus on organizing thoughts before responding",
                    "Work on active listening skills"
                ])
        
        return recommendations
    
    def _get_learning_resources(self, category: SkillCategory) -> List[str]:
        """Get recommended learning resources for a skill category."""
        resources = {
            SkillCategory.DSA: [
                "https://leetcode.com",
                "https://www.geeksforgeeks.org",
                "https://algoexpert.io",
                "Cracking the Coding Interview book"
            ],
            SkillCategory.SYSTEM_DESIGN: [
                "https://www.systemdesignprimer.com",
                "https://github.com/donnemartin/system-design-primer",
                "Designing Data-Intensive Applications book",
                "Grokking System Design Interview course"
            ],
            SkillCategory.DATABASES: [
                "https://www.postgresql.org/docs/",
                "https://redis.io/documentation",
                "Database Internals book",
                "MongoDB University courses"
            ],
            SkillCategory.COMMUNICATION: [
                "Toastmasters International",
                "Cracking the Coding Interview communication section",
                "YouTube: TechLead interview tips",
                "Pramp for mock interviews"
            ]
        }
        
        return resources.get(category, [
            "General technical interview preparation resources",
            "Online courses relevant to your target role",
            "Technical blogs and documentation"
        ])
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        if not self.evaluation_history:
            return {}
        
        scores = self.evaluation_history
        avg_correctness = sum(s.correctness for s in scores) / len(scores)
        avg_depth = sum(s.depth for s in scores) / len(scores)
        avg_clarity = sum(s.clarity for s in scores) / len(scores)
        avg_overall = sum(s.overall for s in scores) / len(scores)
        
        # Confidence band distribution
        band_counts = {}
        for score in scores:
            band = score.confidence_band.value
            band_counts[band] = band_counts.get(band, 0) + 1
        
        return {
            "total_evaluations": len(scores),
            "average_scores": {
                "correctness": round(avg_correctness, 1),
                "depth": round(avg_depth, 1),
                "clarity": round(avg_clarity, 1),
                "overall": round(avg_overall, 1)
            },
            "confidence_distribution": band_counts,
            "skill_gaps": [gap.to_dict() for gap in self.skill_gaps],
            "readiness_level": self._get_readiness_level(avg_overall)
        }
    
    def _get_readiness_level(self, avg_score: float) -> str:
        """Get readiness level description."""
        if avg_score >= self.SCORE_THRESHOLDS["excellent"]:
            return "Interview Ready - Exceptional preparation"
        elif avg_score >= self.SCORE_THRESHOLDS["good"]:
            return "Well Prepared - Minor refinements needed"
        elif avg_score >= self.SCORE_THRESHOLDS["average"]:
            return "Making Progress - Continue practicing fundamentals"
        elif avg_score >= self.SCORE_THRESHOLDS["poor"]:
            return "Keep Practicing - Focus on core concepts"
        else:
            return "Focus Required - Dedicated preparation needed"