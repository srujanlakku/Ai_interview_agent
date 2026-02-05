"""
History Page - View past interview records.
"""
import streamlit as st
from app.utils.history_db import get_history_db


def render_history_page():
    """Render the interview history page."""
    
    # Back button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back", key="history_back_btn"):
            st.session_state.page = "home"
            st.rerun()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📜</div>
        <h1 style="color: white; font-family: 'Poppins', sans-serif; font-weight: 700; margin: 0;">
            Interview History
        </h1>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin-top: 0.5rem;">
            View your past interview performances and track progress
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize database
    db = get_history_db()
    
    # Get all interviews
    interviews = db.get_all_interviews()
    
    if not interviews:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: white; margin: 1rem 0;">No Interview History Yet</h3>
            <p style="color: rgba(255,255,255,0.7); margin: 1rem 0;">
                Complete your first interview to see it appear here.<br/>
                Your interview history will be saved automatically.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        candidate_filter = st.selectbox(
            "Filter by Candidate",
            options=["All"] + list(set(interview["candidate_name"] for interview in interviews)),
            key="candidate_filter"
        )
    
    with col2:
        role_filter = st.selectbox(
            "Filter by Role",
            options=["All"] + list(set(interview["role"] for interview in interviews)),
            key="role_filter"
        )
    
    with col3:
        exp_filter = st.selectbox(
            "Filter by Experience",
            options=["All"] + list(set(interview["experience_level"] for interview in interviews)),
            key="exp_filter"
        )
    
    # Apply filters
    filtered_interviews = interviews
    if candidate_filter != "All":
        filtered_interviews = [i for i in filtered_interviews if i["candidate_name"] == candidate_filter]
    if role_filter != "All":
        filtered_interviews = [i for i in filtered_interviews if i["role"] == role_filter]
    if exp_filter != "All":
        filtered_interviews = [i for i in filtered_interviews if i["experience_level"] == exp_filter]
    
    # Show statistics
    if filtered_interviews:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(filtered_interviews)}</div>
                <div class="metric-label">Total Interviews</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_score = sum(i["final_score"] for i in filtered_interviews if i["final_score"]) / len([i for i in filtered_interviews if i["final_score"]])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_score:.1f}</div>
                <div class="metric-label">Avg Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_questions = sum(i["total_questions"] for i in filtered_interviews)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_questions}</div>
                <div class="metric-label">Total Questions</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Display interviews
    for interview in filtered_interviews:
        with st.container():
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <h3 style="color: white; margin: 0; font-size: 1.3rem;">{interview['candidate_name']}</h3>
                        <p style="color: rgba(255,255,255,0.7); margin: 0.25rem 0 0 0; font-size: 0.9rem;">
                            {interview['role']} • {interview['experience_level'].title()} Level
                            {f' • {interview["company"]}' if interview['company'] else ''}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 2rem; font-weight: 800; color: white; margin-bottom: -0.25rem;">
                            {interview['final_score']:.1f}
                        </div>
                        <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">/10 Avg</div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 1rem; margin-top: 1rem; font-size: 0.85rem;">
                    <span class="badge badge-primary">Q: {interview['total_questions']}</span>
                    <span class="badge badge-success">{interview['created_at'][:10]}</span>
                    <span class="badge badge-warning">ID: {interview['session_id'][:6]}</span>
                </div>
                
                <div style="margin-top: 1rem;">
                    <details style="color: rgba(255,255,255,0.8);">
                        <summary style="cursor: pointer; padding: 0.5rem 0;">Show Details</summary>
                        <div style="padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; margin-top: 0.5rem;">
                            <p><strong>Started:</strong> {interview['started_at']}</p>
                            <p><strong>Ended:</strong> {interview['ended_at']}</p>
                        </div>
                    </details>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Show overall stats
    if interviews:
        stats = db.get_performance_stats()
        st.markdown("""
        <h3 style="color: white; font-family: 'Poppins', sans-serif; margin: 2rem 0 1rem 0;">
            📊 Overall Statistics
        </h3>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0;">
                <strong>Total Interviews:</strong> {stats['total_interviews']}<br/>
                <strong>Average Score:</strong> {stats['average_score']}/10
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_history_page()
