"""
Interview Pressure Simulation Module
Simulates realistic interview pressure scenarios to better prepare candidates
for actual interview conditions including interruptions, silence, time pressure, and follow-ups.
"""
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import random
import time
from datetime import datetime


class PressureType(Enum):
    """Types of interview pressure scenarios"""
    SILENCE = "silence"              # Extended pauses/silence from interviewer
    INTERRUPTION = "interruption"    # Cutting off or interrupting responses
    STRICT_FOLLOWUP = "strict_followup"  # Demanding deeper explanations
    TIME_PRESSURE = "time_pressure"  # Rushed questioning or time constraints
    AGGRESSIVE_CHALLENGE = "aggressive_challenge"  # Challenging or skeptical responses
    RAPID_FIRE = "rapid_fire"        # Quick succession of questions


class PressureIntensity(Enum):
    """Intensity levels for pressure simulation"""
    LOW = "low"        # Subtle/mild pressure
    MEDIUM = "medium"  # Moderate pressure
    HIGH = "high"      # Strong/intense pressure


@dataclass
class PressureScenario:
    """Represents a specific pressure scenario"""
    pressure_type: PressureType
    intensity: PressureIntensity
    trigger_condition: str  # What triggers this pressure
    duration_range: Tuple[int, int]  # Duration in seconds (min, max)
    description: str
    impact_on_evaluation: float  # How much this affects scoring (0-1 multiplier)


@dataclass
class PressureEvent:
    """Actual pressure event that occurs during interview"""
    scenario: PressureScenario
    triggered_at: datetime
    duration: float  # Actual duration in seconds
    response_quality_impact: float  # Measured impact on response quality


class PressureSimulationEngine:
    """
    Simulates realistic interview pressure to train candidates for real scenarios.
    
    Features:
    - Configurable pressure scenarios based on candidate performance
    - Realistic timing and intensity adjustments
    - Impact measurement on response quality
    - Adaptive difficulty based on candidate resilience
    """
    
    def __init__(self):
        self.scenarios = self._initialize_scenarios()
        self.active_pressures: Dict[str, List[PressureEvent]] = {}
        self.pressure_history: List[PressureEvent] = []
        
    def _initialize_scenarios(self) -> List[PressureScenario]:
        """Initialize standard pressure scenarios."""
        return [
            # Silence Scenarios
            PressureScenario(
                pressure_type=PressureType.SILENCE,
                intensity=PressureIntensity.LOW,
                trigger_condition="after candidate finishes speaking",
                duration_range=(3, 8),
                description="Brief pause allowing candidate to continue or conclude",
                impact_on_evaluation=0.1
            ),
            PressureScenario(
                pressure_type=PressureType.SILENCE,
                intensity=PressureIntensity.MEDIUM,
                trigger_condition="during candidate's explanation",
                duration_range=(8, 15),
                description="Extended silence testing comfort with pauses",
                impact_on_evaluation=0.3
            ),
            PressureScenario(
                pressure_type=PressureType.SILENCE,
                intensity=PressureIntensity.HIGH,
                trigger_condition="after partial answer",
                duration_range=(15, 30),
                description="Uncomfortable silence pressuring completion",
                impact_on_evaluation=0.5
            ),
            
            # Interruption Scenarios
            PressureScenario(
                pressure_type=PressureType.INTERRUPTION,
                intensity=PressureIntensity.LOW,
                trigger_condition="when candidate hesitates or uses filler words",
                duration_range=(2, 5),
                description="Gentle interruption to redirect focus",
                impact_on_evaluation=0.2
            ),
            PressureScenario(
                pressure_type=PressureType.INTERRUPTION,
                intensity=PressureIntensity.MEDIUM,
                trigger_condition="when answer becomes unfocused",
                duration_range=(5, 10),
                description="Moderate interruption to regain control",
                impact_on_evaluation=0.4
            ),
            PressureScenario(
                pressure_type=PressureType.INTERRUPTION,
                intensity=PressureIntensity.HIGH,
                trigger_condition="when candidate is rambling or off-topic",
                duration_range=(10, 20),
                description="Strong interruption to enforce structure",
                impact_on_evaluation=0.6
            ),
            
            # Strict Follow-up Scenarios
            PressureScenario(
                pressure_type=PressureType.STRICT_FOLLOWUP,
                intensity=PressureIntensity.LOW,
                trigger_condition="when answer lacks depth",
                duration_range=(15, 30),
                description="Request for more specific details",
                impact_on_evaluation=0.2
            ),
            PressureScenario(
                pressure_type=PressureType.STRICT_FOLLOWUP,
                intensity=PressureIntensity.MEDIUM,
                trigger_condition="when technical explanation is surface-level",
                duration_range=(30, 60),
                description="Demand for deeper technical understanding",
                impact_on_evaluation=0.4
            ),
            PressureScenario(
                pressure_type=PressureType.STRICT_FOLLOWUP,
                intensity=PressureIntensity.HIGH,
                trigger_condition="when answer shows knowledge gaps",
                duration_range=(60, 120),
                description="Intensive probing of weak areas",
                impact_on_evaluation=0.7
            ),
            
            # Time Pressure Scenarios
            PressureScenario(
                pressure_type=PressureType.TIME_PRESSURE,
                intensity=PressureIntensity.LOW,
                trigger_condition="general time constraint awareness",
                duration_range=(30, 60),
                description="Gentle reminder about time limitations",
                impact_on_evaluation=0.1
            ),
            PressureScenario(
                pressure_type=PressureType.TIME_PRESSURE,
                intensity=PressureIntensity.MEDIUM,
                trigger_condition="when answer is taking too long",
                duration_range=(15, 30),
                description="More urgent time pressure",
                impact_on_evaluation=0.3
            ),
            PressureScenario(
                pressure_type=PressureType.TIME_PRESSURE,
                intensity=PressureIntensity.HIGH,
                trigger_condition="critical time constraints",
                duration_range=(5, 15),
                description="Severe time crunch pressure",
                impact_on_evaluation=0.6
            ),
            
            # Aggressive Challenge Scenarios
            PressureScenario(
                pressure_type=PressureType.AGGRESSIVE_CHALLENGE,
                intensity=PressureIntensity.LOW,
                trigger_condition="when answer seems uncertain",
                duration_range=(20, 40),
                description="Gentle skepticism requiring justification",
                impact_on_evaluation=0.3
            ),
            PressureScenario(
                pressure_type=PressureType.AGGRESSIVE_CHALLENGE,
                intensity=PressureIntensity.MEDIUM,
                trigger_condition="when technical claim seems questionable",
                duration_range=(40, 80),
                description="Moderate challenge to defend position",
                impact_on_evaluation=0.5
            ),
            PressureScenario(
                pressure_type=PressureType.AGGRESSIVE_CHALLENGE,
                intensity=PressureIntensity.HIGH,
                trigger_condition="when answer contradicts common practices",
                duration_range=(80, 150),
                description="Intense scrutiny of technical decisions",
                impact_on_evaluation=0.8
            ),
            
            # Rapid Fire Scenarios
            PressureScenario(
                pressure_type=PressureType.RAPID_FIRE,
                intensity=PressureIntensity.LOW,
                trigger_condition="testing quick thinking ability",
                duration_range=(60, 120),
                description="Series of quick, related questions",
                impact_on_evaluation=0.2
            ),
            PressureScenario(
                pressure_type=PressureType.RAPID_FIRE,
                intensity=PressureIntensity.MEDIUM,
                trigger_condition="assessing mental agility under pressure",
                duration_range=(120, 180),
                description="Rapid succession testing composure",
                impact_on_evaluation=0.4
            ),
            PressureScenario(
                pressure_type=PressureType.RAPID_FIRE,
                intensity=PressureIntensity.HIGH,
                trigger_condition="maximum pressure scenario",
                duration_range=(180, 300),
                description="Intense rapid questioning barrage",
                impact_on_evaluation=0.7
            )
        ]
    
    def should_apply_pressure(
        self,
        session_id: str,
        current_score: float,
        question_count: int,
        answer_quality: float,
        time_elapsed: float
    ) -> Optional[PressureScenario]:
        """
        Determine if pressure should be applied based on current interview state.
        
        Args:
            session_id: Interview session identifier
            current_score: Current performance score
            question_count: Number of questions asked
            answer_quality: Quality metric of recent answers (0-1)
            time_elapsed: Time elapsed in current question
            
        Returns:
            PressureScenario to apply, or None if no pressure needed
        """
        # Get session pressure history
        session_pressures = self.active_pressures.get(session_id, [])
        recent_pressures = [p for p in session_pressures if 
                          (datetime.now() - p.triggered_at).seconds < 300]  # Last 5 minutes
        
        # Adjust pressure probability based on various factors
        pressure_probability = 0.0
        
        # Lower scores = higher pressure probability
        if current_score < 4.0:
            pressure_probability += 0.4
        elif current_score < 6.0:
            pressure_probability += 0.2
        elif current_score > 8.0:
            pressure_probability -= 0.2  # Reduce pressure for strong performers
        
        # Poor answer quality increases pressure
        if answer_quality < 0.5:
            pressure_probability += 0.3
        elif answer_quality < 0.7:
            pressure_probability += 0.1
        
        # More questions = increased pressure
        if question_count > 3:
            pressure_probability += 0.1
        if question_count > 6:
            pressure_probability += 0.2
        
        # Recent pressure reduces likelihood of more pressure
        recent_pressure_count = len(recent_pressures)
        if recent_pressure_count > 0:
            pressure_probability -= (recent_pressure_count * 0.15)
        
        # Random element for realism
        pressure_probability += random.uniform(-0.1, 0.1)
        
        # Apply pressure based on probability
        if random.random() < max(0.05, min(0.8, pressure_probability)):
            return self._select_appropriate_scenario(current_score, answer_quality, time_elapsed)
        
        return None
    
    def _select_appropriate_scenario(
        self,
        current_score: float,
        answer_quality: float,
        time_elapsed: float
    ) -> PressureScenario:
        """Select the most appropriate pressure scenario."""
        # Filter scenarios based on current context
        eligible_scenarios = []
        
        # For lower scores, favor more intense scenarios
        if current_score < 4.0:
            intensity_filter = [PressureIntensity.MEDIUM, PressureIntensity.HIGH]
        elif current_score < 6.0:
            intensity_filter = [PressureIntensity.LOW, PressureIntensity.MEDIUM]
        else:
            intensity_filter = [PressureIntensity.LOW]
        
        # For poor answer quality, focus on specific pressure types
        if answer_quality < 0.5:
            type_filter = [PressureType.INTERRUPTION, PressureType.STRICT_FOLLOWUP, 
                          PressureType.AGGRESSIVE_CHALLENGE]
        elif answer_quality < 0.7:
            type_filter = [PressureType.SILENCE, PressureType.STRICT_FOLLOWUP, 
                          PressureType.TIME_PRESSURE]
        else:
            type_filter = [PressureType.SILENCE, PressureType.TIME_PRESSURE]
        
        # Filter scenarios
        for scenario in self.scenarios:
            if (scenario.intensity in intensity_filter and 
                scenario.pressure_type in type_filter):
                eligible_scenarios.append(scenario)
        
        # If no scenarios match filters, return a moderate silence scenario
        if not eligible_scenarios:
            eligible_scenarios = [s for s in self.scenarios 
                                if s.pressure_type == PressureType.SILENCE 
                                and s.intensity == PressureIntensity.MEDIUM]
        
        # Select randomly from eligible scenarios
        return random.choice(eligible_scenarios)
    
    async def apply_pressure(
        self,
        session_id: str,
        scenario: PressureScenario,
        callback_function=None
    ) -> PressureEvent:
        """
        Apply pressure scenario and measure its impact.
        
        Args:
            session_id: Interview session identifier
            scenario: The pressure scenario to apply
            callback_function: Optional async function to handle pressure effects
            
        Returns:
            PressureEvent with measured impact
        """
        # Create pressure event
        pressure_event = PressureEvent(
            scenario=scenario,
            triggered_at=datetime.now(),
            duration=random.uniform(scenario.duration_range[0], scenario.duration_range[1]),
            response_quality_impact=scenario.impact_on_evaluation
        )
        
        # Track in session
        if session_id not in self.active_pressures:
            self.active_pressures[session_id] = []
        self.active_pressures[session_id].append(pressure_event)
        self.pressure_history.append(pressure_event)
        
        # Apply pressure effect
        if callback_function:
            await callback_function(pressure_event)
        
        # Simulate pressure duration
        await asyncio.sleep(pressure_event.duration)
        
        return pressure_event
    
    def measure_pressure_impact(
        self,
        session_id: str,
        pre_pressure_state: Dict[str, Any],
        post_pressure_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Measure the actual impact of pressure on candidate performance.
        
        Args:
            session_id: Interview session identifier
            pre_pressure_state: State before pressure applied
            post_pressure_state: State after pressure applied
            
        Returns:
            Dictionary with impact measurements
        """
        impact_measurements = {
            "confidence_change": 0.0,
            "clarity_change": 0.0,
            "structure_change": 0.0,
            "stress_indicators": [],
            "resilience_score": 0.0
        }
        
        # Calculate changes in key metrics
        pre_score = pre_pressure_state.get("overall_score", 5.0)
        post_score = post_pressure_state.get("overall_score", 5.0)
        
        impact_measurements["score_impact"] = pre_score - post_score
        
        # Check for stress indicators
        post_answer = post_pressure_state.get("answer_text", "")
        if len(post_answer.split()) < len(pre_pressure_state.get("answer_text", "").split()) * 0.7:
            impact_measurements["stress_indicators"].append("shortened_response")
        
        if "um" in post_answer.lower() or "uh" in post_answer.lower():
            impact_measurements["stress_indicators"].append("increased_filler_words")
        
        # Calculate resilience score (0-1, higher is better)
        if impact_measurements["score_impact"] <= 0:  # No negative impact
            impact_measurements["resilience_score"] = 0.9
        elif impact_measurements["score_impact"] <= 1.0:  # Minor impact
            impact_measurements["resilience_score"] = 0.7
        elif impact_measurements["score_impact"] <= 2.0:  # Moderate impact
            impact_measurements["resilience_score"] = 0.5
        else:  # Severe impact
            impact_measurements["resilience_score"] = 0.3
        
        return impact_measurements
    
    def get_pressure_advice(self, session_id: str) -> List[str]:
        """
        Provide advice based on pressure handling patterns.
        
        Args:
            session_id: Interview session identifier
            
        Returns:
            List of personalized advice strings
        """
        session_pressures = self.active_pressures.get(session_id, [])
        if not session_pressures:
            return ["No pressure scenarios encountered yet - good baseline performance"]
        
        advice = []
        pressure_types = [p.scenario.pressure_type for p in session_pressures]
        resilience_scores = [self.measure_pressure_resilience(session_id)]
        
        # Silence handling advice
        if pressure_types.count(PressureType.SILENCE) > 0:
            avg_duration = sum(p.duration for p in session_pressures 
                             if p.scenario.pressure_type == PressureType.SILENCE) / \
                          pressure_types.count(PressureType.SILENCE)
            if avg_duration > 10:
                advice.append("Practice using silence constructively - use it to organize thoughts")
            else:
                advice.append("Good handling of brief silences - maintain this composure")
        
        # Interruption advice
        if pressure_types.count(PressureType.INTERRUPTION) > 0:
            advice.append("Work on staying composed when interrupted - acknowledge and pivot gracefully")
        
        # Time pressure advice
        if pressure_types.count(PressureType.TIME_PRESSURE) > 0:
            advice.append("Practice prioritizing key points under time constraints")
        
        # General resilience advice
        avg_resilience = sum(resilience_scores) / len(resilience_scores) if resilience_scores else 0.5
        if avg_resilience < 0.6:
            advice.append("Focus on stress management techniques for high-pressure situations")
        elif avg_resilience > 0.8:
            advice.append("Excellent pressure handling - continue building this strength")
        
        return advice if advice else ["Strong overall pressure handling demonstrated"]
    
    def measure_pressure_resilience(self, session_id: str) -> float:
        """
        Calculate overall pressure resilience score for a session.
        
        Args:
            session_id: Interview session identifier
            
        Returns:
            Resilience score (0-1, higher is better)
        """
        session_pressures = self.active_pressures.get(session_id, [])
        if not session_pressures:
            return 0.8  # Default good resilience for no pressure encountered
        
        # Calculate average resilience from measured impacts
        total_resilience = 0.0
        valid_measurements = 0
        
        for pressure_event in session_pressures:
            # Simulate measurement (in real implementation, this would use actual data)
            simulated_impact = pressure_event.response_quality_impact
            resilience = max(0.1, 1.0 - simulated_impact)  # Inverse relationship
            total_resilience += resilience
            valid_measurements += 1
        
        return total_resilience / valid_measurements if valid_measurements > 0 else 0.5
    
    def get_session_pressure_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get comprehensive summary of pressure scenarios for a session.
        
        Args:
            session_id: Interview session identifier
            
        Returns:
            Dictionary with pressure summary statistics
        """
        session_pressures = self.active_pressures.get(session_id, [])
        
        if not session_pressures:
            return {
                "total_pressure_events": 0,
                "pressure_types_encountered": [],
                "average_intensity": "None",
                "resilience_score": 0.8,
                "advice": ["No pressure scenarios encountered - maintain steady performance"]
            }
        
        # Analyze pressure patterns
        pressure_counts = {}
        total_intensity = 0
        total_duration = 0
        
        for event in session_pressures:
            pressure_type = event.scenario.pressure_type.value
            pressure_counts[pressure_type] = pressure_counts.get(pressure_type, 0) + 1
            total_intensity += {"low": 1, "medium": 2, "high": 3}[event.scenario.intensity.value]
            total_duration += event.duration
        
        avg_intensity_score = total_intensity / len(session_pressures)
        intensity_labels = {1: "Low", 2: "Medium", 3: "High"}
        avg_intensity = intensity_labels.get(round(avg_intensity_score), "Medium")
        
        resilience_score = self.measure_pressure_resilience(session_id)
        advice = self.get_pressure_advice(session_id)
        
        return {
            "total_pressure_events": len(session_pressures),
            "pressure_types_encountered": list(pressure_counts.keys()),
            "pressure_distribution": pressure_counts,
            "average_intensity": avg_intensity,
            "total_pressure_duration": round(total_duration, 1),
            "resilience_score": round(resilience_score, 2),
            "advice": advice
        }
    
    def reset_session_pressure(self, session_id: str):
        """Reset pressure tracking for a session."""
        if session_id in self.active_pressures:
            del self.active_pressures[session_id]


# Example usage and integration functions
async def simulate_interview_pressure(
    pressure_engine: PressureSimulationEngine,
    session_id: str,
    current_state: Dict[str, Any],
    pressure_callback=None
) -> Optional[PressureEvent]:
    """
    Main function to check for and apply interview pressure.
    
    Args:
        pressure_engine: Initialized PressureSimulationEngine
        session_id: Current interview session ID
        current_state: Dictionary with current interview state
        pressure_callback: Async function to handle pressure effects
        
    Returns:
        PressureEvent if pressure was applied, None otherwise
    """
    # Check if pressure should be applied
    scenario = pressure_engine.should_apply_pressure(
        session_id=session_id,
        current_score=current_state.get("current_score", 5.0),
        question_count=current_state.get("question_count", 1),
        answer_quality=current_state.get("answer_quality", 0.7),
        time_elapsed=current_state.get("time_elapsed", 60.0)
    )
    
    if scenario:
        # Apply the pressure
        pressure_event = await pressure_engine.apply_pressure(
            session_id=session_id,
            scenario=scenario,
            callback_function=pressure_callback
        )
        return pressure_event
    
    return None


# Example callback function for handling pressure effects
async def handle_pressure_effects(pressure_event: PressureEvent):
    """
    Example callback function to demonstrate pressure handling.
    In a real implementation, this would integrate with the UI/frontend.
    """
    pressure_messages = {
        PressureType.SILENCE: "Interviewer maintains thoughtful silence...",
        PressureType.INTERRUPTION: "Interviewer interrupts to redirect focus...",
        PressureType.STRICT_FOLLOWUP: "Interviewer presses for deeper explanation...",
        PressureType.TIME_PRESSURE: "Interviewer emphasizes time constraints...",
        PressureType.AGGRESSIVE_CHALLENGE: "Interviewer challenges your assumptions...",
        PressureType.RAPID_FIRE: "Interviewer rapidly fires follow-up questions..."
    }
    
    message = pressure_messages.get(pressure_event.scenario.pressure_type, 
                                  "Interviewer applies pressure...")
    
    # In a real implementation, this would:
    # 1. Update UI to show pressure indicators
    # 2. Modify question delivery timing
    # 3. Adjust evaluation criteria for pressure handling
    # 4. Provide real-time feedback to candidate
    
    print(f"[PRESSURE] {message} (Duration: {pressure_event.duration:.1f}s)")
    await asyncio.sleep(0.1)  # Simulate processing time