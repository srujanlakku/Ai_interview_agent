#!/usr/bin/env python3
"""
AI Interview Agent - Production Web Application
A production-ready, enterprise-grade interview preparation platform.

Usage:
    streamlit run app.py

Opens at: http://localhost:8501
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# Ensure the app directory is in path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup logging
from app.utils.structured_logging import setup_logging
setup_logging()

# Production utilities
from app.utils.session_manager import init_production_session, save_current_session
from app.utils.navigation_guard import check_navigation_safety, safe_page_redirect, is_interview_in_progress
from app.utils.versioning import get_app_version, get_branding, get_footer
from app.utils.error_handler_prod import handle_exception, safe_call
from app.components.ui_components import show_loading, show_success, show_error

import streamlit as st
import time

# Configure Streamlit page
st.set_page_config(
    page_title="AI Interview Agent | Master Your Technical Interviews",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    """Load custom CSS for stunning UI."""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --primary: #6366F1;
        --primary-dark: #4F46E5;
        --secondary: #EC4899;
        --accent: #14B8A6;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --dark: #1E1B4B;
        --light: #F8FAFC;
        --glass-bg: rgba(255, 255, 255, 0.15);
        --glass-border: rgba(255, 255, 255, 0.2);
    }
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .glass-card-dark {
        background: rgba(30, 27, 75, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
        color: white;
    }
    
    /* Hero Section */
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Animated Badge */
    .badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
        animation: pulse 2s infinite;
    }
    
    .badge-primary {
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        color: white;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #10B981, #14B8A6);
        color: white;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #F59E0B, #FBBF24);
        color: #1E1B4B;
    }
    
    .badge-danger {
        background: linear-gradient(135deg, #EF4444, #F87171);
        color: white;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        color: white;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
    }
    
    /* Question Box */
    .question-container {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(139, 92, 246, 0.3));
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        margin: 1.5rem 0;
    }
    
    .question-header {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .question-tag {
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .tag-type {
        background: rgba(99, 102, 241, 0.8);
        color: white;
    }
    
    .tag-difficulty {
        background: rgba(245, 158, 11, 0.8);
        color: white;
    }
    
    .tag-topic {
        background: rgba(20, 184, 166, 0.8);
        color: white;
    }
    
    .question-text {
        color: white;
        font-size: 1.25rem;
        line-height: 1.8;
        font-weight: 500;
    }
    
    /* Score Display */
    .score-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        position: relative;
        background: conic-gradient(var(--score-color) var(--score-percent), rgba(255,255,255,0.1) 0);
    }
    
    .score-circle::before {
        content: '';
        position: absolute;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: rgba(30, 27, 75, 0.9);
    }
    
    .score-value {
        position: relative;
        z-index: 1;
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
    }
    
    .score-label {
        position: relative;
        z-index: 1;
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* Progress Bar */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #6366F1, #EC4899);
        transition: width 0.5s ease;
    }
    
    /* Chat Message */
    .chat-message {
        display: flex;
        margin: 1rem 0;
        animation: fadeIn 0.3s ease;
    }
    
    .chat-message.interviewer {
        justify-content: flex-start;
    }
    
    .chat-message.candidate {
        justify-content: flex-end;
    }
    
    .message-bubble {
        max-width: 80%;
        padding: 1rem 1.5rem;
        border-radius: 20px;
        position: relative;
    }
    
    .interviewer .message-bubble {
        background: rgba(99, 102, 241, 0.3);
        border: 1px solid rgba(99, 102, 241, 0.5);
        border-bottom-left-radius: 4px;
    }
    
    .candidate .message-bubble {
        background: rgba(20, 184, 166, 0.3);
        border: 1px solid rgba(20, 184, 166, 0.5);
        border-bottom-right-radius: 4px;
    }
    
    .message-text {
        color: white;
        line-height: 1.6;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Metric Card */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Feedback Section */
    .feedback-positive {
        background: rgba(16, 185, 129, 0.2);
        border-left: 4px solid #10B981;
        padding: 1rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 0.5rem 0;
    }
    
    .feedback-negative {
        background: rgba(239, 68, 68, 0.2);
        border-left: 4px solid #EF4444;
        padding: 1rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 0.5rem 0;
    }
    
    .feedback-text {
        color: white;
        font-size: 0.95rem;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
    }
    
    /* Text Input Styles */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background: rgba(30, 27, 75, 0.95) !important;
        backdrop-filter: blur(20px);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Slider */
    .stSlider > div > div {
        background: linear-gradient(90deg, #6366F1, #EC4899) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* Selectbox dropdown */
    [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Animation Classes */
    .animate-float {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .animate-glow {
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px rgba(99, 102, 241, 0.5); }
        to { box-shadow: 0 0 40px rgba(236, 72, 153, 0.5); }
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    defaults = {
        "page": "home",
        "logged_in": False,
        "candidate_name": "",
        "role": "",
        "experience_level": "",
        "company": "",
        "interview_active": False,
        "interview_complete": False,
        "current_question": None,
        "question_number": 0,
        "max_questions": 8,
        "difficulty": "medium",
        "asked_ids": [],
        "asked_topics": [],
        "chat_history": [],
        "scores": [],
        "strengths": [],
        "weaknesses": [],
        "showing_feedback": False,
        "last_evaluation": None,
        # New multi-agent orchestration
        "orchestrator_agent": None,
        "session_id": None,
        # Resume upload
        "uploaded_resume": None,
        "resume_skills": [],
        "resume_projects": [],
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def check_api_key():
    """Check if OpenAI API key is configured."""
    return bool(os.getenv("OPENAI_API_KEY"))


# Import page renderers
from pages.home_page import render_home_page
from pages.login_page import render_login_page
from pages.interview_page import render_interview_page
from pages.results_page import render_results_page
from pages.history_page import render_history_page
from pages.admin_page import render_admin_page


def render_sidebar():
    """Render enhanced sidebar with production features."""
    with st.sidebar:
        # Branding header with version
        branding = get_branding()
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
            <h2 style="color: white; margin: 0; font-size: 1.5rem;">{branding['name']}</h2>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 0.25rem;">
                {branding['tagline']}
            </div>
            <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin-top: 0.5rem;">
                {branding['version']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.session_state.get("logged_in", False):
            st.markdown(f"""
            <div class="glass-card" style="padding: 1rem;">
                <p style="color: rgba(255,255,255,0.7); margin: 0; font-size: 0.85rem;">Welcome back,</p>
                <h3 style="color: white; margin: 0.25rem 0;">{st.session_state.get('candidate_name', 'User')}</h3>
                <p style="color: rgba(255,255,255,0.6); margin: 0; font-size: 0.8rem;">
                    {st.session_state.get('role', 'N/A')}<br/>
                    {st.session_state.get('experience_level', 'N/A').title()} Level
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Interview progress with safe navigation
            if st.session_state.get("interview_active", False):
                st.markdown("### 📊 Interview Progress")
                progress = st.session_state.get("question_number", 0) / st.session_state.get("max_questions", 8)
                st.progress(progress)
                st.caption(f"Question {st.session_state.get('question_number', 0)}/{st.session_state.get('max_questions', 8)}")
                
                if st.session_state.get("scores"):
                    avg = sum(st.session_state["scores"]) / len(st.session_state["scores"])
                    st.metric("Average Score", f"{avg:.1f}/10")
                
                st.metric("Difficulty", st.session_state.get("difficulty", "medium").title())
            
            st.markdown("---")
            
            # Safe navigation buttons
            if st.button("🏠 Home", use_container_width=True, key="nav_home"):
                if check_navigation_safety("home"):
                    safe_page_redirect("home")
            
            if st.button("📜 History", use_container_width=True, key="nav_history"):
                if check_navigation_safety("history"):
                    safe_page_redirect("history")
            
            if st.button("📊 Admin", use_container_width=True, key="nav_admin"):
                if check_navigation_safety("admin"):
                    safe_page_redirect("admin")
            
            if st.button("🚪 Logout", use_container_width=True, key="nav_logout"):
                # Safe logout with session cleanup
                from app.utils.session_manager import clear_interview_session
                clear_interview_session()
                st.session_state.clear()
                st.rerun()
        else:
            st.markdown("""
            <div style="text-align: center; color: rgba(255,255,255,0.8); padding: 1rem;">
                <p>Start your interview preparation journey today!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced footer with links
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.75rem; padding: 1rem 0;">
            <div>{get_footer()}</div>
            <div style="margin-top: 0.5rem;">
                <a href="#" style="color: rgba(255,255,255,0.5); text-decoration: none; margin: 0 0.5rem;">Privacy</a>
                <a href="#" style="color: rgba(255,255,255,0.5); text-decoration: none; margin: 0 0.5rem;">Terms</a>
                <a href="#" style="color: rgba(255,255,255,0.5); text-decoration: none; margin: 0 0.5rem;">Help</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application entry point with production enhancements."""
    try:
        # Load CSS
        load_css()
        
        # Initialize production session management
        session_id = init_production_session()
        
        # Auto-save session periodically
        save_current_session()
        
        # Render sidebar with version info
        render_sidebar()
        
        # Check API key with graceful error handling
        if not safe_call(check_api_key, error_context="API key validation"):
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h2 style="color: white;">⚠️ Configuration Required</h2>
                <p style="color: rgba(255,255,255,0.8);">
                    Please configure your OpenAI API key to continue.
                </p>
                <ol style="text-align: left; color: rgba(255,255,255,0.9); padding-left: 2rem;">
                    <li>Create a <code>.env</code> file in the backend directory</li>
                    <li>Add: <code>OPENAI_API_KEY=your_key_here</code></li>
                    <li>Restart the application</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Route to appropriate page with navigation safety
        current_page = st.session_state.get("page", "home")
        
        # Handle pending navigation
        pending_nav = st.session_state.get("_pending_navigation")
        if pending_nav and check_navigation_safety(pending_nav):
            safe_page_redirect(pending_nav)
            return
        
        # Route based on authentication and interview state
        page_rendered = False
        
        if not st.session_state.get("logged_in", False):
            if current_page == "login":
                render_login_page()
                page_rendered = True
            elif current_page == "history":
                render_history_page()
                page_rendered = True
            elif current_page == "admin":
                render_admin_page()
                page_rendered = True
                
        elif st.session_state.get("interview_complete", False):
            render_results_page()
            page_rendered = True
        elif st.session_state.get("interview_active", False):
            render_interview_page()
            page_rendered = True
        elif current_page == "history":
            render_history_page()
            page_rendered = True
        elif current_page == "admin":
            render_admin_page()
            page_rendered = True
            
        # Render home page if no other page was rendered
        if not page_rendered:
            render_home_page()
            
    except Exception as e:
        # Handle any uncaught exceptions gracefully
        handle_exception(e, "Main application execution")
        
        # Show friendly error page
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 2rem;">
            <h2 style="color: white;">😅 Something Unexpected Happened</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 1rem 0;">
                We've logged the issue and our team will look into it.
            </p>
            <button onclick="location.reload()" style="
                background: var(--primary);
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                font-size: 1rem;
                cursor: pointer;
                margin: 0.5rem;
            ">🔄 Refresh Page</button>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
