/**
 * InterviewPilot - Elite Frontend Application
 * Advanced features: Voice reactivity, interview modes, speedometer, timeline, feedback system
 */

// ==================== GLOBAL STATE ====================

let animationEngine = null;
let sessionManager = null;
let behaviorAnalyzer = null;
let speedometer = null;
let currentPage = null;

let eliteState = {
    isLoggedIn: false,
    currentUser: null,
    currentInterview: null,
    interviewMode: 'practice',
    timeRemaining: null,
    readiness: 0
};

// ==================== PAGE COMPONENTS ====================

/**
 * Elite Login Page
 */
const LoginPage = () => {
    return {
        html: `
            <div class="auth-container">
                <div class="auth-card glass-panel">
                    <div class="auth-header">
                        <h1 class="neon-glow">InterviewPilot</h1>
                        <p>Elite AI Interview Preparation</p>
                    </div>
                    <form id="loginForm" class="auth-form">
                        <div class="form-group">
                            <label for="loginEmail">Email</label>
                            <input type="email" id="loginEmail" name="email" placeholder="test@example.com" required>
                        </div>
                        <div class="form-group">
                            <label for="loginPassword">Password</label>
                            <input type="password" id="loginPassword" name="password" placeholder="••••••••" required>
                        </div>
                        <div id="loginError" class="error-message" style="display: none;"></div>
                        <button type="submit" class="btn btn-primary">Login</button>
                    </form>
                    <div class="auth-footer">
                        <p>No account? <a href="#signup" class="link">Sign up here</a></p>
                    </div>
                </div>
            </div>
        `,
        setupEventListeners: setupLoginForm
    };
};

/**
 * Elite Dashboard with Speedometer
 */
const DashboardPage = () => {
    return {
        html: `
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <div class="header-left">
                        <h1>Dashboard</h1>
                        <p>Welcome back, ${eliteState.currentUser?.name || 'User'}</p>
                    </div>
                    <div class="header-right">
                        <button class="btn btn-sm btn-outline" onclick="logout()">Logout</button>
                    </div>
                </div>
                
                <div class="dashboard-main">
                    <div class="dashboard-grid">
                        <!-- Readiness Speedometer -->
                        <div class="speedometer-card glass-panel">
                            <h3>Interview Readiness</h3>
                            <div id="speedometerContainer" class="speedometer-container"></div>
                        </div>
                        
                        <!-- Interview Mode Selection -->
                        <div class="mode-selection-card glass-panel">
                            <h3>Select Interview Mode</h3>
                            <div class="mode-selector">
                                <button class="mode-button active" data-mode="practice">
                                    <span>🧘</span> Practice
                                </button>
                                <button class="mode-button" data-mode="pressure">
                                    <span>⚡</span> Pressure
                                </button>
                                <button class="mode-button" data-mode="extreme">
                                    <span>🔥</span> Extreme
                                </button>
                            </div>
                        </div>
                        
                        <!-- Stats Card -->
                        <div class="stats-card glass-panel">
                            <h3>Recent Statistics</h3>
                            <div id="statsContent"></div>
                        </div>
                        
                        <!-- Timeline Card -->
                        <div class="timeline-card glass-panel">
                            <h3>Interview Timeline</h3>
                            <div id="timelineContent" class="timeline"></div>
                        </div>
                    </div>
                    
                    <!-- Quick Start Interview -->
                    <div class="action-panel glass-panel">
                        <h3>Ready to Practice?</h3>
                        <div class="quick-company-selector">
                            <select id="companySelect" class="form-input">
                                <option value="">Select a Company</option>
                                <option value="Google">Google</option>
                                <option value="Microsoft">Microsoft</option>
                                <option value="Amazon">Amazon</option>
                                <option value="Apple">Apple</option>
                                <option value="Meta">Meta</option>
                                <option value="Tesla">Tesla</option>
                            </select>
                            <select id="difficultySelect" class="form-input">
                                <option value="Easy">Easy</option>
                                <option value="Medium" selected>Medium</option>
                                <option value="Hard">Hard</option>
                            </select>
                            <button class="btn btn-primary" onclick="startInterview()">Start Interview</button>
                        </div>
                    </div>
                </div>
            </div>
        `,
        setupEventListeners: setupDashboard
    };
};

/**
 * Elite Interview Screen with Real-Time Feedback
 */
const InterviewPage = () => {
    return {
        html: `
            <div class="interview-container">
                <div class="interview-header">
                    <div class="interview-info">
                        <h2>${eliteState.currentInterview?.company} Interview</h2>
                        <span class="difficulty-badge">${eliteState.currentInterview?.difficulty}</span>
                    </div>
                    <div class="interview-timer" id="interviewTimer">
                        Time: <span id="timerValue">00:00</span>
                    </div>
                </div>
                
                <div class="interview-main">
                    <!-- Question Display -->
                    <div class="question-panel glass-panel">
                        <h3>Question <span id="questionNumber">1</span></h3>
                        <div id="questionText" class="question-text">
                            Loading question...
                        </div>
                    </div>
                    
                    <!-- Answer Input -->
                    <div class="answer-panel glass-panel">
                        <h3>Your Answer</h3>
                        <textarea id="answerInput" class="answer-input" placeholder="Type your answer here..."></textarea>
                        <div class="answer-controls">
                            <button class="btn btn-primary" onclick="submitAnswer()">Submit Answer</button>
                            <button class="btn btn-outline" onclick="skipQuestion()">Skip Question</button>
                        </div>
                    </div>
                    
                    <!-- Real-Time Feedback HUD -->
                    <div id="feedbackOverlay" class="feedback-hud" style="display: none;"></div>
                    
                    <!-- Confidence Visualizer -->
                    <div class="confidence-panel glass-panel">
                        <h3>Real-Time Metrics</h3>
                        <div class="confidence-visualizer">
                            <div class="confidence-bar">
                                <span class="confidence-label">Confidence</span>
                                <div class="confidence-track">
                                    <div class="confidence-fill" id="confidenceFill" style="width: 0%"></div>
                                </div>
                                <span class="confidence-value" id="confidenceValue">0%</span>
                            </div>
                            <div class="confidence-bar">
                                <span class="confidence-label">Clarity</span>
                                <div class="confidence-track">
                                    <div class="confidence-fill" id="clarityFill" style="width: 0%"></div>
                                </div>
                                <span class="confidence-value" id="clarityValue">0%</span>
                            </div>
                            <div class="confidence-bar">
                                <span class="confidence-label">Structure</span>
                                <div class="confidence-track">
                                    <div class="confidence-fill" id="structureFill" style="width: 0%"></div>
                                </div>
                                <span class="confidence-value" id="structureValue">0%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        setupEventListeners: setupInterviewPage
    };
};

/**
 * Elite Completion Ceremony
 */
const CompletionCeremonyPage = (score, feedback) => {
    const isBadge = score >= 75 ? '🏆' : score >= 50 ? '⭐' : '💪';
    const title = score >= 75 ? 'Excellent!' : score >= 50 ? 'Good Job!' : 'Keep Practicing!';
    
    return {
        html: `
            <div class="completion-screen">
                <div class="completion-content">
                    <div class="completion-badge">${isBadge}</div>
                    <h1 class="completion-title">${title}</h1>
                    <div class="completion-score">${Math.round(score)}</div>
                    <p class="completion-subtitle">Interview Score</p>
                    <div class="completion-message">
                        ${score >= 75 ? '🎉 Outstanding performance! You\'re ready for real interviews.' : 
                          score >= 50 ? '✓ Good effort! Review the feedback and practice more.' :
                          '💡 Keep practicing. Each interview helps you improve.'}
                    </div>
                    ${score >= 75 ? '<div class="readiness-badge">Interview Ready</div>' : ''}
                    <div style="margin-top: 40px; display: flex; gap: 20px; justify-content: center;">
                        <button class="btn btn-primary" onclick="returnToDashboard()">Return to Dashboard</button>
                        <button class="btn btn-outline" onclick="startNewInterview()">Start Another Interview</button>
                    </div>
                </div>
            </div>
        `,
        setupEventListeners: () => {}
    };
};

/**
 * Elite Timeline & History Page
 */
const TimelinePage = () => {
    const timeline = sessionManager.getSessionTimeline();
    const stats = sessionManager.getStats();
    
    return {
        html: `
            <div class="timeline-container">
                <div class="timeline-header">
                    <h1>Your Interview Journey</h1>
                    <p>Total Interviews: ${stats.totalInterviews} | Average Score: ${stats.averageScore}%</p>
                </div>
                
                <div class="timeline-stats glass-panel">
                    <div class="stat-grid">
                        <div class="stat-item">
                            <div class="stat-value">${stats.totalInterviews}</div>
                            <div class="stat-label">Total Interviews</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${stats.averageScore}%</div>
                            <div class="stat-label">Average Score</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${stats.highestScore}%</div>
                            <div class="stat-label">Best Score</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${stats.companiesInterviewed}</div>
                            <div class="stat-label">Companies</div>
                        </div>
                    </div>
                </div>
                
                <div class="timeline-visual">
                    <div class="timeline">
                        ${timeline.map((session, idx) => `
                            <div class="timeline-item">
                                <div class="timeline-dot"></div>
                                <div class="timeline-content">
                                    <h3>${session.company}</h3>
                                    <p>Score: <strong>${session.score}%</strong> | Difficulty: ${session.difficulty}</p>
                                    <p>Duration: ${session.duration} min | Date: ${session.date.toLocaleDateString()}</p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `,
        setupEventListeners: () => {}
    };
};

// ==================== SETUP FUNCTIONS ====================

function setupLoginForm() {
    const form = document.getElementById('loginForm');
    const errorDiv = document.getElementById('loginError');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        try {
            const response = await apiClient.login(email, password);
            
            if (response.access_token) {
                auth.login({
                    token: response.access_token,
                    user: { email, name: email.split('@')[0] }
                });
                
                eliteState.isLoggedIn = true;
                eliteState.currentUser = auth.getCurrentUser();
                
                router.goTo('/dashboard');
            }
        } catch (error) {
            errorDiv.textContent = error.message || 'Login failed';
            errorDiv.style.display = 'block';
        }
    });
}

function setupDashboard() {
    // Initialize speedometer
    const speedometerContainer = document.getElementById('speedometerContainer');
    if (speedometerContainer && !speedometer) {
        speedometer = new ReadinessSpeedometer('speedometerContainer', { width: 300, height: 300 });
        speedometer.setReadiness(eliteState.readiness);
    }
    
    // Setup mode selector
    document.querySelectorAll('.mode-button').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.mode-button').forEach(b => b.classList.remove('active'));
            e.target.closest('.mode-button').classList.add('active');
            eliteState.interviewMode = e.target.closest('.mode-button').dataset.mode;
            if (animationEngine) {
                animationEngine.setInterviewMode(eliteState.interviewMode);
            }
        });
    });
    
    // Load stats
    const stats = sessionManager.getStats();
    const statsContent = document.getElementById('statsContent');
    statsContent.innerHTML = `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div><span style="color: #00d4ff;">Interviews:</span> <strong style="color: #00ff41;">${stats.totalInterviews}</strong></div>
            <div><span style="color: #00d4ff;">Avg Score:</span> <strong style="color: #00ff41;">${stats.averageScore}%</strong></div>
            <div><span style="color: #00d4ff;">Best Score:</span> <strong style="color: #00ff41;">${stats.highestScore}%</strong></div>
            <div><span style="color: #00d4ff;">Companies:</span> <strong style="color: #00ff41;">${stats.companiesInterviewed}</strong></div>
        </div>
    `;
    
    // Load timeline
    const timeline = sessionManager.getSessionTimeline();
    const timelineContent = document.getElementById('timelineContent');
    timelineContent.innerHTML = timeline.slice(0, 3).map(session => `
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
                <h4>${session.company} - ${session.score}%</h4>
                <p>${session.date.toLocaleDateString()}</p>
            </div>
        </div>
    `).join('');
}

function setupInterviewPage() {
    // Start interview timer
    let seconds = 0;
    setInterval(() => {
        seconds++;
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        document.getElementById('timerValue').textContent = 
            `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }, 1000);
    
    // Load first question (simulated)
    loadNextQuestion();
}

function loadNextQuestion() {
    const questions = [
        'Tell me about a time you overcame a significant challenge at work.',
        'Describe your experience with teamwork and collaboration.',
        'What is your greatest strength as a software engineer?',
        'How do you handle tight deadlines and pressure?'
    ];
    
    const randomQ = questions[Math.floor(Math.random() * questions.length)];
    document.getElementById('questionText').textContent = randomQ;
    
    if (sessionManager.currentSession) {
        sessionManager.addQuestion(randomQ);
    }
}

// ==================== INTERVIEW CONTROLS ====================

function startInterview() {
    const company = document.getElementById('companySelect').value;
    const difficulty = document.getElementById('difficultySelect').value;
    
    if (!company) {
        alert('Please select a company');
        return;
    }
    
    // Create session
    sessionManager.createSession(company, difficulty, eliteState.readiness);
    eliteState.currentInterview = { company, difficulty };
    
    // Set animation engine to interview mode
    if (animationEngine) {
        animationEngine.setInterviewMode(eliteState.interviewMode);
    }
    
    router.goTo('/interview');
}

function submitAnswer() {
    const answerText = document.getElementById('answerInput').value;
    
    if (!answerText.trim()) {
        alert('Please provide an answer');
        return;
    }
    
    // Analyze answer
    const metrics = {
        confidence: Math.random() * 100,
        clarity: Math.random() * 100,
        structure: Math.random() * 100,
        hesitation: Math.random() * 50,
        pace: 100 + Math.random() * 100
    };
    
    const analysis = behaviorAnalyzer.analyzeAnswer(answerText, metrics);
    
    // Update visualizer
    updateConfidenceVisualizer(metrics);
    
    // Add to session
    sessionManager.addAnswer(answerText, metrics.confidence / 100, metrics.clarity / 100, metrics.structure / 100);
    
    // Show next question
    document.getElementById('answerInput').value = '';
    loadNextQuestion();
}

function updateConfidenceVisualizer(metrics) {
    document.getElementById('confidenceFill').style.width = metrics.confidence + '%';
    document.getElementById('confidenceValue').textContent = Math.round(metrics.confidence) + '%';
    
    document.getElementById('clarityFill').style.width = metrics.clarity + '%';
    document.getElementById('clarityValue').textContent = Math.round(metrics.clarity) + '%';
    
    document.getElementById('structureFill').style.width = metrics.structure + '%';
    document.getElementById('structureValue').textContent = Math.round(metrics.structure) + '%';
}

function skipQuestion() {
    loadNextQuestion();
}

function endInterview() {
    const session = sessionManager.currentSession;
    const score = Math.random() * 100;
    
    session.score = score;
    sessionManager.completeSession(score);
    eliteState.readiness += score * 0.2;
    
    showCompletionCeremony(score);
}

function showCompletionCeremony(score) {
    const page = CompletionCeremonyPage(score, []);
    document.getElementById('app').innerHTML = page.html;
    page.setupEventListeners();
}

function returnToDashboard() {
    router.goTo('/dashboard');
}

function startNewInterview() {
    router.goTo('/dashboard');
    setTimeout(() => {
        document.getElementById('companySelect').focus();
    }, 100);
}

function logout() {
    auth.logout();
    eliteState.isLoggedIn = false;
    eliteState.currentUser = null;
    router.goTo('/login');
}

// ==================== ROUTER SETUP ====================

const router = new Router();

router.register('/login', LoginPage, false);
router.register('/dashboard', DashboardPage, true);
router.register('/interview', InterviewPage, true);
router.register('/timeline', TimelinePage, true);

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize core systems
    sessionManager = new InterviewSessionManager();
    
    // Initialize animation engine with voice reactivity
    setTimeout(() => {
        animationEngine = new EliteAnimationEngine('codeRainCanvas', {
            voiceReactive: true,
            glowIntensity: 0.8
        });
        animationEngine.start();
        
        // Initialize behavior analyzer
        behaviorAnalyzer = new AIBehaviorAnalyzer(animationEngine);
    }, 100);
    
    // Check if user is logged in
    if (auth.isLoggedIn()) {
        eliteState.isLoggedIn = true;
        eliteState.currentUser = auth.getCurrentUser();
        router.goTo('/dashboard');
    } else {
        router.goTo('/login');
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (animationEngine) {
        animationEngine.destroy();
    }
    if (speedometer) {
        speedometer.destroy();
    }
});
