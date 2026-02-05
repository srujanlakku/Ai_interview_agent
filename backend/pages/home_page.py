"""
Home Page - Landing page with feature showcase.
"""
import streamlit as st


def render_home_page():
    """Render the stunning home/landing page."""
    
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <div class="animate-float" style="font-size: 5rem; margin-bottom: 1rem;">🎯</div>
        <h1 class="hero-title">AI Interview Agent</h1>
        <p class="hero-subtitle">
            Master your technical interviews with AI-powered practice sessions.<br/>
            Get real-time feedback and boost your confidence.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Start Interview", use_container_width=True, key="start_btn"):
                st.session_state.page = "login"
                st.rerun()
        with col_b:
            if st.button("📖 How It Works", use_container_width=True, key="how_btn"):
                st.session_state.page = "home"
                st.rerun()
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <span class="badge badge-primary">🎯 10+ Roles</span>
        <span class="badge badge-success">⚡ Real-time AI</span>
        <span class="badge badge-warning">📊 Smart Scoring</span>
        <span class="badge badge-danger">🔥 Adaptive Difficulty</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <h2 style="text-align: center; color: white; font-family: 'Poppins', sans-serif; 
               margin: 3rem 0 2rem 0; font-weight: 700;">
        Why Choose AI Interview Agent?
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    features = [
        {
            "icon": "🤖",
            "title": "AI Interviewer",
            "desc": "Intelligent AI that adapts to your skill level and provides realistic interview experience."
        },
        {
            "icon": "📈",
            "title": "Adaptive Difficulty",
            "desc": "Questions automatically adjust based on your performance for optimal learning."
        },
        {
            "icon": "💡",
            "title": "Instant Feedback",
            "desc": "Get detailed feedback on every answer with specific improvement suggestions."
        },
        {
            "icon": "🎯",
            "title": "Role-Specific",
            "desc": "Tailored questions for Backend, Frontend, Full Stack, DevOps, AI/ML, and more."
        }
    ]
    
    for col, feature in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature['icon']}</div>
                <div class="feature-title">{feature['title']}</div>
                <div class="feature-desc">{feature['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown("""
    <h2 style="text-align: center; color: white; font-family: 'Poppins', sans-serif; 
               margin: 2rem 0; font-weight: 700;">
        How It Works
    </h2>
    <p style="text-align: center; color: rgba(255,255,255,0.8); font-size: 1.1rem; max-width: 800px; margin: 0 auto 2rem;">
        Master your technical interviews with our proven 3-step process
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    steps = [
        {
            "number": "1",
            "title": "Setup Your Profile",
            "desc": "Choose your target role and experience level. Optionally upload your resume for personalized questions.",
            "icon": "👤",
            "duration": "2 mins"
        },
        {
            "number": "2",
            "title": "Take the Interview",
            "desc": "Answer 5-15 realistic technical questions. Get instant feedback after each response.",
            "icon": "💬",
            "duration": "15-30 mins"
        },
        {
            "number": "3",
            "title": "Review Results",
            "desc": "See your detailed score breakdown, strengths, weaknesses, and personalized learning recommendations.",
            "icon": "📊",
            "duration": "5 mins"
        }
    ]
    
    for col, step in zip([col1, col2, col3], steps):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="padding: 1.5rem; text-align: center; height: 100%;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">{step['icon']}</div>
                <div style="font-size: 3rem; font-weight: 800; color: #6366F1; margin-bottom: 0.5rem;">
                    {step['number']}
                </div>
                <h3 style="color: white; margin: 0.5rem 0;">{step['title']}</h3>
                <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.5;">
                    {step['desc']}
                </p>
                <div style="margin-top: 1rem;">
                    <span class="badge badge-info">⏱️ {step['duration']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Interview Expectations
    st.markdown("""
    <div class="glass-card" style="padding: 2rem; margin: 2rem 0;">
        <h2 style="color: white; text-align: center; margin-bottom: 1.5rem;">
            🎯 What to Expect During Your Interview
        </h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <div>
                <h4 style="color: #6366F1; margin-bottom: 0.5rem;">📋 Question Types</h4>
                <ul style="color: rgba(255,255,255,0.8); line-height: 1.6;">
                    <li>Technical concepts and theory</li>
                    <li>Coding and problem-solving</li>
                    <li>System design and architecture</li>
                    <li>Behavioral and situational</li>
                </ul>
            </div>
            <div>
                <h4 style="color: #6366F1; margin-bottom: 0.5rem;">⭐ Evaluation Criteria</h4>
                <ul style="color: rgba(255,255,255,0.8); line-height: 1.6;">
                    <li>Correctness and accuracy</li>
                    <li>Depth of understanding</li>
                    <li>Clarity of explanation</li>
                    <li>Problem-solving approach</li>
                </ul>
            </div>
        </div>
        <div style="text-align: center; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);">
            <p style="color: rgba(255,255,255,0.7); font-style: italic;">
                "Practice makes perfect - our AI interviewer provides the same rigorous evaluation as top tech companies"
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Trust & Transparency Section
    st.markdown("""
    <div class="glass-card" style="padding: 2rem; margin: 2rem 0; background: linear-gradient(135deg, #1e293b, #334155);">
        <h2 style="color: white; text-align: center; margin-bottom: 1.5rem;">
            🔒 Your Privacy & Data
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🛡️</div>
                <h4 style="color: white; margin-bottom: 0.5rem;">Data Security</h4>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                    Your interview data is processed securely and deleted after your session ends
                </p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</div>
                <h4 style="color: white; margin-bottom: 0.5rem;">AI Processing</h4>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                    Responses are analyzed by AI to provide objective, consistent evaluation
                </p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <h4 style="color: white; margin-bottom: 0.5rem;">Score Transparency</h4>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                    Understand exactly how your scores are calculated with detailed breakdowns
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    steps = [
        {
            "num": "01",
            "title": "Set Up Profile",
            "desc": "Enter your name, select your target role, and specify your experience level.",
            "icon": "👤"
        },
        {
            "num": "02", 
            "title": "Take Interview",
            "desc": "Answer questions from our AI interviewer. Get real-time feedback and hints.",
            "icon": "💬"
        },
        {
            "num": "03",
            "title": "Review Results",
            "desc": "Get detailed scores, strengths, weaknesses, and personalized improvement tips.",
            "icon": "📊"
        }
    ]
    
    for col, step in zip([col1, col2, col3], steps):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">{step['icon']}</div>
                <div style="font-size: 2rem; font-weight: 800; color: rgba(255,255,255,0.3);">
                    {step['num']}
                </div>
                <h3 style="color: white; margin: 0.5rem 0;">{step['title']}</h3>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                    {step['desc']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Supported Roles
    st.markdown("""
    <h2 style="text-align: center; color: white; font-family: 'Poppins', sans-serif; 
               margin: 2rem 0; font-weight: 700;">
        Supported Roles
    </h2>
    """, unsafe_allow_html=True)
    
    roles = [
        ("💻", "Backend Engineer"),
        ("🎨", "Frontend Engineer"),
        ("🔧", "Full Stack Developer"),
        ("☁️", "DevOps Engineer"),
        ("🤖", "AI/ML Engineer"),
        ("📊", "Data Engineer"),
        ("📱", "Mobile Developer"),
        ("🔐", "Security Engineer"),
        ("🗄️", "Database Engineer"),
        ("🧪", "QA Engineer"),
    ]
    
    # Create a grid of role badges
    role_html = '<div style="text-align: center; display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem;">'
    for icon, role in roles:
        role_html += f'''
        <div class="glass-card" style="padding: 1rem 1.5rem; display: inline-block;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
            <span style="color: white; font-weight: 500;">{role}</span>
        </div>
        '''
    role_html += '</div>'
    st.markdown(role_html, unsafe_allow_html=True)
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class="glass-card animate-glow" style="text-align: center; margin: 2rem auto; max-width: 600px;">
        <h2 style="color: white; margin-bottom: 1rem;">Ready to Ace Your Interview?</h2>
        <p style="color: rgba(255,255,255,0.8); margin-bottom: 1.5rem;">
            Start practicing now and boost your confidence for your next technical interview.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Free Practice", use_container_width=True, key="cta_btn"):
            st.session_state.page = "login"
            st.rerun()
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.5); padding: 2rem; font-size: 0.85rem;">
        <p>Built with ❤️ using Streamlit & OpenAI</p>
        <p style="margin-top: 0.5rem;">© 2026 AI Interview Agent. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_home_page()
