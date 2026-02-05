#!/usr/bin/env python3
"""
AI Interview Agent - Streamlit Web Application

A production-ready web-based AI Interview Agent that conducts adaptive technical interviews.

Usage:
    streamlit run streamlit_app.py

Requirements:
    - Python 3.10+
    - OpenAI API key set in environment or .env file
"""
import os
import sys
from pathlib import Path

# Ensure the app directory is in path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

# Configure Streamlit page
st.set_page_config(
    page_title="AI Interview Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Import page modules
from pages.login_page import render_login_page
from pages.interview_page import render_interview_page
from pages.results_page import render_results_page


def init_session_state():
    """Initialize session state variables if they don't exist."""
    defaults = {
        "logged_in": False,
        "candidate_name": "",
        "role": "",
        "experience_level": "",
        "current_page": "login",
        "interview_started": False,
        "interview_completed": False,
        "current_question": None,
        "current_question_num": 0,
        "max_questions": int(os.getenv("INTERVIEW_MAX_QUESTIONS", "8")),
        "asked_question_ids": [],
        "asked_topics": [],
        "current_difficulty": "medium",
        "history": [],
        "all_strengths": [],
        "all_weaknesses": [],
        "total_score": 0.0,
        "question_scores": [],
        "final_report": None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def ensure_directories():
    """Ensure required directories exist."""
    dirs = ["logs", "temp", "pages"]
    base_path = Path(__file__).parent
    
    for dir_name in dirs:
        dir_path = base_path / dir_name
        dir_path.mkdir(exist_ok=True)


def check_api_key():
    """Check if OpenAI API key is configured."""
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ OpenAI API Key not configured!")
        st.markdown("""
        ### Setup Required
        
        Please configure your OpenAI API key:
        
        1. Create a `.env` file in the backend directory
        2. Add: `OPENAI_API_KEY=your_key_here`
        3. Restart the application
        
        Or set the environment variable directly:
        ```bash
        export OPENAI_API_KEY=your_key_here
        ```
        """)
        return False
    return True


def apply_custom_css():
    """Apply custom CSS styling with futuristic cyber aesthetic."""
    st.markdown("""
    <style>
    /* Reset and base styles */
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    body {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Courier New', monospace;
    }
    
    /* Main container */
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {display: none;}
    
    /* Header/title styling */
    .stTitle {
        color: #FFFFFF !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        font-size: 2.5rem;
        text-shadow: 0 0 10px #FF0000;
        letter-spacing: 2px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 5px #FF0000; }
        to { text-shadow: 0 0 15px #FF0000, 0 0 20px #FF0000; }
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #000000;
        color: #FFFFFF;
        border: 2px solid #FF0000;
        border-radius: 0;
        padding: 1rem 2rem;
        font-weight: 600;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        background-color: #FF0000;
        color: #000000;
        box-shadow: 0 0 20px #FF0000;
        transform: translateY(-2px);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Input fields */
    input, textarea, select {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #FF0000 !important;
        border-radius: 0 !important;
        padding: 0.75rem !important;
        font-family: 'Courier New', monospace !important;
        transition: all 0.3s ease;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #FF0000 !important;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.5) !important;
        outline: none !important;
    }
    
    /* Labels */
    .stMarkdown, label {
        color: #FFFFFF !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Cards and containers */
    .interview-card {
        background-color: #000000;
        border: 2px solid #FF0000;
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
    }
    
    .interview-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #FF0000, #FFFFFF, #FF0000);
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Question boxes */
    .question-box {
        background-color: #000000;
        border: 2px solid #FF0000;
        border-left: 4px solid #FF0000;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .question-box::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 3px;
        height: 100%;
        background: #FF0000;
        animation: pulse 1.5s ease-in-out infinite alternate;
    }
    
    @keyframes pulse {
        from { opacity: 0.3; }
        to { opacity: 1; }
    }
    
    /* Answer boxes */
    .answer-box {
        background-color: #000000;
        border: 1px solid #FFFFFF;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #FFFFFF;
    }
    
    /* Score badges */
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border: 2px solid #FF0000;
        font-weight: 600;
        font-size: 1.2rem;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        letter-spacing: 1px;
        background-color: #000000;
        color: #FFFFFF;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
    }
    
    .score-high {
        border-color: #FF0000;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
    }
    
    .score-medium {
        border-color: #FF0000;
        opacity: 0.8;
    }
    
    .score-low {
        border-color: #FF0000;
        opacity: 0.6;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background-color: #FF0000 !important;
    }
    
    .stProgress > div {
        background-color: #333333 !important;
        border: 1px solid #FF0000;
    }
    
    /* Feedback sections */
    .feedback-positive {
        background-color: #000000;
        border: 2px solid #FF0000;
        border-left: 4px solid #FF0000;
        padding: 1rem;
        margin: 0.5rem 0;
        position: relative;
    }
    
    .feedback-positive::before {
        content: '>>';
        position: absolute;
        left: -20px;
        color: #FF0000;
        font-weight: bold;
    }
    
    .feedback-negative {
        background-color: #000000;
        border: 2px solid #FF0000;
        border-left: 4px solid #FF0000;
        padding: 1rem;
        margin: 0.5rem 0;
        opacity: 0.8;
        position: relative;
    }
    
    .feedback-negative::before {
        content: '>!';
        position: absolute;
        left: -20px;
        color: #FF0000;
        font-weight: bold;
    }
    
    /* Divider lines */
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #FF0000, transparent);
        margin: 2rem 0;
    }
    
    /* Typography enhancements */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Courier New', monospace !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    h2 {
        border-bottom: 1px solid #FF0000;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-up {
        animation: slideUp 0.3s ease-out;
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Cyber grid background effect */
    .cyber-grid {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(255, 0, 0, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 0, 0, 0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        pointer-events: none;
        z-index: -1;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #333333;
        border-radius: 50%;
        border-top-color: #FF0000;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Terminal-like cursor */
    .cursor {
        display: inline-block;
        width: 8px;
        height: 16px;
        background-color: #FF0000;
        animation: blink 1s infinite;
        vertical-align: middle;
        margin-left: 2px;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-active {
        background-color: #FF0000;
        box-shadow: 0 0 10px #FF0000;
        animation: pulse 1.5s ease-in-out infinite alternate;
    }
    
    .status-inactive {
        background-color: #333333;
        border: 1px solid #FF0000;
    }
    
    /* Hover effects */
    .hover-glow:hover {
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        .stTitle {
            font-size: 1.8rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    # Ensure directories exist
    ensure_directories()
    
    # Initialize session state
    init_session_state()
    
    # Apply custom styling
    apply_custom_css()
    
    # Check API key
    if not check_api_key():
        return
    
    # Route to appropriate page based on session state
    if not st.session_state.logged_in:
        render_login_page()
    elif st.session_state.interview_completed:
        render_results_page()
    else:
        render_interview_page()


if __name__ == "__main__":
    main()
