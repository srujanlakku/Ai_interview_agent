"""
Report Generator - Creates comprehensive, exportable interview summaries in multiple formats.
Generates detailed PDF and text reports with visual score representations and actionable insights.
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import io
from pathlib import Path


@dataclass
class ReportMetadata:
    """Metadata for the interview report."""
    candidate_name: str
    role: str
    experience_level: str
    company: Optional[str]
    interview_date: datetime
    total_questions: int
    average_score: float
    duration_minutes: float
    report_id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_name": self.candidate_name,
            "role": self.role,
            "experience_level": self.experience_level,
            "company": self.company,
            "interview_date": self.interview_date.isoformat(),
            "total_questions": self.total_questions,
            "average_score": round(self.average_score, 2),
            "duration_minutes": round(self.duration_minutes, 1),
            "report_id": self.report_id
        }


@dataclass
class ScoreBreakdown:
    """Detailed score breakdown for the report."""
    correctness: float
    depth: float
    clarity: float
    overall: float
    confidence_band: str
    explanation: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "correctness": round(self.correctness, 1),
            "depth": round(self.depth, 1),
            "clarity": round(self.clarity, 1),
            "overall": round(self.overall, 1),
            "confidence_band": self.confidence_band,
            "explanation": self.explanation
        }


@dataclass
class SkillGapReport:
    """Skill gap analysis for the report."""
    category: str
    severity: str
    current_level: float
    target_level: float
    gap_size: float
    recommendations: List[str]
    resources: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "severity": self.severity,
            "current_level": round(self.current_level, 1),
            "target_level": round(self.target_level, 1),
            "gap_size": round(self.gap_size, 1),
            "recommendations": self.recommendations,
            "resources": self.resources
        }


class ReportGenerator:
    """
    Enterprise-grade report generator for interview assessments.
    
    Features:
    - Multiple export formats (PDF, text, JSON)
    - Visual score representations
    - Comprehensive skill gap analysis
    - Actionable recommendations
    - Professional formatting
    """
    
    def __init__(self):
        self.template_dir = Path(__file__).parent / "templates"
        self.template_dir.mkdir(exist_ok=True)
    
    def generate_comprehensive_report(
        self,
        metadata: ReportMetadata,
        score_breakdown: ScoreBreakdown,
        skill_gaps: List[SkillGapReport],
        strengths: List[str],
        weaknesses: List[str],
        question_history: Optional[List[Dict[str, Any]]] = None,
        learning_path: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive interview report with all components.
        
        Args:
            metadata: Report metadata
            score_breakdown: Detailed score analysis
            skill_gaps: Identified skill gaps
            strengths: Candidate strengths
            weaknesses: Candidate weaknesses
            question_history: Optional Q&A history
            learning_path: Optional personalized learning path
            
        Returns:
            Complete report dictionary
        """
        report = {
            "metadata": metadata.to_dict(),
            "executive_summary": self._generate_executive_summary(metadata, score_breakdown),
            "detailed_scores": score_breakdown.to_dict(),
            "readiness_assessment": self._assess_readiness(metadata.average_score),
            "skill_gaps": [gap.to_dict() for gap in skill_gaps],
            "strengths": strengths[:10],  # Limit to top 10
            "weaknesses": weaknesses[:10],  # Limit to top 10
            "recommendations": self._generate_recommendations(
                metadata, score_breakdown, skill_gaps, strengths, weaknesses
            ),
            "learning_roadmap": learning_path or self._generate_default_learning_path(metadata),
            "question_analysis": self._analyze_questions(question_history) if question_history else {},
            "visual_data": self._generate_visual_data(metadata, score_breakdown, skill_gaps),
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def _generate_executive_summary(
        self,
        metadata: ReportMetadata,
        score_breakdown: ScoreBreakdown
    ) -> str:
        """Generate executive summary for the report."""
        avg_score = metadata.average_score
        
        if avg_score >= 8.5:
            performance_level = "Exceptional"
            description = "demonstrates outstanding technical proficiency and communication skills"
        elif avg_score >= 7.0:
            performance_level = "Strong"
            description = "shows solid understanding with minor areas for refinement"
        elif avg_score >= 5.5:
            performance_level = "Competent"
            description = "has a good foundation but needs focused improvement"
        elif avg_score >= 4.0:
            performance_level = "Developing"
            description = "requires significant skill development and practice"
        else:
            performance_level = "Needs Substantial Improvement"
            description = "needs fundamental preparation and structured learning"
        
        return (
            f"Candidate {metadata.candidate_name}, applying for {metadata.role} "
            f"({metadata.experience_level} level), completed an interview assessment "
            f"on {metadata.interview_date.strftime('%B %d, %Y')}.\n\n"
            f"Performance Summary: {performance_level} - The candidate {description}. "
            f"Average score of {avg_score:.1f}/10 across {metadata.total_questions} questions "
            f"with {score_breakdown.confidence_band.lower()} confidence in assessment.\n\n"
            f"Key Strength Areas: {', '.join(metadata.role.split()[:2])} fundamentals, "
            f"problem-solving approach, and technical communication.\n\n"
            f"Recommended Next Steps: Focus on identified skill gaps and follow "
            f"the personalized learning roadmap provided."
        )
    
    def _assess_readiness(self, avg_score: float) -> Dict[str, Any]:
        """Assess interview readiness level."""
        if avg_score >= 8.5:
            level = "Interview Ready"
            color = "#10B981"  # Green
            description = "Exceptionally well-prepared for interviews"
            next_steps = ["Apply to target positions", "Schedule real interviews", "Maintain skills"]
        elif avg_score >= 7.0:
            level = "Well Prepared"
            color = "#22C55E"  # Light green
            description = "Strong preparation with minor refinements needed"
            next_steps = ["Practice mock interviews", "Refine weak areas", "Build confidence"]
        elif avg_score >= 5.5:
            level = "Making Progress"
            color = "#F59E0B"  # Amber
            description = "Good foundation, continue focused practice"
            next_steps = ["Address skill gaps", "Increase practice frequency", "Study fundamentals"]
        elif avg_score >= 4.0:
            level = "Keep Practicing"
            color = "#F97316"  # Orange
            description = "Needs more preparation and structured learning"
            next_steps = ["Focus on core concepts", "Practice regularly", "Seek mentorship"]
        else:
            level = "Focus Required"
            color = "#EF4444"  # Red
            description = "Requires dedicated preparation and fundamentals review"
            next_steps = ["Review basics thoroughly", "Practice daily", "Consider foundational courses"]
        
        return {
            "level": level,
            "color": color,
            "description": description,
            "next_steps": next_steps,
            "score_threshold": avg_score
        }
    
    def _generate_recommendations(
        self,
        metadata: ReportMetadata,
        score_breakdown: ScoreBreakdown,
        skill_gaps: List[SkillGapReport],
        strengths: List[str],
        weaknesses: List[str]
    ) -> List[str]:
        """Generate personalized recommendations."""
        recommendations = []
        avg_score = metadata.average_score
        
        # General recommendations based on performance
        if avg_score < 6:
            recommendations.extend([
                f"📚 Intensive review of {metadata.role} fundamentals",
                "🎯 Focus on one topic at a time until mastery achieved",
                "📝 Practice explaining solutions verbally before coding",
                "⏰ Dedicate 1-2 hours daily to structured interview prep"
            ])
        elif avg_score < 8:
            recommendations.extend([
                f"🚀 Advance to more challenging {metadata.role} problems",
                "💻 Build portfolio projects to apply theoretical knowledge",
                "📖 Study system design and architecture patterns",
                "👥 Join mock interview groups for peer feedback"
            ])
        else:
            recommendations.extend([
                "🎯 Focus on edge cases and optimization techniques",
                "🏗️ Practice large-scale system design scenarios",
                "👥 Consider conducting mock interviews for others",
                "📈 Maintain skills with regular practice sessions"
            ])
        
        # Skill-specific recommendations
        high_priority_gaps = [gap for gap in skill_gaps if gap.severity == "High"]
        if high_priority_gaps:
            recommendations.append(
                f"⚡ Address {len(high_priority_gaps)} critical skill gaps: "
                f"{', '.join([gap.category for gap in high_priority_gaps[:3]])}"
            )
        
        # Add general professional development
        recommendations.extend([
            "📊 Track progress with regular self-assessment",
            "📚 Stay current with industry trends and technologies",
            "🤝 Network with professionals in target role",
            "🎯 Set specific, measurable interview preparation goals"
        ])
        
        return recommendations
    
    def _generate_default_learning_path(self, metadata: ReportMetadata) -> Dict[str, Any]:
        """Generate default learning path when none provided."""
        avg_score = metadata.average_score
        
        if avg_score >= 8:
            duration = 4
            focus = "Maintain excellence and stay current"
        elif avg_score >= 6:
            duration = 8
            focus = "Address moderate skill gaps"
        elif avg_score >= 4:
            duration = 12
            focus = "Build fundamental skills"
        else:
            duration = 16
            focus = "Comprehensive foundation building"
        
        return {
            "title": f"{duration}-Week {metadata.role} Preparation Plan",
            "description": f"Structured learning path based on {metadata.candidate_name}'s assessment",
            "duration_weeks": duration,
            "focus_areas": [focus],
            "phases": [
                {
                    "name": "Foundation Building",
                    "duration_weeks": max(2, duration // 4),
                    "objectives": ["Master core concepts", "Build confidence"],
                    "activities": ["Daily practice", "Concept review", "Basic problem solving"]
                },
                {
                    "name": "Skill Development",
                    "duration_weeks": max(3, duration // 3),
                    "objectives": ["Address identified gaps", "Improve weak areas"],
                    "activities": ["Targeted practice", "Advanced problems", "Peer review"]
                },
                {
                    "name": "Interview Preparation",
                    "duration_weeks": max(2, duration // 4),
                    "objectives": ["Mock interviews", "Final refinement"],
                    "activities": ["Practice interviews", "Time management", "Stress preparation"]
                }
            ]
        }
    
    def _analyze_questions(
        self,
        question_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze question patterns and performance."""
        if not question_history:
            return {}
        
        # Categorize questions and performance
        category_performance = {}
        difficulty_distribution = {}
        
        for qa in question_history:
            category = qa.get("category", "Unknown")
            difficulty = qa.get("difficulty", "medium")
            score = qa.get("score", 5.0)
            
            # Track category performance
            if category not in category_performance:
                category_performance[category] = {"scores": [], "count": 0}
            category_performance[category]["scores"].append(score)
            category_performance[category]["count"] += 1
            
            # Track difficulty distribution
            difficulty_distribution[difficulty] = difficulty_distribution.get(difficulty, 0) + 1
        
        # Calculate averages
        category_averages = {}
        for category, data in category_performance.items():
            avg_score = sum(data["scores"]) / len(data["scores"])
            category_averages[category] = {
                "average_score": round(avg_score, 2),
                "question_count": data["count"],
                "performance_level": self._get_performance_label(avg_score)
            }
        
        return {
            "total_questions": len(question_history),
            "category_performance": category_averages,
            "difficulty_distribution": difficulty_distribution,
            "performance_insights": self._generate_performance_insights(category_averages)
        }
    
    def _get_performance_label(self, score: float) -> str:
        """Convert score to performance label."""
        if score >= 8:
            return "Excellent"
        elif score >= 6:
            return "Good"
        elif score >= 4:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _generate_performance_insights(
        self,
        category_averages: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """Generate insights from category performance data."""
        insights = []
        
        if not category_averages:
            return insights
        
        # Find strongest and weakest categories
        categories_by_score = sorted(
            category_averages.items(),
            key=lambda x: x[1]["average_score"],
            reverse=True
        )
        
        if categories_by_score:
            best_category, best_data = categories_by_score[0]
            insights.append(f"🏆 Strongest area: {best_category} ({best_data['average_score']}/10)")
        
        if len(categories_by_score) > 1:
            worst_category, worst_data = categories_by_score[-1]
            if worst_data["average_score"] < 6:
                insights.append(f"⚠️  Needs attention: {worst_category} ({worst_data['average_score']}/10)")
        
        # Overall pattern insights
        avg_scores = [data["average_score"] for data in category_averages.values()]
        overall_avg = sum(avg_scores) / len(avg_scores)
        
        if max(avg_scores) - min(avg_scores) > 3:
            insights.append("📊 Performance varies significantly across topics - focus on balanced preparation")
        elif overall_avg >= 7:
            insights.append("📈 Consistent strong performance across topics")
        elif overall_avg >= 5:
            insights.append("🎯 Moderate performance with room for improvement in all areas")
        else:
            insights.append("🔧 Fundamental preparation needed across multiple topics")
        
        return insights[:3]  # Limit to 3 key insights
    
    def _generate_visual_data(
        self,
        metadata: ReportMetadata,
        score_breakdown: ScoreBreakdown,
        skill_gaps: List[SkillGapReport]
    ) -> Dict[str, Any]:
        """Generate data suitable for visualization."""
        # Score visualization data
        score_data = {
            "dimensions": ["Correctness", "Depth", "Clarity", "Overall"],
            "scores": [
                score_breakdown.correctness,
                score_breakdown.depth,
                score_breakdown.clarity,
                score_breakdown.overall
            ],
            "max_score": 10
        }
        
        # Skill gap visualization data
        gap_data = {
            "categories": [gap.category for gap in skill_gaps[:5]],  # Top 5 gaps
            "current_levels": [gap.current_level for gap in skill_gaps[:5]],
            "target_levels": [gap.target_level for gap in skill_gaps[:5]],
            "gap_sizes": [gap.gap_size for gap in skill_gaps[:5]]
        }
        
        # Readiness visualization
        readiness_score = self._calculate_readiness_score(metadata.average_score)
        
        return {
            "score_chart": score_data,
            "skill_gap_chart": gap_data,
            "readiness_meter": {
                "score": readiness_score,
                "max_score": 100,
                "level": self._assess_readiness(metadata.average_score)["level"]
            },
            "confidence_band": score_breakdown.confidence_band
        }
    
    def _calculate_readiness_score(self, avg_score: float) -> int:
        """Convert average score to readiness percentage."""
        # Map 0-10 score to 0-100 readiness
        return min(100, max(0, int(avg_score * 10)))
    
    def export_to_json(self, report: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Export report to JSON format.
        
        Args:
            report: Complete report dictionary
            filename: Optional filename for saving
            
        Returns:
            JSON string or file path if filename provided
        """
        json_content = json.dumps(report, indent=2, ensure_ascii=False)
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json_content)
            return filename
        else:
            return json_content
    
    def export_to_text(self, report: Dict[str, Any]) -> str:
        """
        Export report to formatted text.
        
        Args:
            report: Complete report dictionary
            
        Returns:
            Formatted text report
        """
        lines = []
        
        # Header
        metadata = report["metadata"]
        lines.extend([
            "=" * 60,
            f"INTERVIEW ASSESSMENT REPORT",
            "=" * 60,
            f"Candidate: {metadata['candidate_name']}",
            f"Role: {metadata['role']} ({metadata['experience_level']} level)",
            f"Date: {datetime.fromisoformat(metadata['interview_date']).strftime('%B %d, %Y')}",
            f"Duration: {metadata['duration_minutes']} minutes",
            "=" * 60,
            ""
        ])
        
        # Executive Summary
        lines.extend([
            "EXECUTIVE SUMMARY",
            "-" * 20,
            report["executive_summary"],
            ""
        ])
        
        # Readiness Assessment
        readiness = report["readiness_assessment"]
        lines.extend([
            "READINESS ASSESSMENT",
            "-" * 20,
            f"Level: {readiness['level']}",
            f"Description: {readiness['description']}",
            f"Score: {metadata['average_score']:.1f}/10",
            ""
        ])
        
        # Detailed Scores
        scores = report["detailed_scores"]
        lines.extend([
            "DETAILED SCORE BREAKDOWN",
            "-" * 25,
            f"Overall Score: {scores['overall']}/10 ({scores['confidence_band']} confidence)",
            f"Correctness: {scores['correctness']}/10",
            f"Depth: {scores['depth']}/10",
            f"Clarity: {scores['clarity']}/10",
            f"Explanation: {scores['explanation']}",
            ""
        ])
        
        # Strengths and Weaknesses
        if report["strengths"]:
            lines.extend([
                "KEY STRENGTHS",
                "-" * 15
            ])
            for strength in report["strengths"][:5]:
                lines.append(f"• {strength}")
            lines.append("")
        
        if report["weaknesses"]:
            lines.extend([
                "AREAS FOR IMPROVEMENT",
                "-" * 22
            ])
            for weakness in report["weaknesses"][:5]:
                lines.append(f"• {weakness}")
            lines.append("")
        
        # Skill Gaps
        if report["skill_gaps"]:
            lines.extend([
                "IDENTIFIED SKILL GAPS",
                "-" * 20
            ])
            for gap in report["skill_gaps"][:3]:
                lines.extend([
                    f"Category: {gap['category']}",
                    f"Severity: {gap['severity']}",
                    f"Current: {gap['current_level']}/10 → Target: {gap['target_level']}/10",
                    f"Gap Size: {gap['gap_size']}",
                    "Recommendations:"
                ])
                for rec in gap["recommendations"][:2]:
                    lines.append(f"  - {rec}")
                lines.append("")
        
        # Recommendations
        lines.extend([
            "PERSONALIZED RECOMMENDATIONS",
            "-" * 28
        ])
        for rec in report["recommendations"][:6]:
            lines.append(f"• {rec}")
        lines.append("")
        
        # Footer
        lines.extend([
            "=" * 60,
            "Generated by AI Interview Agent",
            f"Report ID: {metadata['report_id']}",
            "=" * 60
        ])
        
        return "\n".join(lines)
    
    def export_to_pdf(self, report: Dict[str, Any], filename: str) -> str:
        """
        Export report to PDF format.
        Note: This is a simplified implementation. In production, use a proper PDF library.
        
        Args:
            report: Complete report dictionary
            filename: Output filename
            
        Returns:
            Filename of generated PDF
        """
        try:
            # Try to import PDF generation library
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib import colors
            
            # Create PDF document
            doc = SimpleDocTemplate(filename, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Add content (simplified - would need more detailed implementation)
            # This is a placeholder showing the concept
            story.append(Paragraph("Interview Assessment Report", styles['Title']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"Candidate: {report['metadata']['candidate_name']}", styles['Normal']))
            story.append(Paragraph(f"Role: {report['metadata']['role']}", styles['Normal']))
            story.append(Spacer(1, 12))
            story.append(Paragraph("Detailed report content would be generated here...", styles['Normal']))
            
            doc.build(story)
            return filename
            
        except ImportError:
            # Fallback to text file if PDF library not available
            text_content = self.export_to_text(report)
            txt_filename = filename.replace('.pdf', '.txt')
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(text_content)
            return txt_filename
    
    def get_export_options(self) -> List[Dict[str, str]]:
        """Get available export format options."""
        return [
            {"format": "json", "description": "Structured JSON data", "extension": ".json"},
            {"format": "text", "description": "Formatted text report", "extension": ".txt"},
            {"format": "pdf", "description": "Professional PDF document", "extension": ".pdf"}
        ]