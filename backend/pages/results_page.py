"""
Results Page - Comprehensive interview results with charts and recommendations.
"""
import streamlit as st
import json
from datetime import datetime
from app.utils.history_db import get_history_db
from app.utils.structured_logging import log_interview_end


def get_readiness_level(avg_score: float) -> tuple:
    """Get readiness level and description."""
    if avg_score >= 8.5:
        return "🏆 Interview Ready", "#10B981", "You're exceptionally well-prepared!"
    elif avg_score >= 7.0:
        return "✅ Well Prepared", "#22C55E", "Strong performance with minor areas to refine."
    elif avg_score >= 5.5:
        return "📈 Making Progress", "#F59E0B", "Good foundation, continue practicing."
    elif avg_score >= 4.0:
        return "📚 Keep Practicing", "#F97316", "Focus on fundamentals and core concepts."
    else:
        return "🎯 Focus Required", "#EF4444", "Dedicate more time to preparation."


def render_score_ring(score: float, label: str, size: int = 120):
    """Render a cyber-styled score indicator."""
    return f"""
    <div style="text-align: center;">
        <div style="
            width: {size}px; height: {size}px;
            border: 3px solid #FF0000;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            margin: 0 auto;
            background: #000000;
        ">
            <div style="
                width: {size - 15}px; height: {size - 15}px;
                border-radius: 50%;
                background: #000000;
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
            ">
                <span style="font-size: {size // 4}px; font-weight: 800; color: #FF0000; font-family: 'Courier New', monospace;">{score:.1f}</span>
                <span style="font-size: {size // 10}px; color: #FFFFFF; font-family: 'Courier New', monospace;">/10</span>
            </div>
        </div>
        <p style="color: #FF0000; margin-top: 0.5rem; font-weight: 500; font-family: 'Courier New', monospace;">>> {label.upper()} <<</p>
    </div>
    """


def render_bar_chart(scores: list, labels: list, max_val: float = 10):
    """Render a cyber-styled bar chart."""
    html = '<div style="display: flex; gap: 1rem; align-items: flex-end; height: 150px; padding: 1rem 0;">'
    
    for score, label in zip(scores, labels):
        height = (score / max_val) * 100
        
        html += f"""
        <div style="flex: 1; text-align: center;">
            <div style="
                height: {height}%;
                background: #000000;
                border: 2px solid #FF0000;
                border-radius: 8px 8px 0 0;
                min-height: 10px;
                display: flex; align-items: flex-start; justify-content: center;
                padding-top: 0.5rem;
            ">
                <span style="color: #FF0000; font-weight: 700; font-size: 0.85rem; font-family: 'Courier New', monospace;">{score:.1f}</span>
            </div>
            <p style="color: #FF0000; font-size: 0.75rem; margin-top: 0.5rem; font-family: 'Courier New', monospace;">{label}</p>
        </div>
        """
    
    html += '</div>'
    return html


def render_results_page():
    """Render the comprehensive results page with cyber aesthetic."""
    
    # Add cyber grid background
    st.markdown('<div class="cyber-grid"></div>', unsafe_allow_html=True)
    
    # Calculate statistics
    scores = st.session_state.scores or [5]
    avg_score = sum(scores) / len(scores)
    best_score = max(scores)
    lowest_score = min(scores)
    
    readiness, readiness_color, readiness_desc = get_readiness_level(avg_score)
    
    # Save interview to database if orchestrator exists
    if hasattr(st.session_state, 'orchestrator_agent') and st.session_state.orchestrator_agent and st.session_state.session_id:
        try:
            # Finalize the session to get complete results
            orchestrator = st.session_state.orchestrator_agent
            session_id = st.session_state.session_id
            session_summary = orchestrator.finalize_session(session_id)
            
            # Save to database
            db = get_history_db()
            db.save_interview(session_summary)
            
            # Log interview end
            log_interview_end(
                session_id=session_id,
                final_score=avg_score,
                total_questions=len(scores)
            )
        except Exception as e:
            st.error(f"Error saving interview to database: {str(e)}")
    
    # Header
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem; color: #FF0000;">[!]</div>
        <h1 style="color: white; font-family: 'Courier New', monospace; font-weight: 700; margin: 0; text-shadow: 0 0 10px #FF0000;">
            >> INTERVIEW PROTOCOL COMPLETE <<
        </h1>
        <p style="color: #FF0000; font-size: 1.1rem; margin-top: 0.5rem; font-family: 'Courier New', monospace;">
            >> EXCELLENT PERFORMANCE, {st.session_state.candidate_name.upper()}! HERE IS YOUR DETAILED ANALYSIS <<
        </p>
        <div class="status-indicator status-active" style="margin: 1rem auto;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Readiness Badge
    st.markdown(f"""
    <div class="interview-card" style="text-align: center; max-width: 500px; margin: 0 auto 2rem auto; border: 2px solid #FF0000;">
        <h2 style="color: #FF0000; margin: 0; font-size: 1.8rem; font-family: 'Courier New', monospace;">>> {readiness.upper()} <<</h2>
        <p style="color: #FFFFFF; margin: 0.5rem 0 0 0; font-family: 'Courier New', monospace;">{readiness_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Score Display
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(render_score_ring(avg_score, "Overall Score", 180), unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Detailed Metrics
    st.markdown("""
    <h2 style="color: white; text-align: center; font-family: 'Courier New', monospace; margin: 2rem 0; text-shadow: 0 0 10px #FF0000;">
        >> PERFORMANCE BREAKDOWN <<
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("Questions", len(scores), "📝"),
        ("Best Score", f"{best_score}/10", "🏆"),
        ("Lowest Score", f"{lowest_score}/10", "📉"),
        ("Consistency", f"{100 - (max(scores) - min(scores)) * 10:.0f}%", "🎯")
    ]
    
    for col, (label, value, icon) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="interview-card" style="text-align: center; border: 2px solid #FF0000;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem; color: #FF0000;">{icon}</div>
                <div class="metric-value" style="color: #FF0000; font-family: 'Courier New', monospace;">{value}</div>
                <div class="metric-label" style="color: #FFFFFF; font-family: 'Courier New', monospace;">>> {label.upper()} <<</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Score Progression Chart
    if len(scores) > 1:
        st.markdown("""
        <h3 style="color: white; font-family: 'Courier New', monospace; margin: 1.5rem 0; text-shadow: 0 0 10px #FF0000;">
            >> SCORE PROGRESSION <<
        </h3>
        """, unsafe_allow_html=True)
        
        labels = [f"Q{i+1}" for i in range(len(scores))]
        st.markdown(f"""
        <div class="interview-card" style="border: 2px solid #FF0000;">
            {render_bar_chart(scores, labels)}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Strengths and Weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="interview-card" style="border: 2px solid #FF0000;">
            <h3 style="color: #FF0000; margin-top: 0; font-family: 'Courier New', monospace;">>> STRENGTHS <<</h3>
        """, unsafe_allow_html=True)
        
        strengths = st.session_state.strengths[:5] if st.session_state.strengths else [
            "Good understanding of fundamentals",
            "Clear communication style",
            "Structured approach to problems"
        ]
        
        for strength in strengths:
            st.markdown(f"""
            <div class="feedback-positive">
                <span class="feedback-text" style="font-family: 'Courier New', monospace;">>> {strength} <<</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="interview-card" style="border: 2px solid #FF0000; opacity: 0.8;">
            <h3 style="color: #FF0000; margin-top: 0; font-family: 'Courier New', monospace;">>> AREAS FOR IMPROVEMENT <<</h3>
        """, unsafe_allow_html=True)
        
        weaknesses = st.session_state.weaknesses[:5] if st.session_state.weaknesses else [
            "Dive deeper into edge cases",
            "Practice time complexity analysis",
            "Strengthen system design knowledge"
        ]
        
        for weakness in weaknesses:
            st.markdown(f"""
            <div class="feedback-negative">
                <span class="feedback-text" style="font-family: 'Courier New', monospace;">>> {weakness} <<</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("""
    <h2 style="color: white; text-align: center; font-family: 'Courier New', monospace; margin: 2rem 0; text-shadow: 0 0 10px #FF0000;">
        >> PERSONALIZED RECOMMENDATIONS <<
    </h2>
    """, unsafe_allow_html=True)
    
    role = st.session_state.role
    exp = st.session_state.experience_level
    
    recommendations = []
    
    if avg_score < 6:
        recommendations.extend([
            f"📚 Review fundamental {role} concepts daily",
            "🎯 Focus on one topic at a time until mastery",
            "📝 Practice explaining solutions out loud",
        ])
    elif avg_score < 8:
        recommendations.extend([
            f"🚀 Tackle more advanced {role} challenges",
            "💻 Build side projects to apply knowledge",
            "📖 Study system design patterns",
        ])
    else:
        recommendations.extend([
            "🎯 Focus on edge cases and optimization",
            "🏗️ Practice large-scale system design",
            "👥 Consider mock interviews with peers",
        ])
    
    recommendations.append(f"⏰ Dedicate 30 min daily for {role} interview prep")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    for rec in recommendations:
        st.markdown(f"""
        <div style="padding: 0.75rem 1rem; margin: 0.5rem 0; 
                    background: rgba(99, 102, 241, 0.2);
                    border-radius: 10px; border-left: 4px solid #6366F1;">
            <span style="color: white;">{rec}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Action Buttons
    st.markdown("""
    <h3 style="color: white; text-align: center; font-family: 'Poppins', sans-serif; margin: 2rem 0 1rem 0;">
        What's Next?
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Practice Again", use_container_width=True, key="retry_btn"):
            # Reset interview state
            st.session_state.interview_active = True
            st.session_state.interview_complete = False
            st.session_state.current_question = None
            st.session_state.question_number = 0
            st.session_state.scores = []
            st.session_state.strengths = []
            st.session_state.weaknesses = []
            st.session_state.chat_history = []
            st.session_state.showing_feedback = False
            st.session_state.last_evaluation = None
            st.session_state.asked_ids = []
            st.session_state.asked_topics = []
            st.rerun()
    
    with col2:
        if st.button("📝 Change Settings", use_container_width=True, key="settings_btn"):
            st.session_state.page = "login"
            st.session_state.interview_complete = False
            st.session_state.interview_active = False
            st.rerun()
    
    with col3:
        # Download results
        results_data = {
            "candidate": st.session_state.candidate_name,
            "role": st.session_state.role,
            "experience_level": st.session_state.experience_level,
            "date": datetime.now().isoformat(),
            "scores": scores,
            "average_score": avg_score,
            "best_score": best_score,
            "strengths": st.session_state.strengths[:5],
            "weaknesses": st.session_state.weaknesses[:5],
            "readiness": readiness
        }
        
        st.download_button(
            label="📥 Download Report",
            data=json.dumps(results_data, indent=2),
            file_name=f"interview_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
            key="download_btn"
        )
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Session Summary
    with st.expander("📋 Full Session Details"):
        st.markdown(f"""
        **Candidate:** {st.session_state.candidate_name}  
        **Role:** {st.session_state.role}  
        **Experience Level:** {st.session_state.experience_level.title()}  
        **Questions Answered:** {len(scores)}  
        **Average Score:** {avg_score:.2f}/10  
        **Readiness Level:** {readiness}
        """)
        
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("**Q&A History:**")
            for i, msg in enumerate(st.session_state.chat_history):
                prefix = "🤖 **Question:**" if msg["role"] == "interviewer" else "👤 **Answer:**"
                st.markdown(f"{prefix} {msg['content'][:300]}...")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.5); padding: 2rem; font-size: 0.85rem;">
        <p>Keep practicing and you'll ace your interviews! 💪</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_results_page()
