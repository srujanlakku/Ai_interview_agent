"""
Skill Gap Analyzer - Maps evaluation scores to concrete skill gaps with actionable recommendations.
Provides detailed analysis of candidate weaknesses and personalized learning paths.
"""
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime

from app.evaluation.enhanced_scorer import SkillCategory, DetailedScore, ConfidenceBand


class GapSeverity(str, Enum):
    """Severity levels for skill gaps."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class LearningPriority(str, Enum):
    """Priority levels for learning recommendations."""
    CRITICAL = "Critical"
    IMPORTANT = "Important"
    HELPFUL = "Helpful"


@dataclass
class GapAnalysis:
    """Comprehensive analysis of identified skill gaps."""
    category: SkillCategory
    severity: GapSeverity
    priority: LearningPriority
    current_mastery: float  # 0-10 scale
    target_mastery: float   # 0-10 scale
    gap_size: float
    impact_on_role: float   # How critical this skill is for the target role
    time_to_improve: str    # Estimated time to close gap
    action_items: List[str] = field(default_factory=list)
    learning_resources: List[Dict[str, str]] = field(default_factory=list)
    practice_exercises: List[str] = field(default_factory=list)
    success_metrics: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "category": self.category.value,
            "severity": self.severity.value,
            "priority": self.priority.value,
            "current_mastery": round(self.current_mastery, 1),
            "target_mastery": round(self.target_mastery, 1),
            "gap_size": round(self.gap_size, 1),
            "impact_on_role": round(self.impact_on_role, 1),
            "time_to_improve": self.time_to_improve,
            "action_items": self.action_items,
            "learning_resources": self.learning_resources,
            "practice_exercises": self.practice_exercises,
            "success_metrics": self.success_metrics,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class LearningPath:
    """Structured learning path for skill development."""
    title: str
    description: str
    duration_weeks: int
    phases: List[Dict[str, Any]] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    outcomes: List[str] = field(default_factory=list)
    resources: List[Dict[str, str]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "title": self.title,
            "description": self.description,
            "duration_weeks": self.duration_weeks,
            "phases": self.phases,
            "prerequisites": self.prerequisites,
            "outcomes": self.outcomes,
            "resources": self.resources
        }


class SkillGapAnalyzer:
    """
    Enterprise-grade skill gap analysis engine.
    
    Features:
    - Detailed gap identification across multiple dimensions
    - Role-specific impact assessment
    - Personalized learning recommendations
    - Structured learning paths
    - Progress tracking metrics
    """
    
    # Role impact weights (how critical each skill is for different roles)
    ROLE_IMPACT_WEIGHTS = {
        "Software Engineer": {
            SkillCategory.DSA: 0.9,
            SkillCategory.SYSTEM_DESIGN: 0.8,
            SkillCategory.DATABASES: 0.7,
            SkillCategory.API_DESIGN: 0.8,
            SkillCategory.TESTING: 0.6,
            SkillCategory.COMMUNICATION: 0.7,
            SkillCategory.PROBLEM_SOLVING: 0.9
        },
        "Backend Developer": {
            SkillCategory.DSA: 0.8,
            SkillCategory.DATABASES: 0.9,
            SkillCategory.API_DESIGN: 0.9,
            SkillCategory.SYSTEM_DESIGN: 0.7,
            SkillCategory.CLOUD: 0.7,
            SkillCategory.SECURITY: 0.6,
            SkillCategory.COMMUNICATION: 0.6
        },
        "Frontend Developer": {
            SkillCategory.JAVASCRIPT: 0.9,
            SkillCategory.API_DESIGN: 0.7,
            SkillCategory.TESTING: 0.7,
            SkillCategory.DSA: 0.6,
            SkillCategory.COMMUNICATION: 0.8,
            SkillCategory.PROBLEM_SOLVING: 0.7
        },
        "Full Stack Developer": {
            SkillCategory.DSA: 0.8,
            SkillCategory.SYSTEM_DESIGN: 0.8,
            SkillCategory.DATABASES: 0.8,
            SkillCategory.API_DESIGN: 0.8,
            SkillCategory.JAVASCRIPT: 0.8,
            SkillCategory.COMMUNICATION: 0.8,
            SkillCategory.PROBLEM_SOLVING: 0.8
        },
        "DevOps Engineer": {
            SkillCategory.CLOUD: 0.9,
            SkillCategory.DEVOPS: 0.9,
            SkillCategory.SECURITY: 0.8,
            SkillCategory.DATABASES: 0.6,
            SkillCategory.NETWORKING: 0.8,
            SkillCategory.COMMUNICATION: 0.7
        }
    }
    
    # Time estimates for improvement (weeks)
    IMPROVEMENT_TIME = {
        GapSeverity.HIGH: "12-16 weeks",
        GapSeverity.MEDIUM: "6-10 weeks", 
        GapSeverity.LOW: "2-4 weeks"
    }
    
    def __init__(self):
        self.analysis_history: List[GapAnalysis] = []
        self.learning_paths: List[LearningPath] = []
    
    def analyze_gaps(
        self,
        evaluation_scores: List[DetailedScore],
        role: str,
        experience_level: str,
        resume_skills: Optional[List[str]] = None
    ) -> List[GapAnalysis]:
        """
        Perform comprehensive skill gap analysis.
        
        Args:
            evaluation_scores: List of detailed evaluation scores
            role: Target role
            experience_level: Experience level (fresher/mid/senior)
            resume_skills: Skills extracted from resume (optional)
            
        Returns:
            List of GapAnalysis objects with detailed recommendations
        """
        if not evaluation_scores:
            return []
        
        # Get role-specific impact weights
        impact_weights = self.ROLE_IMPACT_WEIGHTS.get(
            role, self.ROLE_IMPACT_WEIGHTS["Software Engineer"]
        )
        
        # Calculate average scores across dimensions
        avg_scores = self._calculate_average_scores(evaluation_scores)
        
        # Define target levels based on experience
        target_levels = self._get_target_levels(experience_level)
        
        gaps = []
        
        # Analyze each skill dimension
        for dimension, current_score in avg_scores.items():
            skill_category = self._map_dimension_to_category(dimension)
            target_score = target_levels.get(dimension, 7.0)
            gap_size = target_score - current_score
            
            # Only analyze if there's a meaningful gap
            if gap_size > 0.5:
                impact = impact_weights.get(skill_category, 0.5)
                severity = self._determine_severity(gap_size)
                priority = self._determine_priority(severity, impact)
                
                analysis = GapAnalysis(
                    category=skill_category,
                    severity=severity,
                    priority=priority,
                    current_mastery=current_score,
                    target_mastery=target_score,
                    gap_size=gap_size,
                    impact_on_role=impact,
                    time_to_improve=self.IMPROVEMENT_TIME[severity],
                    action_items=self._generate_action_items(
                        skill_category, severity, current_score
                    ),
                    learning_resources=self._get_learning_resources(
                        skill_category, severity
                    ),
                    practice_exercises=self._get_practice_exercises(
                        skill_category, severity
                    ),
                    success_metrics=self._get_success_metrics(
                        skill_category, severity
                    )
                )
                
                gaps.append(analysis)
        
        # Add resume-based gaps if provided
        if resume_skills:
            resume_gaps = self._analyze_resume_gaps(
                resume_skills, role, experience_level
            )
            gaps.extend(resume_gaps)
        
        # Sort by priority and impact
        gaps.sort(
            key=lambda x: (
                self._priority_rank(x.priority),
                x.impact_on_role,
                x.gap_size
            ),
            reverse=True
        )
        
        self.analysis_history.extend(gaps)
        return gaps
    
    def _calculate_average_scores(
        self,
        scores: List[DetailedScore]
    ) -> Dict[str, float]:
        """Calculate average scores across dimensions."""
        if not scores:
            return {}
        
        correctness_scores = [s.correctness for s in scores]
        depth_scores = [s.depth for s in scores]
        clarity_scores = [s.clarity for s in scores]
        
        return {
            "correctness": sum(correctness_scores) / len(correctness_scores),
            "depth": sum(depth_scores) / len(depth_scores),
            "clarity": sum(clarity_scores) / len(clarity_scores)
        }
    
    def _get_target_levels(self, experience_level: str) -> Dict[str, float]:
        """Get target score levels for different experience levels."""
        targets = {
            "fresher": {"correctness": 6.0, "depth": 5.0, "clarity": 6.0},
            "mid": {"correctness": 7.5, "depth": 6.5, "clarity": 7.0},
            "senior": {"correctness": 8.5, "depth": 8.0, "clarity": 8.0}
        }
        return targets.get(experience_level, targets["mid"])
    
    def _map_dimension_to_category(self, dimension: str) -> SkillCategory:
        """Map evaluation dimension to skill category."""
        mapping = {
            "correctness": SkillCategory.PROBLEM_SOLVING,
            "depth": SkillCategory.SYSTEM_DESIGN,
            "clarity": SkillCategory.COMMUNICATION
        }
        return mapping.get(dimension, SkillCategory.PROBLEM_SOLVING)
    
    def _determine_severity(self, gap_size: float) -> GapSeverity:
        """Determine gap severity based on size."""
        if gap_size >= 3.0:
            return GapSeverity.HIGH
        elif gap_size >= 1.5:
            return GapSeverity.MEDIUM
        else:
            return GapSeverity.LOW
    
    def _determine_priority(
        self,
        severity: GapSeverity,
        impact: float
    ) -> LearningPriority:
        """Determine learning priority based on severity and impact."""
        if severity == GapSeverity.HIGH and impact >= 0.7:
            return LearningPriority.CRITICAL
        elif severity in [GapSeverity.HIGH, GapSeverity.MEDIUM] and impact >= 0.5:
            return LearningPriority.IMPORTANT
        else:
            return LearningPriority.HELPFUL
    
    def _priority_rank(self, priority: LearningPriority) -> int:
        """Convert priority to numeric rank for sorting."""
        ranks = {
            LearningPriority.CRITICAL: 3,
            LearningPriority.IMPORTANT: 2,
            LearningPriority.HELPFUL: 1
        }
        return ranks.get(priority, 0)
    
    def _generate_action_items(
        self,
        category: SkillCategory,
        severity: GapSeverity,
        current_score: float
    ) -> List[str]:
        """Generate specific action items for skill improvement."""
        base_actions = [
            f"Assess current {category.value.lower()} knowledge level",
            "Create structured study plan with timeline",
            "Practice regularly with focused exercises"
        ]
        
        if category == SkillCategory.DSA:
            if severity == GapSeverity.HIGH:
                actions = [
                    "Master fundamental data structures (arrays, linked lists, trees, graphs)",
                    "Solve 50+ LeetCode problems in increasing difficulty",
                    "Study common algorithms (sorting, searching, dynamic programming)",
                    "Practice explaining time/space complexity analysis"
                ]
            elif severity == GapSeverity.MEDIUM:
                actions = [
                    "Review 20-30 medium-difficulty coding problems",
                    "Focus on problem-solving patterns and techniques",
                    "Practice whiteboard-style coding explanations",
                    "Study edge cases and optimization strategies"
                ]
            else:
                actions = [
                    "Solve 10-15 basic coding problems",
                    "Review fundamental concepts and implementations",
                    "Practice clear problem explanation before coding"
                ]
        
        elif category == SkillCategory.SYSTEM_DESIGN:
            if severity == GapSeverity.HIGH:
                actions = [
                    "Study system design fundamentals (scalability, availability, consistency)",
                    "Design 10+ systems from scratch with detailed architecture",
                    "Learn about databases, caching, load balancing, and microservices",
                    "Read case studies from major tech companies"
                ]
            elif severity == GapSeverity.MEDIUM:
                actions = [
                    "Design 5-7 systems focusing on key architectural components",
                    "Study design patterns and best practices",
                    "Practice trade-off analysis and decision making",
                    "Review system design interviews and solutions"
                ]
            else:
                actions = [
                    "Study 3-5 basic system designs",
                    "Focus on understanding key design principles",
                    "Practice explaining design decisions and rationale"
                ]
        
        elif category == SkillCategory.COMMUNICATION:
            if severity == GapSeverity.HIGH:
                actions = [
                    "Practice explaining technical concepts to non-technical audiences",
                    "Record mock interviews and self-evaluate communication style",
                    "Join interview practice groups or find practice partners",
                    "Focus on structured responses using STAR method for behavioral questions"
                ]
            elif severity == GapSeverity.MEDIUM:
                actions = [
                    "Practice clear, concise technical explanations",
                    "Work on reducing filler words and improving fluency",
                    "Structure answers with clear beginning, middle, and end",
                    "Get feedback from peers or mentors on communication style"
                ]
            else:
                actions = [
                    "Practice speaking clearly and confidently about technical topics",
                    "Focus on organizing thoughts before responding",
                    "Work on active listening and clarifying questions"
                ]
        
        else:
            actions = [
                f"Study {category.value} fundamentals and best practices",
                f"Practice {category.value.lower()} concepts through hands-on exercises",
                f"Review common {category.value.lower()} interview questions and solutions"
            ]
        
        return base_actions + actions
    
    def _get_learning_resources(
        self,
        category: SkillCategory,
        severity: GapSeverity
    ) -> List[Dict[str, str]]:
        """Get recommended learning resources."""
        resources = {
            SkillCategory.DSA: [
                {"title": "LeetCode", "url": "https://leetcode.com", "type": "Practice"},
                {"title": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org", "type": "Theory"},
                {"title": "Cracking the Coding Interview", "url": "https://www.amazon.com/Cracking-Coding-Interview-Programming-Questions/dp/0984782850", "type": "Book"},
                {"title": "AlgoExpert", "url": "https://www.algoexpert.io", "type": "Course"}
            ],
            SkillCategory.SYSTEM_DESIGN: [
                {"title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer", "type": "Guide"},
                {"title": "Designing Data-Intensive Applications", "url": "https://dataintensive.net", "type": "Book"},
                {"title": "Grokking System Design Interview", "url": "https://www.educative.io/courses/grokking-the-system-design-interview", "type": "Course"},
                {"title": "High Scalability Blog", "url": "http://highscalability.com", "type": "Blog"}
            ],
            SkillCategory.COMMUNICATION: [
                {"title": "Toastmasters International", "url": "https://www.toastmasters.org", "type": "Practice"},
                {"title": "Interviewing.io", "url": "https://interviewing.io", "type": "Practice"},
                {"title": "Pramp", "url": "https://www.pramp.com", "type": "Practice"},
                {"title": "YouTube: TechLead Interview Tips", "url": "https://www.youtube.com", "type": "Video"}
            ]
        }
        
        category_resources = resources.get(category, [
            {"title": "General technical resources", "url": "https://github.com", "type": "Repository"},
            {"title": "Online courses", "url": "https://coursera.org", "type": "Course"},
            {"title": "Technical documentation", "url": "https://developer.mozilla.org", "type": "Documentation"}
        ])
        
        # Return more resources for higher severity gaps
        if severity == GapSeverity.HIGH:
            return category_resources
        elif severity == GapSeverity.MEDIUM:
            return category_resources[:3]
        else:
            return category_resources[:2]
    
    def _get_practice_exercises(
        self,
        category: SkillCategory,
        severity: GapSeverity
    ) -> List[str]:
        """Get specific practice exercises."""
        exercises = {
            SkillCategory.DSA: [
                "Solve 10 array/string manipulation problems",
                "Implement 5 tree traversal algorithms from scratch",
                "Design and implement a hash table",
                "Solve 3 dynamic programming problems",
                "Practice explaining your approach before coding"
            ],
            SkillCategory.SYSTEM_DESIGN: [
                "Design a URL shortening service",
                "Design a chat application architecture",
                "Design a distributed cache system",
                "Create API design for a social media platform",
                "Practice explaining design trade-offs"
            ],
            SkillCategory.COMMUNICATION: [
                "Explain a technical concept to a non-technical person",
                "Record yourself answering common interview questions",
                "Practice the STAR method for behavioral questions",
                "Get feedback on your explanation clarity",
                "Work on reducing filler words and pauses"
            ]
        }
        
        category_exercises = exercises.get(category, [
            f"Practice {category.value.lower()} fundamentals",
            f"Review {category.value.lower()} best practices",
            f"Apply {category.value.lower()} concepts in mock scenarios"
        ])
        
        # Return appropriate number based on severity
        if severity == GapSeverity.HIGH:
            return category_exercises
        elif severity == GapSeverity.MEDIUM:
            return category_exercises[:3]
        else:
            return category_exercises[:2]
    
    def _get_success_metrics(
        self,
        category: SkillCategory,
        severity: GapSeverity
    ) -> List[str]:
        """Define success metrics for skill improvement."""
        base_metrics = [
            "Consistent performance in practice sessions",
            "Clear explanation of concepts and solutions",
            "Confidence in discussing the topic"
        ]
        
        if category == SkillCategory.DSA:
            metrics = [
                "Solve 80% of practice problems correctly",
                "Explain time/space complexity accurately",
                "Handle edge cases appropriately",
                "Optimize solutions when possible"
            ]
        elif category == SkillCategory.SYSTEM_DESIGN:
            metrics = [
                "Design systems with clear architectural components",
                "Explain design decisions and trade-offs",
                "Consider scalability and reliability requirements",
                "Address potential failure scenarios"
            ]
        elif category == SkillCategory.COMMUNICATION:
            metrics = [
                "Speak clearly without excessive filler words",
                "Structure responses logically",
                "Listen actively and ask clarifying questions",
                "Adapt explanation style to audience"
            ]
        else:
            metrics = [
                f"Demonstrate solid {category.value.lower()} knowledge",
                f"Apply {category.value.lower()} concepts effectively",
                f"Explain {category.value.lower()} principles clearly"
            ]
        
        return base_metrics + metrics
    
    def _analyze_resume_gaps(
        self,
        resume_skills: List[str],
        role: str,
        experience_level: str
    ) -> List[GapAnalysis]:
        """Analyze gaps based on resume skills vs role requirements."""
        # This would typically compare resume skills with role requirements
        # For now, we'll create placeholder gaps for demonstration
        gaps = []
        
        # Example: If resume lacks certain key skills for the role
        required_skills = self._get_required_skills(role, experience_level)
        missing_skills = [skill for skill in required_skills if skill not in resume_skills]
        
        for skill in missing_skills[:3]:  # Limit to top 3 missing skills
            gap = GapAnalysis(
                category=self._skill_to_category(skill),
                severity=GapSeverity.MEDIUM,
                priority=LearningPriority.IMPORTANT,
                current_mastery=2.0,  # Low since not on resume
                target_mastery=7.0,   # Standard target
                gap_size=5.0,
                impact_on_role=0.8,
                time_to_improve="8-12 weeks",
                action_items=[
                    f"Learn fundamentals of {skill}",
                    f"Practice {skill.lower()} concepts",
                    f"Build projects using {skill}",
                    f"Prepare for {skill}-related interview questions"
                ],
                learning_resources=[
                    {"title": f"{skill} documentation", "url": f"https://{skill.lower()}.org", "type": "Documentation"},
                    {"title": f"{skill} online courses", "url": "https://coursera.org", "type": "Course"}
                ],
                practice_exercises=[
                    f"Complete {skill} tutorials",
                    f"Build small {skill} projects",
                    f"Practice {skill} interview questions"
                ],
                success_metrics=[
                    f"Proficiency in basic {skill} concepts",
                    f"Ability to discuss {skill} in interviews",
                    f"Confidence applying {skill} principles"
                ]
            )
            gaps.append(gap)
        
        return gaps
    
    def _get_required_skills(self, role: str, experience_level: str) -> List[str]:
        """Get required skills for a role and experience level."""
        # Simplified skill requirements
        requirements = {
            "Software Engineer": ["Python", "JavaScript", "SQL", "Git", "Testing"],
            "Backend Developer": ["Python", "Java", "SQL", "REST APIs", "Docker"],
            "Frontend Developer": ["JavaScript", "React", "CSS", "HTML", "TypeScript"],
            "Full Stack Developer": ["Python", "JavaScript", "React", "SQL", "Node.js"],
            "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"]
        }
        return requirements.get(role, ["Programming", "Problem Solving", "Communication"])
    
    def _skill_to_category(self, skill: str) -> SkillCategory:
        """Map a skill name to a skill category."""
        skill_mapping = {
            "Python": SkillCategory.PYTHON,
            "JavaScript": SkillCategory.JAVASCRIPT,
            "SQL": SkillCategory.DATABASES,
            "Docker": SkillCategory.DEVOPS,
            "Kubernetes": SkillCategory.DEVOPS,
            "AWS": SkillCategory.CLOUD,
            "React": SkillCategory.JAVASCRIPT,
            "Git": SkillCategory.DEVOPS,
            "Testing": SkillCategory.TESTING,
            "REST APIs": SkillCategory.API_DESIGN,
            "Node.js": SkillCategory.JAVASCRIPT,
            "Linux": SkillCategory.OPERATING_SYSTEMS,
            "Programming": SkillCategory.PROBLEM_SOLVING,
            "Problem Solving": SkillCategory.PROBLEM_SOLVING,
            "Communication": SkillCategory.COMMUNICATION
        }
        return skill_mapping.get(skill, SkillCategory.PROBLEM_SOLVING)
    
    def generate_learning_path(
        self,
        gaps: List[GapAnalysis],
        available_time_weeks: int = 12
    ) -> LearningPath:
        """
        Generate a personalized learning path based on identified gaps.
        
        Args:
            gaps: List of identified skill gaps
            available_time_weeks: Total available time for learning
            
        Returns:
            Structured learning path
        """
        if not gaps:
            return LearningPath(
                title="Maintain Current Skills",
                description="Continue practicing and stay current with technology trends",
                duration_weeks=4,
                outcomes=["Maintain proficiency in core areas", "Stay updated with industry trends"]
            )
        
        # Sort gaps by priority
        critical_gaps = [g for g in gaps if g.priority == LearningPriority.CRITICAL]
        important_gaps = [g for g in gaps if g.priority == LearningPriority.IMPORTANT]
        
        # Create learning phases
        phases = []
        weeks_allocated = 0
        
        # Phase 1: Critical gaps (if any)
        if critical_gaps:
            phase_duration = min(4, available_time_weeks - weeks_allocated)
            if phase_duration > 0:
                phases.append({
                    "name": "Critical Skills Foundation",
                    "duration_weeks": phase_duration,
                    "focus_areas": [g.category.value for g in critical_gaps],
                    "objectives": [f"Address {len(critical_gaps)} critical skill gaps"],
                    "activities": [
                        "Intensive study of critical areas",
                        "Daily practice focused on weak areas",
                        "Weekly assessment of progress"
                    ]
                })
                weeks_allocated += phase_duration
        
        # Phase 2: Important gaps
        if important_gaps and weeks_allocated < available_time_weeks:
            remaining_weeks = available_time_weeks - weeks_allocated
            phase_duration = min(6, remaining_weeks)
            if phase_duration > 0:
                phases.append({
                    "name": "Core Skills Development",
                    "duration_weeks": phase_duration,
                    "focus_areas": [g.category.value for g in important_gaps],
                    "objectives": [f"Improve {len(important_gaps)} important skill areas"],
                    "activities": [
                        "Structured learning of core competencies",
                        "Regular practice and application",
                        "Progress tracking and adjustment"
                    ]
                })
                weeks_allocated += phase_duration
        
        # Phase 3: Review and integration
        if weeks_allocated < available_time_weeks:
            review_weeks = available_time_weeks - weeks_allocated
            phases.append({
                "name": "Integration and Review",
                "duration_weeks": review_weeks,
                "focus_areas": ["All previously studied areas"],
                "objectives": ["Consolidate learning", "Practice integrated application"],
                "activities": [
                    "Comprehensive review of all topics",
                    "Mock interviews and practical application",
                    "Final assessment and preparation"
                ]
            })
        
        # Compile resources from all gaps
        all_resources = []
        for gap in gaps:
            all_resources.extend(gap.learning_resources)
        
        # Remove duplicates
        unique_resources = []
        seen_urls = set()
        for resource in all_resources:
            if resource["url"] not in seen_urls:
                unique_resources.append(resource)
                seen_urls.add(resource["url"])
        
        learning_path = LearningPath(
            title=f"Personalized {available_time_weeks}-Week Learning Path",
            description=f"Targeted skill development plan based on interview performance analysis",
            duration_weeks=available_time_weeks,
            phases=phases,
            prerequisites=["Basic programming knowledge", "Willingness to practice consistently"],
            outcomes=[
                "Addressed critical skill gaps",
                "Improved overall interview readiness",
                "Confidence in technical discussions",
                "Structured approach to continuous learning"
            ],
            resources=unique_resources
        )
        
        self.learning_paths.append(learning_path)
        return learning_path
    
    def get_summary_report(self) -> Dict[str, Any]:
        """Generate summary report of all analyses."""
        if not self.analysis_history:
            return {"message": "No gap analysis performed yet"}
        
        # Group by severity and priority
        severity_counts = {}
        priority_counts = {}
        
        for analysis in self.analysis_history:
            severity_counts[analysis.severity.value] = severity_counts.get(analysis.severity.value, 0) + 1
            priority_counts[analysis.priority.value] = priority_counts.get(analysis.priority.value, 0) + 1
        
        # Get top categories
        category_impacts = {}
        for analysis in self.analysis_history:
            category_impacts[analysis.category.value] = category_impacts.get(analysis.category.value, 0) + (
                analysis.impact_on_role * analysis.gap_size
            )
        
        top_categories = sorted(
            category_impacts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "total_analyses": len(self.analysis_history),
            "severity_distribution": severity_counts,
            "priority_distribution": priority_counts,
            "top_impact_categories": [
                {"category": cat, "impact_score": round(score, 2)}
                for cat, score in top_categories
            ],
            "recommended_focus": self._get_recommended_focus(),
            "learning_paths_created": len(self.learning_paths)
        }
    
    def _get_recommended_focus(self) -> str:
        """Get overall recommendation for focus areas."""
        critical_gaps = [g for g in self.analysis_history if g.priority == LearningPriority.CRITICAL]
        high_impact_gaps = [g for g in self.analysis_history if g.impact_on_role >= 0.8]
        
        if critical_gaps:
            categories = [g.category.value for g in critical_gaps]
            return f"Focus primarily on: {', '.join(categories[:2])}"
        elif high_impact_gaps:
            categories = [g.category.value for g in high_impact_gaps]
            return f"Prioritize: {', '.join(categories[:3])}"
        else:
            return "Maintain current strengths while gradually improving all areas"