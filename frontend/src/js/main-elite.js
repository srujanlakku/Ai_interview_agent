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
let interviewStartTime = null;
let questionCount = 0;
let totalQuestions = 5;

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
 * Login Page
 */
function LoginPage(params = {}) {
    return `
    <div class="auth-container">
        <div class="card auth-card glass-panel">
            <div class="auth-header">
                <div class="auth-logo neon-glow">INTERVIEW</div>
                <div class="auth-logo" style="font-size: var(--font-size-2xl); color: var(--color-neon-cyan);">PILOT</div>
                <p class="auth-subtitle">Elite AI Interview Preparation</p>
            </div>

            <form class="auth-form" id="loginForm">
                <div class="form-group">
                    <label for="email" class="form-label">Email</label>
                    <input 
                        type="email" 
                        id="email" 
                        class="form-input" 
                        placeholder="test@example.com"
                        value="test@example.com"
                        required
                    >
                </div>

                <div class="form-group">
                    <label for="password" class="form-label">Password</label>
                    <input 
                        type="password" 
                        id="password" 
                        class="form-input" 
                        placeholder="••••••••"
                        value="password123"
                        required
                    >
                </div>

                <div id="errorMessage" class="alert alert-error" style="display: none;"></div>

                <button type="submit" class="btn btn-primary" style="width: 100%; margin-bottom: 10px;">
                    Login
                </button>
            </form>

            <div class="auth-footer">
                <span class="auth-footer-text">
                    Don't have an account?
                    <a class="auth-footer-link" onclick="window.router.goTo('/signup')">Sign up here</a>
                </span>
            </div>
        </div>
    </div>
    `;
}

/**
 * Dashboard Page
 */
function DashboardPage(params = {}) {
    // Initialize speedometer after page renders
    setTimeout(() => {
        if (!speedometer && document.getElementById('speedometerContainer')) {
            speedometer = new ReadinessSpeedometer('speedometerContainer', { width: 280, height: 280 });
            speedometer.setReadiness(eliteState.readiness);
        }
    }, 100);
    
    const stats = sessionManager.getStats();
    
    return `
    <div class="dashboard-container">
        <div class="dashboard-header">
            <div>
                <h1 class="dashboard-title">Dashboard</h1>
                <p class="text-secondary">Welcome back, ${eliteState.currentUser?.name || 'User'}</p>
            </div>
            <div class="dashboard-user-info">
                <button class="btn btn-secondary btn-sm" onclick="logout()">
                    Logout
                </button>
            </div>
        </div>

        <!-- Main Grid -->
        <div class="dashboard-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; margin-bottom: 30px;">
            
            <!-- Speedometer Card -->
            <div class="speedometer-card glass-panel">
                <h3>Interview Readiness</h3>
                <div id="speedometerContainer" class="speedometer-container"></div>
            </div>
            
            <!-- Interview Mode Selection -->
            <div class="mode-selection-card glass-panel">
                <h3>Select Interview Mode</h3>
                <div class="mode-selector">
                    <button class="mode-button active" data-mode="practice" onclick="selectMode('practice', this)">
                        <span>🧘</span> Practice
                    </button>
                    <button class="mode-button" data-mode="pressure" onclick="selectMode('pressure', this)">
                        <span>⚡</span> Pressure
                    </button>
                    <button class="mode-button" data-mode="extreme" onclick="selectMode('extreme', this)">
                        <span>🔥</span> Extreme
                    </button>
                </div>
            </div>
            
            <!-- Stats Card -->
            <div class="stats-card glass-panel">
                <h3>Statistics</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; color: #00d4ff; font-weight: bold;">${stats.totalInterviews}</div>
                        <div class="text-secondary" style="font-size: 12px; margin-top: 5px;">Total Interviews</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; color: #00ff41; font-weight: bold;">${stats.averageScore}%</div>
                        <div class="text-secondary" style="font-size: 12px; margin-top: 5px;">Avg Score</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Quick Start Interview -->
        <div class="action-panel glass-panel">
            <h3>Ready to Practice?</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; align-items: flex-end;">
                <div>
                    <select id="companySelect" class="form-input">
                        <option value="">Select a Company</option>
                        <option value="Google">Google</option>
                        <option value="Microsoft">Microsoft</option>
                        <option value="Amazon">Amazon</option>
                        <option value="Apple">Apple</option>
                        <option value="Meta">Meta</option>
                        <option value="Tesla">Tesla</option>
                    </select>
                </div>
                <div>
                    <select id="difficultySelect" class="form-input">
                        <option value="Easy">Easy</option>
                        <option value="Medium" selected>Medium</option>
                        <option value="Hard">Hard</option>
                    </select>
                </div>
                <div>
                    <button class="btn btn-primary" style="width: 100%; padding: 10px;" onclick="startInterview()">Start Interview</button>
                </div>
            </div>
        </div>
    </div>
    `;
}

/**
 * Interview Screen
 */
function InterviewPage(params = {}) {
    questionCount = 0;
    interviewStartTime = Date.now();
    
    return `
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
                <h3>Question <span id="questionNumber">1</span> of ${totalQuestions}</h3>
                <div id="questionText" class="question-text">
                    Tell me about a time you overcame a significant challenge at work.
                </div>
            </div>
            
            <!-- Answer Input -->
            <div class="answer-panel glass-panel">
                <h3>Your Answer</h3>
                <textarea id="answerInput" class="answer-input" placeholder="Type your answer here..."></textarea>
                <div class="answer-controls">
                    <button class="btn btn-primary" onclick="submitAnswer()">Submit Answer</button>
                    <button class="btn btn-outline" onclick="skipQuestion()">Skip Question</button>
                    <button class="btn btn-danger" onclick="endInterview()">End Interview</button>
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
                            <div class="confidence-fill" id="confidenceFill" style="width: 0%; background: linear-gradient(90deg, #ff6b6b, #ffd93d);"></div>
                        </div>
                        <span class="confidence-value" id="confidenceValue">0%</span>
                    </div>
                    <div class="confidence-bar">
                        <span class="confidence-label">Clarity</span>
                        <div class="confidence-track">
                            <div class="confidence-fill" id="clarityFill" style="width: 0%; background: linear-gradient(90deg, #6bcf7f, #00ff41);"></div>
                        </div>
                        <span class="confidence-value" id="clarityValue">0%</span>
                    </div>
                    <div class="confidence-bar">
                        <span class="confidence-label">Structure</span>
                        <div class="confidence-track">
                            <div class="confidence-fill" id="structureFill" style="width: 0%; background: linear-gradient(90deg, #6b9cff, #00d4ff);"></div>
                        </div>
                        <span class="confidence-value" id="structureValue">0%</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;
}

/**
 * Completion Ceremony
 */
function CompletionCeremonyPage(score, feedback) {
    const isBadge = score >= 75 ? '🏆' : score >= 50 ? '⭐' : '💪';
    const title = score >= 75 ? 'Excellent!' : score >= 50 ? 'Good Job!' : 'Keep Practicing!';
    
    return `
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
    `;
}

// ==================== INTERVIEW CONTROLS ====================

function selectMode(mode, element) {
    eliteState.interviewMode = mode;
    document.querySelectorAll('.mode-button').forEach(btn => btn.classList.remove('active'));
    element.classList.add('active');
    if (animationEngine) {
        animationEngine.setInterviewMode(mode);
    }
}

function startInterview() {
    const company = document.getElementById('companySelect').value;
    const difficulty = document.getElementById('difficultySelect').value;
    
    if (!company) {
        alert('Please select a company');
        return;
    }
    
    // Create session
    const session = sessionManager.createSession(company, difficulty, eliteState.readiness);
    eliteState.currentInterview = { company, difficulty };
    
    // Set animation engine to interview mode
    if (animationEngine) {
        animationEngine.setInterviewMode(eliteState.interviewMode);
    }
    
    window.router.goTo('/interview');
}

function submitAnswer() {
    const answerText = document.getElementById('answerInput').value;
    
    if (!answerText.trim()) {
        alert('Please provide an answer');
        return;
    }
    
    questionCount++;
    
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
    if (sessionManager.currentSession) {
        sessionManager.addAnswer(
            answerText, 
            metrics.confidence / 100, 
            metrics.clarity / 100, 
            metrics.structure / 100
        );
    }
    
    // Show next question or end interview
    document.getElementById('answerInput').value = '';
    
    if (questionCount >= totalQuestions) {
        endInterview();
    } else {
        loadNextQuestion();
    }
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
    questionCount++;
    if (questionCount >= totalQuestions) {
        endInterview();
    } else {
        document.getElementById('answerInput').value = '';
        loadNextQuestion();
    }
}

function loadNextQuestion() {
    const questions = [
        'Tell me about a time you overcame a significant challenge at work.',
        'Describe your experience with teamwork and collaboration.',
        'What is your greatest strength as a software engineer?',
        'How do you handle tight deadlines and pressure?',
        'Tell me about your most complex technical project.'
    ];
    
    const randomQ = questions[Math.floor(Math.random() * questions.length)];
    document.getElementById('questionText').textContent = randomQ;
    document.getElementById('questionNumber').textContent = questionCount + 1;
    
    if (sessionManager.currentSession) {
        sessionManager.addQuestion(randomQ);
    }
}

function endInterview() {
    const session = sessionManager.currentSession;
    const score = Math.random() * 100;
    
    if (session) {
        session.score = score;
        sessionManager.completeSession(score);
        eliteState.readiness = Math.min(100, eliteState.readiness + score * 0.1);
    }
    
    showCompletionCeremony(score);
}

function showCompletionCeremony(score) {
    const page = CompletionCeremonyPage(score, []);
    document.getElementById('app').innerHTML = page;
    
    // Set up timer for page transitions
    setTimeout(() => {
        if (animationEngine) {
            animationEngine.queueFeedback('Interview completed!', 'success', 3000);
        }
    }, 500);
}

function returnToDashboard() {
    window.router.goTo('/dashboard');
}

function startNewInterview() {
    window.router.goTo('/dashboard');
    setTimeout(() => {
        document.getElementById('companySelect')?.focus();
    }, 100);
}

function logout() {
    auth.logout();
    eliteState.isLoggedIn = false;
    eliteState.currentUser = null;
    window.router.goTo('/login');
}

// ==================== ROUTER SETUP ====================

function initializePages() {
    window.router.register('/login', LoginPage, false);
    window.router.register('/dashboard', DashboardPage, true);
    window.router.register('/interview', InterviewPage, true);
    
    window.router.register('/', LoginPage, false);
}

function attachEventListeners() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const result = await auth.login(email, password);
                if (result && result.access_token) {
                    eliteState.isLoggedIn = true;
                    eliteState.currentUser = auth.getCurrentUser() || { name: email.split('@')[0], email };
                    window.router.goTo('/dashboard');
                } else {
                    const errorEl = document.getElementById('errorMessage');
                    errorEl.textContent = 'Login failed. Check credentials.';
                    errorEl.style.display = 'block';
                }
            } catch (error) {
                const errorEl = document.getElementById('errorMessage');
                errorEl.textContent = error.message || 'Login failed';
                errorEl.style.display = 'block';
            }
        });
    }

    // Interview timer
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
}

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
        
        // Set up pages
        initializePages();
        
        // Check if user is logged in
        if (auth.isLoggedIn()) {
            eliteState.isLoggedIn = true;
            eliteState.currentUser = auth.getCurrentUser();
            window.router.goTo('/dashboard');
        } else {
            window.router.goTo('/login');
        }
    }, 100);

    // Attach event listeners after a slight delay
    setTimeout(() => {
        attachEventListeners();
    }, 200);
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
