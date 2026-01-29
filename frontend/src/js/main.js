/**
 * InterviewPilot - Elite Frontend Application
 * Advanced features: Voice reactivity, interview modes, speedometer, timeline, feedback system
 */

let animationEngine = null;
let sessionManager = null;
let behaviorAnalyzer = null;
let speedometer = null;
let interviewStartTime = null;
let questionCount = 0;
let totalQuestions = 5;

let eliteState = {
    isLoggedIn: false,
    currentUser: null,
    currentInterview: null,
    interviewMode: 'practice',
    readiness: 0
};

// ==================== PAGE COMPONENTS ====================

function LoginPage(params = {}) {
    return `
    <div class="auth-container">
        <div class="card auth-card glass-panel">
            <div class="auth-header">
                <div class="auth-logo neon-glow">INTERVIEW</div>
                <div class="auth-logo" style="font-size: var(--font-size-2xl); color: var(--color-neon-cyan);">PILOT</div>
                <p class="auth-subtitle">Interview pilot by Srujan Patel</p>
            </div>

            <form class="auth-form" id="loginForm">
                <div class="form-group">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" id="email" class="form-input" placeholder="your@email.com" value="test@example.com" required>
                </div>

                <div class="form-group">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" id="password" class="form-input" placeholder="••••••••" value="Password123" required>
                </div>

                <div id="errorMessage" class="alert alert-error" style="display: none;"></div>

                <button type="submit" class="btn btn-primary" style="width: 100%;">Login</button>
            </form>

            <div class="auth-footer">
                <span class="auth-footer-text">
                    Don't have an account?
                    <a class="auth-footer-link" style="cursor: pointer;" onclick="window.router.goTo('/signup')">Sign up here</a>
                </span>
            </div>
        </div>
    </div>
    `;
}

function SignupPage(params = {}) {
    return `
    <div class="auth-container">
        <div class="card auth-card glass-panel">
            <div class="auth-header">
                <div class="auth-logo neon-glow">INTERVIEW</div>
                <div class="auth-logo" style="font-size: var(--font-size-2xl); color: var(--color-neon-cyan);">PILOT</div>
                <p class="auth-subtitle">Create your account</p>
            </div>

            <form class="auth-form" id="signupForm">
                <div class="form-group">
                    <label for="signup-name" class="form-label">Full Name</label>
                    <input type="text" id="signup-name" class="form-input" placeholder="John Doe" required>
                </div>

                <div class="form-group">
                    <label for="signup-email" class="form-label">Email</label>
                    <input type="email" id="signup-email" class="form-input" placeholder="your@email.com" required>
                </div>

                <div class="form-group">
                    <label for="signup-password" class="form-label">Password</label>
                    <input type="password" id="signup-password" class="form-input" placeholder="Min 8 chars, 1 uppercase, 1 digit" required>
                </div>

                <div id="signupErrorMessage" class="alert alert-error" style="display: none;"></div>

                <button type="submit" class="btn btn-primary" style="width: 100%;">Sign Up</button>
            </form>

            <div class="auth-footer">
                <span class="auth-footer-text">
                    Already have an account?
                    <a class="auth-footer-link" style="cursor: pointer;" onclick="window.router.goTo('/login')">Login here</a>
                </span>
            </div>
        </div>
    </div>
    `;
}

// ==================== COMPANY SELECTION PAGE ====================

function CompanySelectionPage(params = {}) {
    setTimeout(() => {
        if (!window.companySelector) {
            window.companySelector = new CompanySelector(new APIClient(), 'company-selector');
        }
    }, 100);

    return `
    <div id="company-selector"></div>
    `;
}

// ==================== ROLE SELECTION PAGE ====================

function RoleSelectionPage(params = {}) {
    const selectedCompany = JSON.parse(sessionStorage.getItem('selectedCompany') || '{}');

    if (!selectedCompany.id) {
        window.router.goTo('/company-select');
        return '<div></div>';
    }

    setTimeout(() => {
        if (!window.roleSelector) {
            window.roleSelector = new RoleSelector(new APIClient(), selectedCompany, 'role-selector');
        }
    }, 100);

    return `
    <div id="role-selector"></div>
    `;
}

// ==================== DASHBOARD PAGE ====================

function DashboardPage(params = {}) {
    setTimeout(() => {
        if (!speedometer && document.getElementById('speedometerContainer')) {
            speedometer = new ReadinessSpeedometer('speedometerContainer', { width: 280, height: 280 });
            speedometer.setReadiness(eliteState.readiness);
        }
    }, 100);

    const stats = sessionManager ? sessionManager.getStats() : { totalInterviews: 0, averageScore: 0 };

    return `
    <div class="dashboard-container">
        <div class="dashboard-header">
            <div>
                <h1 class="dashboard-title">Dashboard</h1>
                <p class="text-secondary">Welcome back, ${eliteState.currentUser?.name || 'User'}</p>
            </div>
            <div class="dashboard-user-info">
                <button class="btn btn-secondary btn-sm" onclick="logout()">Logout</button>
            </div>
        </div>

        <div class="dashboard-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; margin-bottom: 30px;">
            
            <div class="speedometer-card glass-panel" style="padding: 20px; border-radius: 8px;">
                <h3>Interview Readiness</h3>
                <div id="speedometerContainer" class="speedometer-container" style="height: 300px; display: flex; justify-content: center;"></div>
            </div>
            
            <div class="mode-selection-card glass-panel" style="padding: 20px; border-radius: 8px;">
                <h3>Select Interview Mode</h3>
                <div class="mode-selector" style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                    <button class="mode-button active" data-mode="practice" onclick="selectMode('practice', this)" style="padding: 15px; border: 2px solid #00d4ff; border-radius: 8px; background: rgba(0, 212, 255, 0.1); cursor: pointer; color: #00d4ff; font-weight: bold;">🧘 Practice</button>
                    <button class="mode-button" data-mode="pressure" onclick="selectMode('pressure', this)" style="padding: 15px; border: 2px solid transparent; border-radius: 8px; background: transparent; cursor: pointer; color: #999; font-weight: bold;">⚡ Pressure</button>
                    <button class="mode-button" data-mode="extreme" onclick="selectMode('extreme', this)" style="padding: 15px; border: 2px solid transparent; border-radius: 8px; background: transparent; cursor: pointer; color: #999; font-weight: bold;">🔥 Extreme</button>
                </div>
            </div>
            
            <div class="stats-card glass-panel" style="padding: 20px; border-radius: 8px;">
                <h3>Statistics</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div style="text-align: center;"><div style="font-size: 24px; color: #00d4ff; font-weight: bold;">${stats.totalInterviews}</div><div style="font-size: 12px; color: #999; margin-top: 5px;">Total Interviews</div></div>
                    <div style="text-align: center;"><div style="font-size: 24px; color: #00ff41; font-weight: bold;">${stats.averageScore}%</div><div style="font-size: 12px; color: #999; margin-top: 5px;">Avg Score</div></div>
                </div>
            </div>
        </div>

        <div class="action-panel glass-panel" style="padding: 20px; border-radius: 8px;">
            <h3>🎯 India MNC Interview Preparation</h3>
            <p style="color: #999; margin: 10px 0; font-size: 14px;">Prepare for interviews at 25+ Indian MNCs with company-specific questions</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                <button class="btn btn-primary" style="width: 100%; padding: 12px; cursor: pointer; background: linear-gradient(135deg, #00D9FF, #00FF88); color: #000a15; font-weight: bold;" onclick="window.router.goTo('/company-select')">🏢 Select Company</button>
                <button class="btn btn-secondary" style="width: 100%; padding: 12px; cursor: pointer; border: 2px solid #00D9FF; background: transparent; color: #00D9FF;" onclick="window.router.goTo('/practice')">🎓 Practice Skills</button>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                <button class="btn btn-secondary" style="width: 100%; padding: 12px; cursor: pointer; border: 1px solid rgba(0, 212, 255, 0.4); color: #00d4ff;" onclick="window.router.goTo('/dashboard/resume')">📄 Resume Analyzer</button>
                <button class="btn btn-secondary" style="width: 100%; padding: 12px; cursor: pointer; border: 1px solid rgba(0, 212, 255, 0.4); color: #00d4ff;" onclick="window.router.goTo('/dashboard/sure-questions')">🎯 Sure Questions</button>
                <button class="btn btn-secondary" style="width: 100%; padding: 12px; cursor: pointer; border: 1px solid rgba(0, 212, 255, 0.4); color: #00d4ff;" onclick="window.router.goTo('/dashboard/insights')">📊 Insights</button>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; align-items: flex-end;">
                <div><select id="companySelect" class="form-input" style="width: 100%; padding: 10px; border: 1px solid #00d4ff; border-radius: 4px; background: transparent; color: #00d4ff;"><option value="">Select Company</option><option value="Google">Google</option><option value="Microsoft">Microsoft</option><option value="Amazon">Amazon</option><option value="Apple">Apple</option><option value="Meta">Meta</option><option value="Tesla">Tesla</option></select></div>
                <div><select id="difficultySelect" class="form-input" style="width: 100%; padding: 10px; border: 1px solid #00d4ff; border-radius: 4px; background: transparent; color: #00d4ff;"><option value="Easy">Easy</option><option value="Medium" selected>Medium</option><option value="Hard">Hard</option></select></div>
                <div><button class="btn btn-primary" style="width: 100%; padding: 10px; cursor: pointer;" onclick="startInterview()">Start Interview</button></div>
            </div>
        </div>
    </div>
    `;
}

function InterviewPage(params = {}) {
    questionCount = 0;
    interviewStartTime = Date.now();

    return `
    <div class="interview-container">
        <div class="interview-header" style="display: flex; justify-content: space-between; margin-bottom: 20px;">
            <div><h2>${eliteState.currentInterview?.company} Interview</h2><span style="display: inline-block; padding: 5px 10px; background: #ffd93d; color: #000; border-radius: 4px; font-weight: bold;">${eliteState.currentInterview?.difficulty}</span></div>
            <div id="interviewTimer" style="text-align: right; font-size: 18px; color: #00d4ff;">Time: <span id="timerValue">00:00</span></div>
        </div>
        
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
            <div>
                <div class="question-panel glass-panel" style="padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h3>Question <span id="questionNumber">1</span> of ${totalQuestions}</h3>
                    <div id="questionText" style="font-size: 16px; margin: 20px 0; line-height: 1.6;">Tell me about yourself</div>
                </div>
                
                <div class="answer-panel glass-panel" style="padding: 20px; border-radius: 8px;">
                    <h3>Your Answer</h3>
                    <textarea id="answerInput" placeholder="Type your answer here..." style="width: 100%; height: 150px; padding: 10px; border: 1px solid #00d4ff; border-radius: 4px; background: rgba(0, 212, 255, 0.05); color: #00d4ff; font-family: monospace;"></textarea>
                    <div style="display: flex; gap: 10px; margin-top: 10px;">
                        <button onclick="submitAnswer()" style="flex: 1; padding: 10px; background: #00d4ff; color: #000; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">Submit</button>
                        <button onclick="skipQuestion()" style="flex: 1; padding: 10px; border: 1px solid #999; background: transparent; color: #999; border-radius: 4px; cursor: pointer;">Skip</button>
                        <button onclick="endInterview()" style="flex: 1; padding: 10px; border: 1px solid #ff6b6b; background: rgba(255, 107, 107, 0.1); color: #ff6b6b; border-radius: 4px; cursor: pointer;">End</button>
                    </div>
                </div>
            </div>
            
            <div class="confidence-panel glass-panel" style="padding: 20px; border-radius: 8px; height: fit-content;">
                <h3>Real-Time Metrics</h3>
                <div style="margin-bottom: 15px;"><span style="display: block; font-size: 12px; color: #999; margin-bottom: 5px;">Confidence</span><div style="width: 100%; height: 20px; background: rgba(0, 212, 255, 0.1); border-radius: 4px; overflow: hidden;"><div id="confidenceFill" style="width: 0%; background: linear-gradient(90deg, #ff6b6b, #ffd93d); height: 100%;"></div></div><span id="confidenceValue" style="display: inline-block; margin-top: 5px; font-size: 12px; color: #00d4ff;">0%</span></div>
                <div style="margin-bottom: 15px;"><span style="display: block; font-size: 12px; color: #999; margin-bottom: 5px;">Clarity</span><div style="width: 100%; height: 20px; background: rgba(0, 212, 255, 0.1); border-radius: 4px; overflow: hidden;"><div id="clarityFill" style="width: 0%; background: linear-gradient(90deg, #6bcf7f, #00ff41); height: 100%;"></div></div><span id="clarityValue" style="display: inline-block; margin-top: 5px; font-size: 12px; color: #00d4ff;">0%</span></div>
                <div><span style="display: block; font-size: 12px; color: #999; margin-bottom: 5px;">Structure</span><div style="width: 100%; height: 20px; background: rgba(0, 212, 255, 0.1); border-radius: 4px; overflow: hidden;"><div id="structureFill" style="width: 0%; background: linear-gradient(90deg, #6b9cff, #00d4ff); height: 100%;"></div></div><span id="structureValue" style="display: inline-block; margin-top: 5px; font-size: 12px; color: #00d4ff;">0%</span></div>
            </div>
        </div>
    </div>
    `;
}

function CompletionPage(score) {
    const badge = score >= 75 ? '🏆' : score >= 50 ? '⭐' : '💪';
    const title = score >= 75 ? 'Excellent!' : score >= 50 ? 'Good Job!' : 'Keep Practicing!';

    return `
        <div style="display: flex; align-items: center; justify-content: center; min-height: 100vh;">
            <div style="text-align: center;">
                <div style="font-size: 80px; margin-bottom: 20px;">${badge}</div>
                <h1 style="font-size: 36px; color: #00d4ff; margin-bottom: 20px;">${title}</h1>
                <div style="font-size: 72px; color: #00ff41; font-weight: bold; margin-bottom: 10px;">${Math.round(score)}</div>
                <p style="color: #999; font-size: 18px; margin-bottom: 40px;">Interview Score</p>
                <div style="display: flex; gap: 15px; flex-direction: column; align-items: center;">
                    <div style="display: flex; gap: 15px; justify-content: center;">
                        <button onclick="viewInterviewReview()" class="btn btn-primary" style="padding: 12px 30px; font-size: 16px; font-weight: bold; cursor: pointer;">View Detailed Review</button>
                    </div>
                    <div style="display: flex; gap: 15px; justify-content: center; margin-top: 10px;">
                        <button onclick="returnToDashboard()" style="padding: 12px 30px; font-size: 16px; background: #00d4ff; color: #000; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">Return to Dashboard</button>
                        <button onclick="startNewInterview()" style="padding: 12px 30px; font-size: 16px; border: 1px solid #00d4ff; background: transparent; color: #00d4ff; border-radius: 4px; cursor: pointer;">Start Another</button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// ==================== FUNCTIONS ====================

function selectMode(mode, element) {
    eliteState.interviewMode = mode;
    document.querySelectorAll('.mode-button').forEach(btn => {
        btn.style.border = '2px solid transparent';
        btn.style.background = 'transparent';
        btn.style.color = '#999';
    });
    element.style.border = '2px solid #00d4ff';
    element.style.background = 'rgba(0, 212, 255, 0.1)';
    element.style.color = '#00d4ff';
    if (animationEngine && animationEngine.setInterviewMode) {
        animationEngine.setInterviewMode(mode);
    }
}

async function startInterview() {
    const company = document.getElementById('companySelect').value;
    const difficulty = document.getElementById('difficultySelect').value;

    if (!company) {
        alert('Please select a company');
        return;
    }

    try {
        // 1. Create the interview entry
        const interview = await window.api.createInterview(company, 'Software Engineer', difficulty);
        eliteState.currentInterview = interview;

        if (sessionManager) {
            sessionManager.createSession(company, difficulty, eliteState.readiness);
            sessionManager.currentSession.backendId = interview.id;
        }

        // 2. Start the Multi-Agent Orchestration
        const result = await window.api.getNextQuestion(interview.id);

        if (result && result.question) {
            eliteState.currentQuestion = result.question;
            questionCount = 0; // Reset for new session
            window.router.goTo('/interview');

            // Allow page to load then set question
            setTimeout(() => {
                displayQuestion(result.question, result.question_number);
            }, 100);
        }

        if (animationEngine && animationEngine.setInterviewMode) {
            animationEngine.setInterviewMode(eliteState.interviewMode);
        }
    } catch (error) {
        console.error('Failed to start interview:', error);
        alert('Failed to initialize AI Supervisor. Please check your connection.');
    }
}

async function submitAnswer() {
    const answerText = document.getElementById('answerInput').value;
    if (!answerText.trim()) {
        alert('Please provide an answer');
        return;
    }

    // Visual feedback
    const submitBtn = document.querySelector('button[onclick="submitAnswer()"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Analyzing...';
    submitBtn.disabled = true;

    try {
        if (!eliteState.currentInterview || !eliteState.currentInterview.id) {
            throw new Error('No active interview session');
        }

        // Call Multi-Agent Supervisor to process answer and get next step
        const result = await window.api.submitAnswer(eliteState.currentInterview.id, answerText);

        if (result.success) {
            if (result.status === 'completed') {
                endInterview(result.summary);
            } else if (result.next_question) {
                eliteState.currentQuestion = result.next_question;
                questionCount++;
                displayQuestion(result.next_question, result.question_number || (questionCount + 1));
                document.getElementById('answerInput').value = '';
            }
        }

    } catch (error) {
        console.error('Failed to submit answer:', error);
        alert('Supervisor error. Retrying last step...');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

function viewInterviewReview() {
    const sessionId = sessionManager?.currentSession?.backendId || eliteState.currentInterview?.id || 1;
    window.router.goTo(`/review/${sessionId}`, { id: sessionId });
}

function updateConfidenceVisualizer(metrics) {
    const confFill = document.getElementById('confidenceFill');
    if (confFill) {
        confFill.style.width = metrics.confidence + '%';
        document.getElementById('confidenceValue').textContent = Math.round(metrics.confidence) + '%';
    }
    const clarFill = document.getElementById('clarityFill');
    if (clarFill) {
        clarFill.style.width = metrics.clarity + '%';
        document.getElementById('clarityValue').textContent = Math.round(metrics.clarity) + '%';
    }
    const strucFill = document.getElementById('structureFill');
    if (strucFill) {
        strucFill.style.width = metrics.structure + '%';
        document.getElementById('structureValue').textContent = Math.round(metrics.structure) + '%';
    }
}

function skipQuestion() {
    questionCount++;
    if (questionCount >= totalQuestions) {
        endInterview();
    } else {
        document.getElementById('answerInput').value = '';
        loadNextQuestion();
    }
}

function displayQuestion(questionData, number) {
    const questionTextEl = document.getElementById('questionText');
    const questionNumberEl = document.getElementById('questionNumber');

    if (!questionTextEl) return;

    let content = questionData.question_text || questionData;

    // Check if it's a coding question
    if (questionData.question_type === 'coding' && questionData.coding_data) {
        const coding = questionData.coding_data;
        content = `
            <div class="coding-problem">
                <div class="problem-statement" style="background: rgba(0, 0, 0, 0.3); padding: 15px; border-left: 4px solid #00d4ff; margin-bottom: 15px;">
                    <strong>Problem:</strong><br>${coding.problem_statement}
                </div>
                <div style="font-size: 14px; color: #aaa; margin-bottom: 10px;">
                    Type your code solution below. Consider time and space complexity.
                </div>
            </div>
        `;
        document.getElementById('answerInput').placeholder = "/* Write your code here... */\n\nfunction solution() {\n  \n}";
    } else {
        document.getElementById('answerInput').placeholder = "Type your answer here...";
    }

    questionTextEl.innerHTML = content;
    if (questionNumberEl) questionNumberEl.textContent = number || (questionCount + 1);

    if (sessionManager && sessionManager.currentSession) {
        sessionManager.addQuestion(content);
    }
}

function loadNextQuestion() {
    // This is now handled by the SupervisorAgent via submitAnswer/startInterview
    console.log("Static loadNextQuestion bypassed for Agent flow");
}

function endInterview(summary) {
    const score = summary ? summary.final_score * 10 : Math.random() * 100;

    if (sessionManager && sessionManager.currentSession) {
        sessionManager.currentSession.score = score;
        sessionManager.completeSession(score);
    }

    eliteState.readiness = Math.min(100, eliteState.readiness + score * 0.1);

    const badge = score >= 75 ? '🏆' : score >= 50 ? '⭐' : '💪';
    const title = score >= 75 ? 'Ready for the Job!' : score >= 50 ? 'Gaining Momentum' : 'Work in Progress';

    document.getElementById('app').innerHTML = `
        <div style="display: flex; align-items: center; justify-content: center; min-height: 100vh;">
            <div style="text-align: center; max-width: 600px;">
                <div style="font-size: 80px; margin-bottom: 20px;">${badge}</div>
                <h1 style="font-size: 36px; color: #00d4ff; margin-bottom: 10px;">${title}</h1>
                <div style="font-size: 72px; color: #00ff41; font-weight: bold; margin-bottom: 5px;">${Math.round(score)}</div>
                <p style="color: #999; font-size: 18px; margin-bottom: 30px;">AI Assessment Score</p>
                
                ${summary ? `
                    <div class="glass-panel" style="padding: 20px; text-align: left; margin-bottom: 30px; border: 1px solid rgba(0, 212, 255, 0.3);">
                        <h4 style="color: #00d4ff;">Supervisor Summary:</h4>
                        <p style="color: #ddd; line-height: 1.6;">${summary.summary_report}</p>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px;">
                            <div>
                                <small style="color: #00ff41;">Strengths:</small>
                                <ul style="font-size: 12px; padding-left: 15px;">${summary.key_strengths.map(s => `<li>${s}</li>`).join('')}</ul>
                            </div>
                            <div>
                                <small style="color: #ff6b6b;">Focus Areas:</small>
                                <ul style="font-size: 12px; padding-left: 15px;">${summary.main_weaknesses.map(w => `<li>${w}</li>`).join('')}</ul>
                            </div>
                        </div>
                    </div>
                ` : ''}

                <div style="display: flex; gap: 15px; flex-direction: column; align-items: center;">
                    <div style="display: flex; gap: 15px; justify-content: center;">
                        <button onclick="viewInterviewReview()" class="btn btn-primary" style="padding: 12px 30px; font-size: 16px; font-weight: bold; cursor: pointer;">View Detailed Analysis</button>
                    </div>
                    <div style="display: flex; gap: 15px; justify-content: center; margin-top: 10px;">
                        <button onclick="returnToDashboard()" style="padding: 12px 30px; font-size: 16px; background: rgba(0, 212, 255, 0.2); color: #00d4ff; border: 1px solid #00d4ff; border-radius: 4px; font-weight: bold; cursor: pointer;">Return to Dashboard</button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function returnToDashboard() {
    window.router.goTo('/dashboard');
}

function startNewInterview() {
    window.router.goTo('/dashboard');
}

function logout() {
    auth.logout();
    eliteState.isLoggedIn = false;
    window.router.goTo('/login');
}

function startClassicInterview() {
    eliteState.currentInterview = {
        company: 'Classic Mode',
        difficulty: 'Medium'
    };
    window.router.goTo('/interview');
}

// ==================== INITIALIZATION ====================

function initializePages() {
    window.router.register('/login', LoginPage, false);
    window.router.register('/signup', SignupPage, false);
    window.router.register('/company-select', CompanySelectionPage, true);
    window.router.register('/role-select', RoleSelectionPage, true);
    window.router.register('/interview', InterviewPage, true);
    window.router.register('/review/:id', InterviewReviewPage, true);
    window.router.register('/dashboard', DashboardPage, true);
    window.router.register('/dashboard/insights', () => {
        setTimeout(() => initializeDashboard(), 100);
        return InsightsPage();
    }, true);
    window.router.register('/dashboard/resume', ResumeAnalyzerPage, true);
    window.router.register('/dashboard/sure-questions', SureQuestionsPage, true);
    window.router.register('/practice', PracticeModePage, true);
    window.router.register('/', LoginPage, false);
}

function attachEventListeners() {
    setTimeout(() => {
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;

                try {
                    if (auth && auth.login) {
                        const result = await auth.login(email, password);
                        if (result && result.success) {
                            eliteState.isLoggedIn = true;
                            eliteState.currentUser = result.user || { name: email.split('@')[0] };
                            window.router.goTo('/dashboard');
                        } else {
                            throw new Error(result.error || 'Login failed');
                        }
                    }
                } catch (error) {
                    const errorEl = document.getElementById('errorMessage');
                    if (errorEl) {
                        errorEl.textContent = 'Login failed: ' + (error.message || 'Unknown error');
                        errorEl.style.display = 'block';
                    }
                }
            });
        }

        const signupForm = document.getElementById('signupForm');
        if (signupForm) {
            signupForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const name = document.getElementById('signup-name').value;
                const email = document.getElementById('signup-email').value;
                const password = document.getElementById('signup-password').value;

                try {
                    if (auth && auth.signup) {
                        const result = await auth.signup(email, password, name);
                        if (result && result.success) {
                            eliteState.isLoggedIn = true;
                            eliteState.currentUser = result.user;
                            window.router.goTo('/dashboard');
                        } else {
                            throw new Error(result.error || 'Signup failed');
                        }
                    }
                } catch (error) {
                    const errorEl = document.getElementById('signupErrorMessage');
                    if (errorEl) {
                        errorEl.textContent = 'Signup failed: ' + (error.message || 'Unknown error');
                        errorEl.style.display = 'block';
                    }
                }
            });
        }

        const timerElement = document.getElementById('interviewTimer');
        if (timerElement) {
            let seconds = 0;
            setInterval(() => {
                seconds++;
                const mins = Math.floor(seconds / 60);
                const secs = seconds % 60;
                const timerValue = document.getElementById('timerValue');
                if (timerValue) {
                    timerValue.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
                }
            }, 1000);

            loadNextQuestion();
        }
    }, 300);
}

document.addEventListener('DOMContentLoaded', () => {
    try {
        sessionManager = new InterviewSessionManager();
    } catch (e) {
        console.log('Session manager error:', e.message);
    }

    setTimeout(() => {
        try {
            animationEngine = new EliteAnimationEngine('codeRainCanvas', { voiceReactive: true, glowIntensity: 0.8 });
            if (animationEngine && animationEngine.start) {
                animationEngine.start();
            }
        } catch (e) {
            console.log('Animation engine error:', e.message);
        }

        try {
            behaviorAnalyzer = new AIBehaviorAnalyzer(animationEngine);
        } catch (e) {
            console.log('Behavior analyzer error:', e.message);
        }

        // Initialize pages and routes BEFORE using router
        initializePages();

        // Setup router listeners
        window.router.setupListeners();

        if (auth && auth.isLoggedIn && auth.isLoggedIn()) {
            eliteState.isLoggedIn = true;
            eliteState.currentUser = auth.getCurrentUser();
            window.router.goTo('/dashboard');
        } else {
            window.router.goTo('/login');
        }
    }, 100);

    setTimeout(() => {
        attachEventListeners();
    }, 200);
});

window.addEventListener('beforeunload', () => {
    if (animationEngine && animationEngine.destroy) {
        animationEngine.destroy();
    }
    if (speedometer && speedometer.destroy) {
        speedometer.destroy();
    }
});
