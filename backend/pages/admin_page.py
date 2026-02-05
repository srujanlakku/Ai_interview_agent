"""
Admin/Review Page - Compare candidates and view aggregate results.
"""
import streamlit as st
import pandas as pd
from app.utils.history_db import get_history_db


def render_admin_page():
    """Render the admin/review page for comparing candidates."""
    
    # Back button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back", key="admin_back_btn"):
            st.session_state.page = "home"
            st.rerun()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
        <h1 style="color: white; font-family: 'Poppins', sans-serif; font-weight: 700; margin: 0;">
            Admin Dashboard
        </h1>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin-top: 0.5rem;">
            View and compare candidate performance across interviews
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize database
    db = get_history_db()
    
    # Get overall stats
    stats = db.get_performance_stats()
    
    # Stats overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['total_interviews']}</div>
            <div class="metric-label">Total Interviews</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['average_score']:.1f}</div>
            <div class="metric-label">Avg Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(stats['by_role'])}</div>
            <div class="metric-label">Roles Tracked</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(stats['by_experience'])}</div>
            <div class="metric-label">Experience Levels</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👥 Candidates", "💼 By Role", "📈 Performance"])
    
    with tab1:
        # Role distribution chart
        if stats['by_role']:
            df_roles = pd.DataFrame(stats['by_role'])
            st.markdown("### Interviews by Role")
            st.bar_chart(df_roles.set_index('role')['count'])
        
        # Experience distribution chart
        if stats['by_experience']:
            df_exp = pd.DataFrame(stats['by_experience'])
            st.markdown("### Interviews by Experience Level")
            st.bar_chart(df_exp.set_index('level')['count'])
    
    with tab2:
        # All candidates table
        all_interviews = db.get_all_interviews()
        
        if all_interviews:
            df_candidates = pd.DataFrame(all_interviews)
            df_candidates = df_candidates[['candidate_name', 'role', 'experience_level', 'final_score', 'total_questions', 'created_at']]
            df_candidates = df_candidates.rename(columns={
                'candidate_name': 'Name',
                'role': 'Role',
                'experience_level': 'Experience',
                'final_score': 'Score',
                'total_questions': 'Questions',
                'created_at': 'Date'
            })
            
            st.dataframe(
                df_candidates,
                column_config={
                    "Score": st.column_config.NumberColumn(format="%.2f"),
                    "Date": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No interviews recorded yet.")
    
    with tab3:
        # Performance by role
        if stats['by_role']:
            df_role_perf = pd.DataFrame(stats['by_role'])
            df_role_perf = df_role_perf.rename(columns={
                'role': 'Role',
                'count': 'Interviews',
                'avg_score': 'Avg Score'
            })
            
            st.markdown("### Average Performance by Role")
            st.dataframe(df_role_perf, hide_index=True, use_container_width=True)
            
            # Top performers by role
            st.markdown("### Top Performers by Role")
            for role_stat in stats['by_role']:
                role_interviews = db.get_interviews_by_role(role_stat['role'])
                if role_interviews:
                    top_performers = sorted(role_interviews, key=lambda x: x['final_score'] or 0, reverse=True)[:5]
                    st.markdown(f"#### {role_stat['role']}")
                    for perf in top_performers:
                        st.markdown(f"- **{perf['candidate_name']}**: {perf['final_score']:.2f}/10")
    
    with tab4:
        # Performance trends
        if all_interviews:
            df_trends = pd.DataFrame(all_interviews)
            df_trends['date'] = pd.to_datetime(df_trends['created_at']).dt.date
            daily_avg = df_trends.groupby('date')['final_score'].mean().reset_index()
            
            if not daily_avg.empty:
                st.markdown("### Daily Average Performance")
                st.line_chart(daily_avg.set_index('date')['final_score'])
        
        # Experience vs Score scatter plot
        if all_interviews:
            df_scatter = pd.DataFrame([
                {
                    'Experience': i['experience_level'],
                    'Score': i['final_score'],
                    'Role': i['role']
                } 
                for i in all_interviews if i['final_score'] is not None
            ])
            
            if not df_scatter.empty:
                st.markdown("### Score Distribution by Experience")
                st.scatter_chart(
                    df_scatter,
                    x='Experience',
                    y='Score',
                    color='Role',
                    size=50
                )
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Export functionality
    st.markdown("### 📥 Export Data")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export All Data (JSON)", use_container_width=True):
            all_data = {
                "metadata": {
                    "export_date": pd.Timestamp.now().isoformat(),
                    "total_interviews": stats['total_interviews'],
                    "average_score": stats['average_score']
                },
                "interviews": db.get_all_interviews(),
                "statistics": stats
            }
            st.download_button(
                label="Download JSON",
                data=pd.json.dumps(all_data, indent=2),
                file_name=f"interview_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("Export All Data (CSV)", use_container_width=True):
            all_interviews = db.get_all_interviews()
            df_export = pd.DataFrame(all_interviews)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"interview_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("Export Summary (PDF)", use_container_width=True):
            # This would require additional PDF generation libraries
            st.info("PDF export coming soon!")


if __name__ == "__main__":
    render_admin_page()
