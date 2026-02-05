"""
Confidence & Communication Signals Tracker
Monitors and analyzes verbal and non-verbal communication signals during interviews
to provide insights on confidence levels, clarity, and communication effectiveness.
"""
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import re
import statistics
from datetime import datetime


class ConfidenceLevel(Enum):
    """Confidence levels based on communication analysis"""
    VERY_HIGH = "very_high"    # 90-100% confidence
    HIGH = "high"              # 75-89% confidence
    MODERATE = "moderate"      # 60-74% confidence
    LOW = "low"                # 40-59% confidence
    VERY_LOW = "very_low"      # 0-39% confidence


class ClarityLevel(Enum):
    """Clarity levels of communication"""
    EXCEPTIONAL = "exceptional"    # Crystal clear, perfectly structured
    CLEAR = "clear"                # Well-articulated and understandable
    ADEQUATE = "adequate"          # Generally clear with minor issues
    UNCLEAR = "unclear"            # Difficult to follow or confusing
    VERY_UNCLEAR = "very_unclear"  # Very difficult to understand


class CommunicationSignal(Enum):
    """Types of communication signals detected"""
    FILLER_WORDS = "filler_words"          # um, uh, like, you know
    REPETITION = "repetition"              # Repeating words/phrases
    HESITATION = "hesitation"              # Pauses, delays in speech
    MONOTONE = "monotone"                  # Lack of vocal variety
    RAMBLING = "rambling"                  # Going off-topic or too verbose
    INTERRUPTIONS = "interruptions"        # Self-interruptions or corrections
    CLARITY_ISSUES = "clarity_issues"      # Unclear explanations
    CONFIDENCE_INDICATORS = "confidence_indicators"  # Positive/negative confidence signals


@dataclass
class SignalMetrics:
    """Metrics for specific communication signals"""
    signal_type: CommunicationSignal
    frequency: int
    duration: float  # seconds where applicable
    impact_score: float  # 0-1 impact on overall communication


@dataclass
class CommunicationAnalysis:
    """Complete analysis of communication signals for an answer"""
    answer_id: str
    timestamp: datetime
    confidence_level: ConfidenceLevel
    clarity_level: ClarityLevel
    confidence_score: float  # 0-100 numerical score
    clarity_score: float     # 0-100 numerical score
    signal_metrics: List[SignalMetrics]
    key_insights: List[str]
    improvement_suggestions: List[str]
    overall_communication_score: float  # Combined weighted score


class CommunicationSignalsTracker:
    """
    Tracks and analyzes communication signals to assess confidence and clarity.
    
    Features:
    - Real-time signal detection from text/transcript
    - Confidence level assessment
    - Clarity measurement
    - Pattern recognition for improvement areas
    - Historical trend analysis
    """
    
    def __init__(self):
        # Filler words and phrases to detect
        self.filler_words = {
            'um', 'uh', 'er', 'ah', 'like', 'you know', 'sort of', 
            'kind of', 'basically', 'actually', 'literally', 'totally',
            'so', 'well', 'right', 'okay', 'yeah', 'I mean'
        }
        
        # Confidence indicators (positive and negative)
        self.positive_indicators = {
            'clearly', 'definitely', 'absolutely', 'certainly', 'obviously',
            'confidently', 'strongly', 'firmly', 'precisely', 'exactly'
        }
        
        self.negative_indicators = {
            'maybe', 'perhaps', 'possibly', 'I think', 'I believe', 'I guess',
            'not sure', 'unsure', 'doubt', 'uncertain', 'probably'
        }
        
        # Analysis history
        self.analysis_history: List[CommunicationAnalysis] = []
        self.session_analyses: Dict[str, List[CommunicationAnalysis]] = {}
    
    def analyze_answer_communication(
        self,
        answer_id: str,
        answer_text: str,
        session_id: str,
        context: Dict[str, Any] = None
    ) -> CommunicationAnalysis:
        """
        Analyze communication signals in a given answer.
        
        Args:
            answer_id: Unique identifier for this answer
            answer_text: The actual answer text
            session_id: Interview session identifier
            context: Additional context (timing, previous answers, etc.)
            
        Returns:
            Complete communication analysis
        """
        # Preprocess text
        cleaned_text = self._preprocess_text(answer_text)
        
        # Detect various signals
        signal_metrics = self._detect_signal_metrics(cleaned_text, context or {})
        
        # Calculate confidence level
        confidence_level, confidence_score = self._assess_confidence(signal_metrics, cleaned_text)
        
        # Calculate clarity level
        clarity_level, clarity_score = self._assess_clarity(signal_metrics, cleaned_text, context or {})
        
        # Generate insights and suggestions
        key_insights = self._generate_insights(signal_metrics, confidence_level, clarity_level)
        improvement_suggestions = self._generate_suggestions(signal_metrics, confidence_level, clarity_level)
        
        # Calculate overall communication score
        overall_score = self._calculate_overall_score(confidence_score, clarity_score, signal_metrics)
        
        # Create analysis object
        analysis = CommunicationAnalysis(
            answer_id=answer_id,
            timestamp=datetime.now(),
            confidence_level=confidence_level,
            clarity_level=clarity_level,
            confidence_score=confidence_score,
            clarity_score=clarity_score,
            signal_metrics=signal_metrics,
            key_insights=key_insights,
            improvement_suggestions=improvement_suggestions,
            overall_communication_score=overall_score
        )
        
        # Store analysis
        self.analysis_history.append(analysis)
        if session_id not in self.session_analyses:
            self.session_analyses[session_id] = []
        self.session_analyses[session_id].append(analysis)
        
        return analysis
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize text for analysis."""
        # Convert to lowercase for consistent matching
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _detect_signal_metrics(self, text: str, context: Dict[str, Any]) -> List[SignalMetrics]:
        """Detect various communication signals and their metrics."""
        metrics = []
        
        # Detect filler words
        filler_count = 0
        for filler in self.filler_words:
            filler_count += len(re.findall(r'\b' + re.escape(filler) + r'\b', text))
        
        metrics.append(SignalMetrics(
            signal_type=CommunicationSignal.FILLER_WORDS,
            frequency=filler_count,
            duration=filler_count * 0.5,  # Estimated 0.5 seconds per filler
            impact_score=min(1.0, filler_count / max(1, len(text.split()) / 20))
        ))
        
        # Detect repetition
        words = text.split()
        unique_words = set(words)
        repetition_ratio = 1 - (len(unique_words) / len(words)) if words else 0
        repetition_count = int(repetition_ratio * len(words))
        
        metrics.append(SignalMetrics(
            signal_type=CommunicationSignal.REPETITION,
            frequency=repetition_count,
            duration=repetition_count * 0.3,
            impact_score=min(0.8, repetition_ratio * 2)
        ))
        
        # Detect hesitation (multiple approaches)
        # Method 1: Count ellipses and dashes
        hesitation_marks = len(re.findall(r'[.]{2,}|[-]{2,}', text))
        
        # Method 2: Count repeated starting phrases
        hesitation_phrases = len(re.findall(r'\b(i|i\'m|uh|um|well)\s+(i|i\'m|uh|um|well)\b', text))
        
        total_hesitations = hesitation_marks + hesitation_phrases
        
        metrics.append(SignalMetrics(
            signal_type=CommunicationSignal.HESITATION,
            frequency=total_hesitations,
            duration=total_hesitations * 1.0,  # Estimated 1 second per hesitation
            impact_score=min(0.9, total_hesitations / max(1, len(text.split()) / 15))
        ))
        
        # Detect rambling (length-based)
        word_count = len(words)
        avg_response_length = context.get('avg_response_length', 100)
        rambling_ratio = max(0, (word_count - avg_response_length) / avg_response_length) if avg_response_length > 0 else 0
        
        metrics.append(SignalMetrics(
            signal_type=CommunicationSignal.RAMBLING,
            frequency=1 if rambling_ratio > 0.5 else 0,
            duration=rambling_ratio * 2.0,
            impact_score=min(0.7, rambling_ratio)
        ))
        
        # Detect clarity issues
        clarity_issues = 0
        
        # Check for vague terms
        vague_terms = ['thing', 'stuff', 'this', 'that', 'these', 'those']
        for term in vague_terms:
            clarity_issues += len(re.findall(r'\b' + re.escape(term) + r'\b', text))
        
        # Check for incomplete sentences
        sentences = re.split(r'[.!?]+', text)
        incomplete_sentences = sum(1 for s in sentences if len(s.strip()) > 0 and len(s.split()) < 3)
        clarity_issues += incomplete_sentences
        
        metrics.append(SignalMetrics(
            signal_type=CommunicationSignal.CLARITY_ISSUES,
            frequency=clarity_issues,
            duration=0,  # Not time-based
            impact_score=min(0.8, clarity_issues / max(1, len(sentences)))
        ))
        
        # Detect confidence indicators
        positive_count = sum(1 for indicator in self.positive_indicators 
                           if indicator in text)
        negative_count = sum(1 for indicator in self.negative_indicators 
                           if indicator in text)
        
        confidence_indicators_net = positive_count - negative_count
        
        metrics.append(SignalMetrics(
            signal_type=CommunicationSignal.CONFIDENCE_INDICATORS,
            frequency=abs(confidence_indicators_net),
            duration=0,
            impact_score=min(0.6, abs(confidence_indicators_net) / max(1, len(text.split()) / 20))
        ))
        
        return metrics
    
    def _assess_confidence(self, metrics: List[SignalMetrics], text: str) -> Tuple[ConfidenceLevel, float]:
        """Assess confidence level based on detected signals."""
        # Calculate confidence detractors
        detractors = 0
        total_signals = 0
        
        for metric in metrics:
            if metric.signal_type in [CommunicationSignal.FILLER_WORDS, 
                                    CommunicationSignal.HESITATION,
                                    CommunicationSignal.REPETITION]:
                detractors += metric.frequency * metric.impact_score
                total_signals += metric.frequency
        
        # Normalize detractors
        normalized_detractors = detractors / max(1, total_signals)
        
        # Calculate confidence boosters
        confidence_boosters = 0
        for metric in metrics:
            if metric.signal_type == CommunicationSignal.CONFIDENCE_INDICATORS:
                # Positive indicators boost confidence
                confidence_boosters = metric.frequency * 0.1  # Scale down impact
        
        # Base confidence from text characteristics
        word_count = len(text.split())
        base_confidence = min(1.0, word_count / 50)  # More words = more confidence up to a point
        
        # Final confidence calculation
        confidence_score = max(0, min(100, 
                                   (base_confidence + confidence_boosters - normalized_detractors) * 100))
        
        # Map to confidence level
        if confidence_score >= 90:
            level = ConfidenceLevel.VERY_HIGH
        elif confidence_score >= 75:
            level = ConfidenceLevel.HIGH
        elif confidence_score >= 60:
            level = ConfidenceLevel.MODERATE
        elif confidence_score >= 40:
            level = ConfidenceLevel.LOW
        else:
            level = ConfidenceLevel.VERY_LOW
        
        return level, confidence_score
    
    def _assess_clarity(self, metrics: List[SignalMetrics], text: str, context: Dict[str, Any]) -> Tuple[ClarityLevel, float]:
        """Assess clarity level based on detected signals."""
        # Calculate clarity issues
        clarity_issues = 0
        total_elements = 0
        
        for metric in metrics:
            if metric.signal_type in [CommunicationSignal.CLARITY_ISSUES,
                                    CommunicationSignal.RAMBLING,
                                    CommunicationSignal.REPETITION]:
                clarity_issues += metric.frequency * metric.impact_score
                total_elements += 1 if metric.frequency > 0 else 0
        
        # Normalize clarity issues
        normalized_issues = clarity_issues / max(1, total_elements)
        
        # Structural clarity factors
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Average sentence length (optimal is 15-20 words)
        if sentences:
            avg_sentence_length = statistics.mean([len(s.split()) for s in sentences])
            structure_penalty = abs(avg_sentence_length - 17.5) / 17.5  # Distance from optimal
        else:
            structure_penalty = 1.0
        
        # Clarity score calculation
        base_clarity = 100 - (normalized_issues * 40) - (structure_penalty * 30)
        clarity_score = max(0, min(100, base_clarity))
        
        # Map to clarity level
        if clarity_score >= 90:
            level = ClarityLevel.EXCEPTIONAL
        elif clarity_score >= 75:
            level = ClarityLevel.CLEAR
        elif clarity_score >= 60:
            level = ClarityLevel.ADEQUATE
        elif clarity_score >= 40:
            level = ClarityLevel.UNCLEAR
        else:
            level = ClarityLevel.VERY_UNCLEAR
        
        return level, clarity_score
    
    def _generate_insights(
        self,
        metrics: List[SignalMetrics],
        confidence_level: ConfidenceLevel,
        clarity_level: ClarityLevel
    ) -> List[str]:
        """Generate key insights from the analysis."""
        insights = []
        
        # Confidence insights
        if confidence_level in [ConfidenceLevel.VERY_LOW, ConfidenceLevel.LOW]:
            insights.append("Low confidence indicators present - work on assertive language")
        elif confidence_level == ConfidenceLevel.MODERATE:
            insights.append("Moderate confidence shown - room for improvement in self-assurance")
        else:
            insights.append("Strong confidence demonstrated - positive communication presence")
        
        # Clarity insights
        if clarity_level in [ClarityLevel.VERY_UNCLEAR, ClarityLevel.UNCLEAR]:
            insights.append("Clarity issues detected - focus on structured explanations")
        elif clarity_level == ClarityLevel.ADEQUATE:
            insights.append("Generally clear communication with minor improvement areas")
        else:
            insights.append("Excellent clarity in explanations - easy to follow")
        
        # Specific signal insights
        filler_metric = next((m for m in metrics if m.signal_type == CommunicationSignal.FILLER_WORDS), None)
        if filler_metric and filler_metric.frequency > 3:
            insights.append(f"Frequent filler words ({filler_metric.frequency}) may undermine professionalism")
        
        hesitation_metric = next((m for m in metrics if m.signal_type == CommunicationSignal.HESITATION), None)
        if hesitation_metric and hesitation_metric.frequency > 2:
            insights.append("Multiple hesitation points suggest need for better preparation")
        
        return insights
    
    def _generate_suggestions(
        self,
        metrics: List[SignalMetrics],
        confidence_level: ConfidenceLevel,
        clarity_level: ClarityLevel
    ) -> List[str]:
        """Generate actionable improvement suggestions."""
        suggestions = []
        
        # Confidence improvement suggestions
        if confidence_level.value in ['very_low', 'low']:
            suggestions.extend([
                "Practice power poses before interviews to boost confidence",
                "Use positive self-affirmations during preparation",
                "Record yourself speaking to identify confidence barriers",
                "Prepare 3-5 key achievements to reference confidently"
            ])
        
        # Clarity improvement suggestions
        if clarity_level.value in ['very_unclear', 'unclear']:
            suggestions.extend([
                "Structure responses using STAR method (Situation, Task, Action, Result)",
                "Pause to organize thoughts before speaking",
                "Replace vague terms with specific examples",
                "Practice explaining concepts to non-technical people"
            ])
        
        # Specific signal suggestions
        filler_metric = next((m for m in metrics if m.signal_type == CommunicationSignal.FILLER_WORDS), None)
        if filler_metric and filler_metric.frequency > 2:
            suggestions.append("Reduce filler words by pausing silently instead of saying 'um' or 'uh'")
        
        hesitation_metric = next((m for m in metrics if m.signal_type == CommunicationSignal.HESITATION), None)
        if hesitation_metric and hesitation_metric.frequency > 1:
            suggestions.append("Anticipate likely questions and prepare key talking points in advance")
        
        rambling_metric = next((m for m in metrics if m.signal_type == CommunicationSignal.RAMBLING), None)
        if rambling_metric and rambling_metric.frequency > 0:
            suggestions.append("Practice concise responses - aim for 2-3 key points per answer")
        
        return suggestions[:5]  # Limit to 5 most relevant suggestions
    
    def _calculate_overall_score(
        self,
        confidence_score: float,
        clarity_score: float,
        metrics: List[SignalMetrics]
    ) -> float:
        """Calculate weighted overall communication score."""
        # Weight distribution
        confidence_weight = 0.4
        clarity_weight = 0.4
        signal_quality_weight = 0.2
        
        # Calculate signal quality score (fewer negative signals = higher quality)
        total_negative_impact = sum(m.impact_score for m in metrics 
                                  if m.signal_type in [CommunicationSignal.FILLER_WORDS,
                                                     CommunicationSignal.HESITATION,
                                                     CommunicationSignal.RAMBLING,
                                                     CommunicationSignal.CLARITY_ISSUES])
        signal_quality_score = max(0, 100 - (total_negative_impact * 25))  # Scale to 0-100
        
        # Calculate weighted score
        overall_score = (
            confidence_score * confidence_weight +
            clarity_score * clarity_weight +
            signal_quality_score * signal_quality_weight
        )
        
        return round(overall_score, 1)
    
    def get_session_communication_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive communication analysis for a session."""
        session_analyses = self.session_analyses.get(session_id, [])
        
        if not session_analyses:
            return {
                "total_answers_analyzed": 0,
                "average_confidence": 0,
                "average_clarity": 0,
                "communication_trends": [],
                "common_issues": [],
                "improvement_areas": []
            }
        
        # Calculate averages
        avg_confidence = statistics.mean([a.confidence_score for a in session_analyses])
        avg_clarity = statistics.mean([a.clarity_score for a in session_analyses])
        avg_overall = statistics.mean([a.overall_communication_score for a in session_analyses])
        
        # Identify trends
        trends = self._identify_communication_trends(session_analyses)
        
        # Aggregate common issues
        all_insights = []
        for analysis in session_analyses:
            all_insights.extend(analysis.key_insights)
        
        common_issues = list(set(all_insights))
        
        # Aggregate improvement suggestions
        all_suggestions = []
        for analysis in session_analyses:
            all_suggestions.extend(analysis.improvement_suggestions)
        
        # Get most frequent suggestions
        suggestion_freq = {}
        for suggestion in all_suggestions:
            suggestion_freq[suggestion] = suggestion_freq.get(suggestion, 0) + 1
        
        improvement_areas = sorted(suggestion_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        improvement_areas = [item[0] for item in improvement_areas]
        
        return {
            "total_answers_analyzed": len(session_analyses),
            "average_confidence": round(avg_confidence, 1),
            "average_clarity": round(avg_clarity, 1),
            "average_overall_score": round(avg_overall, 1),
            "confidence_level_distribution": self._get_level_distribution(
                [a.confidence_level for a in session_analyses]
            ),
            "clarity_level_distribution": self._get_level_distribution(
                [a.clarity_level for a in session_analyses]
            ),
            "communication_trends": trends,
            "common_issues": common_issues[:5],
            "improvement_areas": improvement_areas,
            "detailed_analyses": [asdict(analysis) for analysis in session_analyses]
        }
    
    def _identify_communication_trends(self, analyses: List[CommunicationAnalysis]) -> List[str]:
        """Identify trends in communication patterns."""
        trends = []
        
        if len(analyses) < 2:
            return ["Insufficient data for trend analysis"]
        
        # Confidence trend
        confidence_scores = [a.confidence_score for a in analyses]
        if len(confidence_scores) >= 2:
            first_half = confidence_scores[:len(confidence_scores)//2]
            second_half = confidence_scores[len(confidence_scores)//2:]
            
            first_avg = statistics.mean(first_half)
            second_avg = statistics.mean(second_half)
            
            if second_avg > first_avg + 10:
                trends.append("📈 Confidence improving throughout interview")
            elif second_avg < first_avg - 10:
                trends.append("📉 Confidence declining - may indicate fatigue or increasing difficulty")
            else:
                trends.append("➡️ Confidence remaining relatively stable")
        
        # Clarity trend
        clarity_scores = [a.clarity_score for a in analyses]
        if len(clarity_scores) >= 2:
            clarity_std = statistics.stdev(clarity_scores) if len(clarity_scores) > 1 else 0
            if clarity_std < 15:
                trends.append("🎯 Consistently clear communication")
            elif max(clarity_scores) - min(clarity_scores) > 30:
                trends.append("⚠️ Variable clarity - some answers much clearer than others")
        
        # Signal improvement
        early_fillers = sum(m.frequency for a in analyses[:len(analyses)//2] 
                           for m in a.signal_metrics 
                           if m.signal_type == CommunicationSignal.FILLER_WORDS)
        late_fillers = sum(m.frequency for a in analyses[len(analyses)//2:] 
                          for m in a.signal_metrics 
                          if m.signal_type == CommunicationSignal.FILLER_WORDS)
        
        if late_fillers < early_fillers:
            trends.append("✅ Reduction in filler words over time")
        elif late_fillers > early_fillers:
            trends.append("⚠️ Increasing use of filler words")
        
        return trends
    
    def _get_level_distribution(self, levels: List[Enum]) -> Dict[str, int]:
        """Get distribution of confidence/clarity levels."""
        distribution = {}
        for level in levels:
            distribution[level.value] = distribution.get(level.value, 0) + 1
        return distribution
    
    def reset_session_tracking(self, session_id: str):
        """Reset tracking for a specific session."""
        if session_id in self.session_analyses:
            del self.session_analyses[session_id]


# Integration helper functions
def integrate_with_evaluation(
    communication_tracker: CommunicationSignalsTracker,
    evaluation_data: Dict[str, Any],
    answer_text: str,
    session_id: str,
    answer_id: str
) -> Dict[str, Any]:
    """
    Integrate communication analysis with evaluation data.
    
    Args:
        communication_tracker: Initialized CommunicationSignalsTracker
        evaluation_data: Existing evaluation data
        answer_text: The answer being evaluated
        session_id: Interview session identifier
        answer_id: Unique answer identifier
        
    Returns:
        Enhanced evaluation data with communication insights
    """
    # Perform communication analysis
    comm_analysis = communication_tracker.analyze_answer_communication(
        answer_id=answer_id,
        answer_text=answer_text,
        session_id=session_id
    )
    
    # Enhance evaluation data with communication metrics
    enhanced_evaluation = evaluation_data.copy()
    
    # Add communication scores
    enhanced_evaluation.update({
        "confidence_level": comm_analysis.confidence_level.value,
        "confidence_score": comm_analysis.confidence_score,
        "clarity_level": comm_analysis.clarity_level.value,
        "clarity_score": comm_analysis.clarity_score,
        "communication_score": comm_analysis.overall_communication_score,
        "communication_insights": comm_analysis.key_insights,
        "communication_suggestions": comm_analysis.improvement_suggestions
    })
    
    # Adjust overall score based on communication quality
    base_score = evaluation_data.get("score", 5.0)
    communication_factor = comm_analysis.overall_communication_score / 100
    
    # Communication can impact score by up to ±2 points
    communication_adjustment = (communication_factor - 0.7) * 2  # Center around 0.7 (70%)
    adjusted_score = max(0, min(10, base_score + communication_adjustment))
    
    enhanced_evaluation["score"] = round(adjusted_score, 1)
    enhanced_evaluation["score_adjustment_reason"] = (
        f"Adjusted by {communication_adjustment:+.1f} points based on communication quality "
        f"(confidence: {comm_analysis.confidence_score:.0f}%, clarity: {comm_analysis.clarity_score:.0f}%)"
    )
    
    return enhanced_evaluation


# Example usage
async def demo_communication_tracking():
    """Demonstrate communication tracking functionality."""
    tracker = CommunicationSignalsTracker()
    
    sample_answers = [
        {
            "id": "ans_001",
            "text": "Um, well, basically, I think the, uh, system design approach should involve, you know, microservices architecture and, like, containerization for scalability.",
            "session": "demo_session_1"
        },
        {
            "id": "ans_002",
            "text": "The system should use a microservices architecture with Docker containers for optimal scalability and maintainability. This approach allows independent deployment and scaling of individual services.",
            "session": "demo_session_1"
        },
        {
            "id": "ans_003",
            "text": "I'm not entirely sure, but maybe we could use Kubernetes for orchestration? Or perhaps AWS ECS? I guess it depends on the specific requirements and team expertise.",
            "session": "demo_session_1"
        }
    ]
    
    print("🎯 Communication Signals Analysis Demo")
    print("=" * 50)
    
    for answer in sample_answers:
        analysis = tracker.analyze_answer_communication(
            answer_id=answer["id"],
            answer_text=answer["text"],
            session_id=answer["session"]
        )
        
        print(f"\n📝 Answer {answer['id']}:")
        print(f"   Text: {answer['text'][:100]}{'...' if len(answer['text']) > 100 else ''}")
        print(f"   Confidence: {analysis.confidence_level.value} ({analysis.confidence_score:.1f}%)")
        print(f"   Clarity: {analysis.clarity_level.value} ({analysis.clarity_score:.1f}%)")
        print(f"   Overall Score: {analysis.overall_communication_score:.1f}%")
        print(f"   Key Insights: {', '.join(analysis.key_insights[:2])}")
        print(f"   Suggestions: {', '.join(analysis.improvement_suggestions[:2])}")
    
    # Session summary
    session_summary = tracker.get_session_communication_summary("demo_session_1")
    print(f"\n📊 Session Summary:")
    print(f"   Average Confidence: {session_summary['average_confidence']:.1f}%")
    print(f"   Average Clarity: {session_summary['average_clarity']:.1f}%")
    print(f"   Communication Trends: {', '.join(session_summary['communication_trends'])}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_communication_tracking())