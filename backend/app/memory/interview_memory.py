"""
Simplified Interview Memory Manager for Streamlit interface.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class InterviewInteraction:
    """Single Q&A interaction."""
    question: str
    answer: str
    score: float
    feedback: str
    strengths: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)


class InterviewMemoryManager:
    """
    Simplified memory manager for Streamlit interview sessions.
    Tracks interactions and provides summaries.
    """
    
    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self.interactions: List[InterviewInteraction] = []
        self.compressed_summary: str = ""
    
    def add_interaction(
        self,
        question: str,
        answer: str,
        evaluation: Dict[str, Any]
    ) -> None:
        """Add a new Q&A interaction."""
        interaction = InterviewInteraction(
            question=question,
            answer=answer,
            score=evaluation.get("score", 5),
            feedback=evaluation.get("feedback", ""),
            strengths=evaluation.get("strengths", []),
            improvements=evaluation.get("improvements", evaluation.get("improvement_suggestions", []))
        )
        
        self.interactions.append(interaction)
        
        # Compress old interactions
        if len(self.interactions) > self.max_history:
            self._compress_old_interactions()
    
    def _compress_old_interactions(self) -> None:
        """Compress older interactions into a summary."""
        entries_to_compress = len(self.interactions) - self.max_history
        old_entries = self.interactions[:entries_to_compress]
        
        summary_parts = [
            f"Q{i+1}: Score {entry.score:.1f}/10"
            for i, entry in enumerate(old_entries)
        ]
        
        if self.compressed_summary:
            self.compressed_summary += " | "
        self.compressed_summary += ", ".join(summary_parts)
        
        self.interactions = self.interactions[entries_to_compress:]
    
    def get_average_score(self) -> float:
        """Get average score across all interactions."""
        if not self.interactions:
            return 0.0
        return sum(i.score for i in self.interactions) / len(self.interactions)
    
    def get_all_strengths(self) -> List[str]:
        """Get all identified strengths."""
        strengths = []
        for interaction in self.interactions:
            strengths.extend(interaction.strengths)
        return strengths
    
    def get_all_improvements(self) -> List[str]:
        """Get all suggested improvements."""
        improvements = []
        for interaction in self.interactions:
            improvements.extend(interaction.improvements)
        return improvements
    
    def get_context_summary(self) -> str:
        """Get a summary for LLM context."""
        parts = [f"Total Questions: {len(self.interactions)}"]
        
        if self.interactions:
            avg = self.get_average_score()
            parts.append(f"Average Score: {avg:.1f}/10")
            
            recent = self.interactions[-3:]
            parts.append("Recent Performance:")
            for i, entry in enumerate(recent):
                parts.append(f"  Q{i+1}: {entry.score:.1f}/10")
        
        if self.compressed_summary:
            parts.append(f"Earlier: {self.compressed_summary}")
        
        return "\n".join(parts)
    
    def clear(self) -> None:
        """Clear all interactions."""
        self.interactions = []
        self.compressed_summary = ""
