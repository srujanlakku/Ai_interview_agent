/**
 * Dashboard Component
 * Displays frequently asked questions and company analytics
 */

function InsightsPage() {
    return `
        <div class="dashboard-container">
            <div class="dashboard-header">
                <h1>Interview Insights Dashboard</h1>
                <p class="dashboard-subtitle">Frequently Asked Questions & Company Analytics</p>
                <button onclick="window.router.goTo('/company-select')" class="btn-secondary" style="margin-top: 1rem;">
                    Back to Interview Start
                </button>
            </div>
            
            <div class="dashboard-filters">
                <div class="filter-group">
                    <label for="companyFilter">Company</label>
                    <input type="text" id="companyFilter" placeholder="e.g., Google, Amazon" />
                </div>
                <div class="filter-group">
                    <label for="roleFilter">Role</label>
                    <input type="text" id="roleFilter" placeholder="e.g., Software Engineer" />
                </div>
                <button id="applyFilters" class="btn-primary">Search</button>
            </div>
            
            <div id="dashboardContent" class="dashboard-content">
                <div class="dashboard-placeholder">
                    <p>Enter a company and role to view frequently asked questions</p>
                </div>
            </div>
        </div>
    `;
}

/**
 * Initialize dashboard event listeners
 */
function initializeDashboard() {
    const applyBtn = document.getElementById('applyFilters');
    const companyInput = document.getElementById('companyFilter');
    const roleInput = document.getElementById('roleFilter');

    if (applyBtn && companyInput && roleInput) {
        applyBtn.addEventListener('click', async () => {
            const company = companyInput.value.trim();
            const role = roleInput.value.trim();

            if (company && role) {
                await loadDashboardData(company, role);
            } else {
                alert('Please enter both company and role');
            }
        });

        // Allow Enter key to submit
        [companyInput, roleInput].forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    applyBtn.click();
                }
            });
        });
    }
}

/**
 * Load dashboard data
 */
async function loadDashboardData(company, role) {
    const contentEl = document.getElementById('dashboardContent');
    if (!contentEl) return;

    contentEl.innerHTML = '<div class="loading">Loading insights...</div>';

    try {
        // Load top questions and company stats in parallel
        const [topQuestions, companyStats] = await Promise.all([
            window.api.getTopQuestions(company, role, 20),
            window.api.getCompanyStats(company)
        ]);

        contentEl.innerHTML = `
            <div class="stats-overview">
                ${renderCompanyStats(companyStats)}
            </div>
            
            <div class="top-questions-section">
                <h2>Top ${topQuestions.total_questions} Frequently Asked Questions</h2>
                <p class="section-subtitle">for ${role} at ${company}</p>
                ${renderTopQuestions(topQuestions.questions)}
            </div>
        `;

    } catch (error) {
        console.error('Error loading dashboard:', error);
        contentEl.innerHTML = `
            <div class="error-message">
                <p>Failed to load dashboard data: ${error.message}</p>
                <p class="error-hint">This might be because there's no interview data for this company/role yet.</p>
            </div>
        `;
    }
}

/**
 * Render company statistics
 */
function renderCompanyStats(stats) {
    const roles = stats && stats.most_asked_roles ? stats.most_asked_roles.slice(0, 3).join(', ') : 'N/A';
    const topics = stats && stats.common_topics ? stats.common_topics.slice(0, 5).join(', ') : 'N/A';
    const total = stats ? stats.total_interviews : 0;

    return `
        <div class="stat-card">
            <div class="stat-item">
                <span class="stat-label">Total Interviews</span>
                <span class="stat-value">${total}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Top Roles</span>
                <span class="stat-value">${roles || 'N/A'}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Common Topics</span>
                <span class="stat-value">${topics || 'N/A'}</span>
            </div>
        </div>
    `;
}

/**
 * Render top questions list
 */
function renderTopQuestions(questions) {
    if (!questions || questions.length === 0) {
        return '<p class="no-data">No frequently asked questions found for this combination.</p>';
    }

    return `
        <div class="questions-grid">
            ${questions.map((q, index) => renderQuestionCard(q, index + 1)).join('')}
        </div>
    `;
}

/**
 * Render individual question card
 */
function renderQuestionCard(question, rank) {
    const typeClass = `type-${question.question_type.replace('_', '-')}`;

    return `
        <div class="dashboard-question-card ${typeClass}">
            <div class="question-rank">#${rank}</div>
            <div class="question-body">
                <div class="question-meta">
                    <span class="question-type-badge">${formatQuestionType(question.question_type)}</span>
                    ${question.category ? `<span class="question-category">${question.category}</span>` : ''}
                    <span class="question-frequency">Asked ${question.frequency}x</span>
                </div>
                <p class="question-text">${escapeHtml(question.question)}</p>
                <div class="question-footer">
                    <span class="last-asked">Last asked: ${formatDate(question.last_asked)}</span>
                </div>
            </div>
        </div>
    `;
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
    return date.toLocaleDateString();
}

/**
 * Format question type (reuse from InterviewReview)
 */
function formatQuestionType(type) {
    const typeMap = {
        'soft_skill': 'Soft Skill',
        'technical': 'Technical',
        'coding': 'Coding'
    };
    return typeMap[type] || type;
}

/**
 * Escape HTML (reuse from InterviewReview)
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
