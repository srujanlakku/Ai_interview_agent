"""
Root-Cause Failure Analysis Engine
Analyzes interview performance to identify exact reasons for weak/failing performance
and provides clear, actionable improvement guidance.
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json


class FailurePattern(Enum):
    """Common failure patterns identified in interviews"""
    CONCEPTUAL_GAP = "conceptual_gap"
    STRUCTURE_POOR = "structure_poor"
    COMMUNICATION_WEAK = "communication_weak"
    CONFIDENCE_LOW = "confidence_low"
    OVER_EXPLAINING = "over_explaining"
    PANIC_RESPONSE = "panic_response"
    MEMORY_LAPSE = "memory_lapse"
    TIME_MANAGEMENT = "time_management"


class SeverityLevel(Enum):
    """Severity levels for identified issues"""
    HIGH = "high"      # Critical issue requiring immediate attention
    MEDIUM = "medium"  # Important issue affecting performance
    LOW = "low"        # Minor issue with minimal impact


@dataclass
class RootCause:
    """Identified root cause of performance issue"""
    pattern: FailurePattern
    severity: SeverityLevel
    description: str
    evidence: List[str]
    impact_on_score: float  # 0-10 scale
    primary_indicator: bool = False  # Whether this is the main issue to fix


@dataclass
class CauseChain:
    """Chain of causes leading to poor performance"""
    primary_cause: RootCause
    contributing_factors: List[RootCause]
    cascade_effects: List[str]


@dataclass
class ActionableRecommendation:
    """Specific, actionable recommendation"""
    priority: int  # 1 = highest priority
    action: str
    timeframe: str  # e.g., "immediate", "within 1 week", "ongoing"
    resources: List[str]
    success_metrics: List[str]


@dataclass
class FailureAnalysis:
    """Complete failure analysis for an interview or question"""
    session_id: str
    question_id: Optional[str]
    overall_score: float
    failure_patterns: List[RootCause]
    primary_issue: RootCause
    cause_chain: CauseChain
    recommendations: List[ActionableRecommendation]
    confidence_level: float  # 0-1 confidence in analysis
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "question_id": self.question_id,
            "overall_score": self.overall_score,
            "failure_patterns": [asdict(pattern) for pattern in self.failure_patterns],
            "primary_issue": asdict(self.primary_issue),
            "cause_chain": {
                "primary_cause": asdict(self.cause_chain.primary_cause),
                "contributing_factors": [asdict(factor) for factor in self.cause_chain.contributing_factors],
                "cascade_effects": self.cause_chain.cascade_effects
            },
            "recommendations": [asdict(rec) for rec in self.recommendations],
            "confidence_level": self.confidence_level
        }


class FailureAnalysisEngine:
    """
    Analyzes interview failures to identify root causes and provide clear guidance.
    
    Features:
    - Pattern recognition for common failure modes
    - Cause-effect chain analysis
    - Priority-based improvement recommendations
    - Confidence scoring for analysis reliability
    """
    
    # Thresholds for identifying failure patterns
    SCORE_THRESHOLDS = {
        "failure": 4.0,      # Below this is considered failing
        "borderline": 6.0,   # Between 4-6 is borderline
        "pass": 7.0          # Above 7 is passing
    }
    
    # Pattern detection weights
    PATTERN_WEIGHTS = {
        FailurePattern.CONCEPTUAL_GAP: 0.30,
        FailurePattern.STRUCTURE_POOR: 0.25,
        FailurePattern.COMMUNICATION_WEAK: 0.20,
        FailurePattern.CONFIDENCE_LOW: 0.15,
        FailurePattern.OVER_EXPLAINING: 0.05,
        FailurePattern.PANIC_RESPONSE: 0.03,
        FailurePattern.MEMORY_LAPSE: 0.01,
        FailurePattern.TIME_MANAGEMENT: 0.01
    }
    
    def __init__(self):
        self.analysis_history: List[FailureAnalysis] = []
    
    def analyze_performance(
        self,
        session_id: str,
        question_id: Optional[str],
        score: float,
        evaluation_data: Dict[str, Any],
        answer_text: str,
        context: Dict[str, Any] = None
    ) -> FailureAnalysis:
        """
        Analyze interview performance and identify root causes of failure.
        
        Args:
            session_id: Interview session identifier
            question_id: Specific question identifier (optional)
            score: Overall score (0-10)
            evaluation_data: Detailed evaluation from evaluation agent
            answer_text: Candidate's actual answer
            context: Additional context (previous scores, timing, etc.)
            
        Returns:
            Complete failure analysis with root causes and recommendations
        """
        # Detect failure patterns
        patterns = self._detect_failure_patterns(
            score, evaluation_data, answer_text, context or {}
        )
        
        # Identify primary issue
        primary_issue = self._identify_primary_issue(patterns, score)
        
        # Build cause chain
        cause_chain = self._build_cause_chain(primary_issue, patterns)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(primary_issue, patterns, score)
        
        # Calculate confidence
        confidence = self._calculate_analysis_confidence(patterns, evaluation_data)
        
        analysis = FailureAnalysis(
            session_id=session_id,
            question_id=question_id,
            overall_score=score,
            failure_patterns=patterns,
            primary_issue=primary_issue,
            cause_chain=cause_chain,
            recommendations=recommendations,
            confidence_level=confidence
        )
        
        self.analysis_history.append(analysis)
        return analysis
    
    def _detect_failure_patterns(
        self,
        score: float,
        evaluation_data: Dict[str, Any],
        answer_text: str,
        context: Dict[str, Any]
    ) -> List[RootCause]:
        """Detect various failure patterns from evaluation data."""
        patterns = []
        
        # Conceptual Gap Detection
        if self._detect_conceptual_gap(evaluation_data, score):
            patterns.append(RootCause(
                pattern=FailurePattern.CONCEPTUAL_GAP,
                severity=self._assess_severity(score, 0.3),
                description="Fundamental misunderstanding of core concepts",
                evidence=self._extract_evidence(evaluation_data, "missing_concepts", "incorrect_facts"),
                impact_on_score=3.5,
                primary_indicator=(score <= 3.0)
            ))
        
        # Structure/Poor Organization Detection
        if self._detect_structure_issues(evaluation_data, answer_text):
            patterns.append(RootCause(
                pattern=FailurePattern.STRUCTURE_POOR,
                severity=self._assess_severity(score, 0.25),
                description="Poor answer organization and flow",
                evidence=self._extract_evidence(evaluation_data, "structure_issues", "organization_problems"),
                impact_on_score=2.0,
                primary_indicator=("structure" in str(evaluation_data.get("weaknesses", [])).lower())
            ))
        
        # Communication Issues Detection
        if self._detect_communication_issues(evaluation_data, score):
            patterns.append(RootCause(
                pattern=FailurePattern.COMMUNICATION_WEAK,
                severity=self._assess_severity(score, 0.2),
                description="Unclear or confusing explanation",
                evidence=self._extract_evidence(evaluation_data, "clarity_issues", "communication_problems"),
                impact_on_score=2.5,
                primary_indicator=(evaluation_data.get("clarity_score", 10) <= 4.0)
            ))
        
        # Confidence/Low Detection
        if self._detect_confidence_issues(evaluation_data, context):
            patterns.append(RootCause(
                pattern=FailurePattern.CONFIDENCE_LOW,
                severity=self._assess_severity(score, 0.15),
                description="Low confidence affecting performance",
                evidence=self._extract_evidence(context, "hesitation_indicators", "confidence_signals"),
                impact_on_score=1.5,
                primary_indicator=context.get("confidence_level", 1.0) < 0.4
            ))
        
        # Over-explaining Detection
        if self._detect_over_explaining(answer_text, evaluation_data):
            patterns.append(RootCause(
                pattern=FailurePattern.OVER_EXPLAINING,
                severity=SeverityLevel.LOW,
                description="Providing too much unnecessary detail",
                evidence=["Answer length exceeds typical response by 2x+", "Including irrelevant information"],
                impact_on_score=0.5,
                primary_indicator=False
            ))
        
        # Panic Response Detection
        if self._detect_panic_response(answer_text, context):
            patterns.append(RootCause(
                pattern=FailurePattern.PANIC_RESPONSE,
                severity=self._assess_severity(score, 0.03),
                description="Panic-induced poor response quality",
                evidence=["Incoherent response structure", "Fundamental errors in basic concepts"],
                impact_on_score=3.0,
                primary_indicator=(score <= 2.0 and len(answer_text.split()) < 20)
            ))
        
        return patterns
    
    def _identify_primary_issue(self, patterns: List[RootCause], score: float) -> RootCause:
        """Identify the single most critical issue to address first."""
        if not patterns:
            # If no clear patterns, create a general weakness indicator
            return RootCause(
                pattern=FailurePattern.CONCEPTUAL_GAP,
                severity=SeverityLevel.MEDIUM,
                description="General knowledge gaps requiring comprehensive review",
                evidence=["Overall score indicates fundamental understanding issues"],
                impact_on_score=4.0,
                primary_indicator=True
            )
        
        # Sort by impact and severity
        sorted_patterns = sorted(
            patterns, 
            key=lambda p: (p.severity.value, p.impact_on_score), 
            reverse=True
        )
        
        # Mark the highest impact as primary
        primary = sorted_patterns[0]
        primary.primary_indicator = True
        return primary
    
    def _build_cause_chain(self, primary: RootCause, all_patterns: List[RootCause]) -> CauseChain:
        """Build the causal chain showing how issues connect."""
        contributing = [p for p in all_patterns if p != primary and p.severity != SeverityLevel.LOW]
        
        # Define cascade effects based on primary cause
        cascade_effects = self._determine_cascade_effects(primary.pattern)
        
        return CauseChain(
            primary_cause=primary,
            contributing_factors=contributing,
            cascade_effects=cascade_effects
        )
    
    def _generate_recommendations(
        self, 
        primary_issue: RootCause, 
        patterns: List[RootCause], 
        score: float
    ) -> List[ActionableRecommendation]:
        """Generate prioritized, actionable recommendations."""
        recommendations = []
        
        # Primary issue recommendation (highest priority)
        primary_rec = self._generate_primary_recommendation(primary_issue, score)
        recommendations.append(primary_rec)
        
        # Supporting recommendations for other patterns
        for i, pattern in enumerate([p for p in patterns if not p.primary_indicator][:2]):
            rec = self._generate_supporting_recommendation(pattern, priority=i+2)
            recommendations.append(rec)
        
        # General improvement recommendation
        general_rec = ActionableRecommendation(
            priority=len(recommendations) + 1,
            action="Practice mock interviews regularly to build confidence and fluency",
            timeframe="Ongoing",
            resources=[
                "Pramp.com for free mock interviews",
                "InterviewBit for practice problems",
                "Record yourself answering common questions"
            ],
            success_metrics=[
                "Consistent scores above 7.0",
                "Reduced hesitation in responses",
                "Improved answer structure and clarity"
            ]
        )
        recommendations.append(general_rec)
        
        return recommendations
    
    def _detect_conceptual_gap(self, eval_data: Dict, score: float) -> bool:
        """Detect fundamental conceptual misunderstandings."""
        missing_concepts = eval_data.get("missing_concepts", [])
        incorrect_facts = eval_data.get("incorrect_facts", [])
        factually_correct = eval_data.get("is_factually_correct", True)
        
        return (
            score <= 4.0 or
            len(missing_concepts) >= 2 or
            len(incorrect_facts) >= 1 or
            not factually_correct
        )
    
    def _detect_structure_issues(self, eval_data: Dict, answer_text: str) -> bool:
        """Detect poor answer organization."""
        structure_issues = eval_data.get("structure_issues", [])
        organization_score = eval_data.get("organization_score", 10)
        
        return (
            len(structure_issues) > 0 or
            organization_score <= 4.0 or
            "disorganized" in str(eval_data.get("feedback", "")).lower()
        )
    
    def _detect_communication_issues(self, eval_data: Dict, score: float) -> bool:
        """Detect communication/clarity problems."""
        clarity_score = eval_data.get("clarity_score", 10)
        communication_issues = eval_data.get("communication_problems", [])
        
        return (
            clarity_score <= 5.0 or
            len(communication_issues) > 0 or
            score <= 5.0
        )
    
    def _detect_confidence_issues(self, eval_data: Dict, context: Dict) -> bool:
        """Detect confidence-related issues."""
        confidence_indicators = context.get("confidence_indicators", {})
        hesitation_count = confidence_indicators.get("hesitation_count", 0)
        filler_words = confidence_indicators.get("filler_words", 0)
        
        return hesitation_count > 3 or filler_words > 5
    
    def _detect_over_explaining(self, answer_text: str, eval_data: Dict) -> bool:
        """Detect overly verbose responses."""
        word_count = len(answer_text.split())
        avg_length = eval_data.get("typical_length", 100)
        
        return word_count > avg_length * 2
    
    def _detect_panic_response(self, answer_text: str, context: Dict) -> bool:
        """Detect panic-induced poor responses."""
        word_count = len(answer_text.split())
        time_pressure = context.get("time_pressure", False)
        
        return word_count < 15 and time_pressure
    
    def _extract_evidence(self, data: Dict, *keys) -> List[str]:
        """Extract evidence from evaluation data."""
        evidence = []
        for key in keys:
            if key in data:
                value = data[key]
                if isinstance(value, list):
                    evidence.extend([str(item) for item in value[:3]])  # Limit to 3 items
                elif value:
                    evidence.append(str(value))
        return evidence[:5]  # Limit total evidence
    
    def _assess_severity(self, score: float, weight: float) -> SeverityLevel:
        """Assess severity based on score impact."""
        impact_score = score * weight
        if impact_score <= 1.0:
            return SeverityLevel.HIGH
        elif impact_score <= 2.0:
            return SeverityLevel.MEDIUM
        else:
            return SeverityLevel.LOW
    
    def _determine_cascade_effects(self, primary_pattern: FailurePattern) -> List[str]:
        """Determine downstream effects of the primary issue."""
        cascades = {
            FailurePattern.CONCEPTUAL_GAP: [
                "Poor foundation leads to incorrect problem-solving approaches",
                "Difficulty connecting related concepts during discussion",
                "Inability to explain trade-offs or alternatives"
            ],
            FailurePattern.STRUCTURE_POOR: [
                "Interviewer struggles to follow your thought process",
                "Important points get lost in disorganized presentation",
                "Appears unprepared or lacking systematic approach"
            ],
            FailurePattern.COMMUNICATION_WEAK: [
                "Key technical points misunderstood by interviewer",
                "Difficulty demonstrating depth of knowledge",
                "May appear less competent than actual ability"
            ],
            FailurePattern.CONFIDENCE_LOW: [
                "Hesitation undermines credibility of correct answers",
                "Interviewer may question overall preparedness",
                "Self-doubt affects problem-solving approach"
            ]
        }
        return cascades.get(primary_pattern, ["General performance impact on interview perception"])
    
    def _generate_primary_recommendation(self, issue: RootCause, score: float) -> ActionableRecommendation:
        """Generate the most important recommendation to address."""
        recommendations = {
            FailurePattern.CONCEPTUAL_GAP: ActionableRecommendation(
                priority=1,
                action=f"Focus intensively on {issue.description.split()[0]} fundamentals - review core concepts and practice basic applications",
                timeframe="Immediate (1-2 weeks)",
                resources=[
                    "Review textbooks/online courses on fundamentals",
                    "Practice 20+ basic problems daily",
                    "Explain concepts aloud to verify understanding"
                ],
                success_metrics=[
                    "Score improvement of 3+ points on similar questions",
                    "Ability to explain concepts clearly without hesitation",
                    "Consistent correct identification of core principles"
                ]
            ),
            FailurePattern.STRUCTURE_POOR: ActionableRecommendation(
                priority=1,
                action="Master structured response frameworks (STAR for behavioral, Problem-Solution-Tradeoffs for technical)",
                timeframe="Within 1 week",
                resources=[
                    "Practice the PREP method (Point, Reason, Example, Point)",
                    "Use the What-Why-How framework for technical explanations",
                    "Record and analyze your answer structure"
                ],
                success_metrics=[
                    "Clear beginning-middle-end structure in all responses",
                    "Interviewer can easily follow your reasoning",
                    "Consistent use of transition phrases"
                ]
            ),
            FailurePattern.COMMUNICATION_WEAK: ActionableRecommendation(
                priority=1,
                action="Practice clear, concise technical communication with non-experts",
                timeframe="Ongoing (2-3 weeks)",
                resources=[
                    "Explain technical concepts to friends/family",
                    "Join Toastmasters or public speaking groups",
                    "Practice elevator pitches for technical topics"
                ],
                success_metrics=[
                    "Reduced 'um', 'uh', and filler words",
                    "Interviewer asks fewer clarification questions",
                    "Ability to adjust explanation complexity based on audience"
                ]
            ),
            FailurePattern.CONFIDENCE_LOW: ActionableRecommendation(
                priority=1,
                action="Build confidence through repetition and positive self-talk",
                timeframe="Ongoing (3-4 weeks)",
                resources=[
                    "Daily mock interviews with timer",
                    "Positive affirmation practice before interviews",
                    "Physical preparation (good sleep, exercise, nutrition)"
                ],
                success_metrics=[
                    "Reduced hesitation and pauses",
                    "Stronger voice projection and posture",
                    "Better handling of challenging questions"
                ]
            )
        }
        
        return recommendations.get(issue.pattern, ActionableRecommendation(
            priority=1,
            action=f"Address {issue.description} through targeted practice",
            timeframe="1-2 weeks",
            resources=["General interview preparation resources"],
            success_metrics=["Measurable score improvement"]
        ))
    
    def _generate_supporting_recommendation(self, issue: RootCause, priority: int) -> ActionableRecommendation:
        """Generate supporting recommendations."""
        return ActionableRecommendation(
            priority=priority,
            action=f"Also work on {issue.description.lower()}",
            timeframe="Within 2 weeks",
            resources=["Supplementary practice materials"],
            success_metrics=[f"Reduction in {issue.pattern.value.replace('_', ' ')} indicators"]
        )
    
    def _calculate_analysis_confidence(self, patterns: List[RootCause], eval_data: Dict) -> float:
        """Calculate confidence level in the analysis."""
        # Base confidence
        confidence = 0.7
        
        # Increase for clear evidence
        clear_indicators = len([p for p in patterns if p.evidence])
        confidence += min(0.2, clear_indicators * 0.05)
        
        # Decrease for borderline cases
        if eval_data.get("score", 5) >= 5.5:  # Borderline performance
            confidence -= 0.1
        
        return min(0.95, max(0.5, confidence))
    
    def get_session_analysis_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of all analyses for a session."""
        session_analyses = [a for a in self.analysis_history if a.session_id == session_id]
        
        if not session_analyses:
            return {}
        
        # Aggregate findings
        all_patterns = []
        primary_issues = []
        
        for analysis in session_analyses:
            all_patterns.extend(analysis.failure_patterns)
            primary_issues.append(analysis.primary_issue)
        
        # Most common patterns
        pattern_counts = {}
        for pattern in all_patterns:
            pattern_counts[pattern.pattern] = pattern_counts.get(pattern.pattern, 0) + 1
        
        return {
            "total_analyses": len(session_analyses),
            "average_score": sum(a.overall_score for a in session_analyses) / len(session_analyses),
            "most_common_patterns": [
                {"pattern": pattern.value, "count": count} 
                for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            ],
            "primary_focus_areas": list(set([issue.pattern.value for issue in primary_issues])),
            "confidence_level": sum(a.confidence_level for a in session_analyses) / len(session_analyses)
        }