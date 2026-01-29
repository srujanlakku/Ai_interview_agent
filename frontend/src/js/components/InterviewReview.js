/**
 * Interview Review Page Component
 * Displays detailed review of interview with answers, ideal solutions, and feedback
 */

function InterviewReviewPage() {
    return `
        <div class="review-container">
            <div class="review-header">
                <h1>Interview Review</h1>
                <div id="reviewMeta" class="review-meta"></div>
            </div>
            
            <div id="reviewQuestions" class="review-questions">
                <!-- Questions will be loaded here -->
            </div>
            
            <div class="review-actions">
                <button onclick="window.router.goTo('/dashboard')" class="btn-secondary">
                    Back to Dashboard
                </button>
                <button onclick="window.router.goTo('/interviews')" class="btn-primary">
                    Start New Interview
                </button>
            </div>
        </div>
    `;
}

/**
 * Load and display interview review
 */
async function loadInterviewReview(interviewId) {
    try {
        const review = await window.api.getInterviewReview(interviewId);

        // Update meta information
        const metaEl = document.getElementById('reviewMeta');
        if (metaEl) {
            metaEl.innerHTML = `
                <div class="meta-item">
                    <span class="meta-label">Company:</span>
                    <span class="meta-value">${review.company_name || 'N/A'}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Role:</span>
                    <span class="meta-value">${review.job_role || 'N/A'}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Overall Score:</span>
                    <span class="meta-value score">${review.overall_score ? review.overall_score.toFixed(1) + '/10' : 'N/A'}</span>
                </div>
            `;
        }

        // Render questions
        const questionsEl = document.getElementById('reviewQuestions');
        if (questionsEl && review.questions) {
            questionsEl.innerHTML = review.questions.map((q, index) =>
                renderReviewQuestion(q, index + 1)
            ).join('');
        }

    } catch (error) {
        console.error('Error loading review:', error);
        const questionsEl = document.getElementById('reviewQuestions');
        if (questionsEl) {
            questionsEl.innerHTML = `
                <div class="error-message">
                    <p>Failed to load interview review: ${error.message}</p>
                </div>
            `;
        }
    }
}

/**
 * Render individual question review card
 */
function renderReviewQuestion(question, number) {
    const typeClass = `question-type-${question.question_type}`;
    const scoreClass = getScoreClass(question.score);

    return `
        <div class="review-question-card ${typeClass}">
            <div class="question-header">
                <span class="question-number">Question ${number}</span>
                <span class="question-type-badge">${formatQuestionType(question.question_type)}</span>
                ${question.score !== null && question.score !== undefined ?
            `<span class="question-score ${scoreClass}">${question.score.toFixed(1)}/10</span>` :
            ''}
            </div>
            
            <div class="question-content">
                <h3>Question</h3>
                <p class="question-text">${escapeHtml(question.question)}</p>
                
                ${question.question_type === 'coding' && question.coding_data ?
            renderCodingProblem(question.coding_data) : ''}
            </div>
            
            <div class="answer-section">
                <div class="user-answer">
                    <h4>Your Answer</h4>
                    <div class="answer-content">
                        ${question.candidate_answer ?
            (question.question_type === 'coding' ?
                `<pre><code>${escapeHtml(question.candidate_answer)}</code></pre>` :
                `<p>${escapeHtml(question.candidate_answer)}</p>`) :
            '<p class="no-answer">No answer provided</p>'}
                    </div>
                </div>
                
                ${question.ideal_answer ? `
                <div class="ideal-answer">
                    <h4>Ideal Answer</h4>
                    <div class="answer-content">
                        ${question.question_type === 'coding' && question.coding_data ?
                `<pre><code>${escapeHtml(question.coding_data.code_solution)}</code></pre>` :
                `<p>${escapeHtml(question.ideal_answer)}</p>`}
                    </div>
                </div>` : ''}
            </div>
            
            ${question.feedback ? `
            <div class="feedback-section">
                <h4>Feedback</h4>
                <p class="feedback-text">${escapeHtml(question.feedback)}</p>
            </div>` : ''}
        </div>
    `;
}

/**
 * Render coding problem details
 */
function renderCodingProblem(codingData) {
    return `
        <div class="coding-problem-details">
            <h4>Problem Statement</h4>
            <p>${escapeHtml(codingData.problem_statement)}</p>
            
            <h4>Expected Approach</h4>
            <p>${escapeHtml(codingData.expected_approach)}</p>
            
            <div class="difficulty-badge difficulty-${codingData.difficulty_level.toLowerCase()}">
                ${codingData.difficulty_level}
            </div>
        </div>
    `;
}

/**
 * Format question type for display
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
 * Get CSS class for score
 */
function getScoreClass(score) {
    if (score === null || score === undefined) return '';
    if (score >= 8) return 'score-excellent';
    if (score >= 6) return 'score-good';
    if (score >= 4) return 'score-average';
    return 'score-poor';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
