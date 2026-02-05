"""
Login Page - Candidate profile setup with role and experience selection.
"""
import streamlit as st
from app.utils.resume_parser import get_resume_parser


# Available roles
ROLES = [
    "Backend Engineer",
    "Frontend Engineer", 
    "Full Stack Developer",
    "DevOps Engineer",
    "AI/ML Engineer",
    "Data Engineer",
    "Mobile Developer",
    "Security Engineer",
    "Database Engineer",
    "QA Engineer",
    "Cloud Architect",
    "System Administrator"
]

# Experience levels
EXPERIENCE_LEVELS = [
    ("junior", "Junior (0-2 years)", "Entry-level questions, fundamental concepts"),
    ("mid", "Mid-level (2-5 years)", "Intermediate complexity, system design basics"),
    ("senior", "Senior (5-8 years)", "Advanced questions, architecture & leadership"),
    ("principal", "Principal (8+ years)", "Expert-level, strategic & complex scenarios")
]

# Companies (optional)
COMPANIES = [
    "Generic",
    "Google",
    "Amazon",
    "Microsoft",
    "Meta",
    "Apple",
    "Netflix",
    "Uber",
    "Airbnb",
    "Stripe",
    "Spotify",
    "LinkedIn",
    "Twitter",
    "Salesforce",
    "Adobe",
    "Intel",
    "NVIDIA",
    "Oracle",
    "IBM",
    "TCS",
    "Infosys",
    "Wipro",
    "HCL",
    "Other"
]


def render_login_page():
    """Render the login/profile setup page with cyber aesthetic."""
    
    # Add cyber grid background
    st.markdown('<div class="cyber-grid"></div>', unsafe_allow_html=True)
    
    # Back button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button(">> BACK <<", key="back_btn"):
            st.session_state.page = "home"
            st.rerun()
    
    # Header with cyber styling
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem; color: #FF0000;">[!]</div>
        <h1 style="color: white; font-family: 'Courier New', monospace; font-weight: 700; margin: 0; text-shadow: 0 0 10px #FF0000;">
            >> CYBER INTERVIEW SYSTEM <<
        </h1>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin-top: 0.5rem; font-family: 'Courier New', monospace;">
            INITIALIZING CANDIDATE PROFILE PROTOCOLS
        </p>
        <div class="status-indicator status-active" style="margin: 1rem auto;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main form container with cyber styling
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="interview-card">', unsafe_allow_html=True)
        
        # Name input
        st.markdown("### >> PERSONAL IDENTIFICATION <<")
        name = st.text_input(
            ">> FULL NAME *",
            placeholder="ENTER YOUR DESIGNATION",
            key="name_input",
            help="THIS WILL PERSONALIZE YOUR INTERVIEW PROTOCOLS"
        )
        
        email = st.text_input(
            ">> EMAIL ADDRESS [OPTIONAL]",
            placeholder="IDENT@CORP.NET",
            key="email_input",
            help="FOR PROGRESS RETENTION (NOT MANDATORY)"
        )
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Role selection
        st.markdown("### >> TARGET ROLE ASSIGNMENT <<")
        role = st.selectbox(
            ">> SELECT YOUR TARGET ROLE *",
            options=[""] + ROLES,
            key="role_select",
            help="WE'LL CUSTOMIZE QUESTIONS BASED ON YOUR TARGET ROLE"
        )
        
        # Role-specific tips
        if role:
            role_tips = {
                "Backend Engineer": "Focus on: APIs, databases, scalability, system design",
                "Frontend Engineer": "Focus on: JavaScript, React/Vue, CSS, performance",
                "Full Stack Developer": "Focus on: Both frontend & backend, integration",
                "DevOps Engineer": "Focus on: CI/CD, containers, cloud, automation",
                "AI/ML Engineer": "Focus on: ML algorithms, deep learning, MLOps",
                "Data Engineer": "Focus on: ETL, data pipelines, big data tools",
                "Mobile Developer": "Focus on: iOS/Android, React Native, mobile UX",
                "Security Engineer": "Focus on: Security protocols, vulnerabilities, encryption",
                "Database Engineer": "Focus on: SQL, NoSQL, optimization, modeling",
                "QA Engineer": "Focus on: Testing strategies, automation, quality",
                "Cloud Architect": "Focus on: AWS/Azure/GCP, architecture, cost optimization",
                "System Administrator": "Focus on: Linux, networking, scripting, monitoring"
            }
            st.info(f"💡 {role_tips.get(role, '')}")
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Experience level
        st.markdown("### >> EXPERIENCE CLASSIFICATION <<")
        
        exp_options = [level[1] for level in EXPERIENCE_LEVELS]
        experience_index = st.radio(
            ">> SELECT YOUR EXPERIENCE LEVEL *",
            options=range(len(exp_options)),
            format_func=lambda x: f">> {exp_options[x].upper()} <<",
            key="exp_radio",
            horizontal=True
        )
        
        selected_exp = EXPERIENCE_LEVELS[experience_index]
        st.caption(f"📌 {selected_exp[2]}")
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Company selection (optional)
        st.markdown("### >> CORPORATE TARGETING [OPTIONAL] <<")
        company = st.selectbox(
            ">> SELECT A COMPANY FOR TAILORED QUESTIONS",
            options=COMPANIES,
            index=0,
            key="company_select",
            help="QUESTIONS WILL BE CUSTOMIZED FOR THIS COMPANY'S INTERVIEW STYLE"
        )
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Resume upload (optional)
        st.markdown("### >> RESUME INTEGRATION [OPTIONAL] <<")
        uploaded_file = st.file_uploader(
            ">> UPLOAD YOUR RESUME (PDF) TO CUSTOMIZE QUESTIONS BASED ON YOUR SKILLS",
            type=['pdf'],
            key="resume_upload"
        )
        
        if uploaded_file is not None:
            try:
                # Parse resume
                resume_bytes = uploaded_file.read()
                parser = get_resume_parser()
                resume_data = parser.parse_pdf_resume(resume_bytes)
                
                # Store in session state
                st.session_state.uploaded_resume = resume_data
                st.session_state.resume_skills = resume_data.get("skills", [])[:10]  # Limit to top 10
                st.session_state.resume_projects = resume_data.get("projects", [])[:3]  # Limit to top 3
                
                # Show parsed information
                with st.expander(">> RESUME ANALYSIS <<", expanded=True):
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.markdown("**>> SKILLS IDENTIFIED <<**")
                        skills_text = ", ".join(st.session_state.resume_skills)
                        st.caption(skills_text if skills_text else "NO SKILLS DETECTED")
                        
                        st.markdown("**>> PROGRAMMING LANGUAGES <<**")
                        langs = resume_data.get("programming_languages", [])
                        langs_text = ", ".join(langs)
                        st.caption(langs_text if langs_text else "NO LANGUAGES DETECTED")
                    
                    with col_b:
                        st.markdown("**>> TECHNOLOGIES <<**")
                        tech = resume_data.get("technologies", [])
                        tech_text = ", ".join(tech)
                        st.caption(tech_text if tech_text else "NO TECHNOLOGIES DETECTED")
                        
                        st.markdown("**>> PROJECTS <<**")
                        proj_count = len(st.session_state.resume_projects)
                        st.caption(f">> {proj_count} PROJECT{'S' if proj_count != 1 else ''} IDENTIFIED <<")
                
                st.markdown("<div class='feedback-positive'>> RESUME UPLOAD AND ANALYSIS COMPLETE <</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f"<div class='feedback-negative'>> ERROR PROCESSING RESUME: {str(e)} <</div>", unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Interview settings
        st.markdown("### >> INTERVIEW PROTOCOL CONFIGURATION <<")
        
        col_a, col_b = st.columns(2)
        with col_a:
            num_questions = st.slider(
                ">> NUMBER OF QUESTIONS <<",
                min_value=5,
                max_value=15,
                value=8,
                key="num_questions",
                help="TOTAL QUESTIONS IN THE INTERVIEW"
            )
        
        with col_b:
            difficulty = st.select_slider(
                ">> STARTING DIFFICULTY <<",
                options=["EASY", "MEDIUM", "HARD"],
                value="MEDIUM",
                key="start_difficulty"
            )
        
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Validation
        if st.button(">> INITIATE INTERVIEW PROTOCOL <<", use_container_width=True, key="start_interview_btn"):
            if not name.strip():
                st.markdown("<div class='feedback-negative'>> ERROR: PLEASE ENTER YOUR NAME TO CONTINUE <</div>", unsafe_allow_html=True)
            elif not role:
                st.markdown("<div class='feedback-negative'>> ERROR: PLEASE SELECT A TARGET ROLE <</div>", unsafe_allow_html=True)
            else:
                # Save to session state
                st.session_state.candidate_name = name.strip()
                st.session_state.role = role
                st.session_state.experience_level = selected_exp[0]
                st.session_state.company = company if company != "Generic" else ""
                st.session_state.max_questions = num_questions
                st.session_state.difficulty = difficulty
                st.session_state.logged_in = True
                st.session_state.interview_active = True
                st.session_state.page = "interview"
                
                # Clear previous session data
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
                
                # Clear orchestrator to create a new session
                st.session_state.orchestrator_agent = None
                st.session_state.session_id = None
                
                # Pass resume data if available
                if hasattr(st.session_state, 'resume_skills'):
                    st.session_state.resume_skills = st.session_state.get('resume_skills', [])
                if hasattr(st.session_state, 'resume_projects'):
                    st.session_state.resume_projects = st.session_state.get('resume_projects', [])
                
                # Show success message briefly
                st.markdown(f"<div class='feedback-positive'>> WELCOME, {name.strip().upper()}! INITIATING {role.upper()} INTERVIEW PROTOCOLS... <</div>", unsafe_allow_html=True)
                st.rerun()
        
        # Back to home
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem; font-family: 'Courier New', monospace;">
            <p>>> ALL INFORMATION IS SESSION-BOUND AND NOT STORED <<<</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_login_page()
