/**
 * Interview Review Component
 * Displays detailed review of an interview with all questions, answers, and feedback.
 */

function InterviewReviewPage() {
    return `
        <div class="interview-review-container">
            <div class="glass-card review-header-card">
                <h2>📋 Interview Review</h2>
                <p>Detailed breakdown of your interview performance</p>
            </div>
            <div id="interviewReviewContent" class="review-content">
                <!-- Review content will be loaded here -->
            </div>
        </div>
    `;
}

async function loadInterviewReview(interviewId) {
    const container = document.getElementById('interviewReviewContent');

    try {
        container.innerHTML = '<div class="loader-container"><div class="spinner"></div><p>Loading review...</p></div>';

        const review = await window.api.getInterviewReview(interviewId);

        if (!review) {
            container.innerHTML = '<p class="error-message">Failed to load interview review.</p>';
            return;
        }

        renderInterviewReview(review, container);
    } catch (error) {
        console.error('Error loading interview review:', error);
        container.innerHTML = '<p class="error-message">Failed to load interview review: ' + error.message + '</p>';
    }
}

function renderInterviewReview(review, container) {
    const overallScore = review.overall_score || 0;
    const scoreColor = overallScore >= 8 ? '#00e676' : (overallScore >= 5 ? '#ffeb3b' : '#ff5252');

    container.innerHTML = `
        <div class="glass-card score-summary-card">
            <div class="score-summary">
                <div class="main-score" style="border-color: ${scoreColor}">
                    <span class="score-value" style="color: ${scoreColor}">${overallScore.toFixed(1)}</span>
                    <span class="score-total">/ 10</span>
                </div>
                <div class="summary-info">
                    <h3>${review.company_name || 'Interview'}</h3>
                    <p>${review.job_role || 'Software Engineer'}</p>
                </div>
            </div>
        </div>
        
        <div class="questions-review-list">
            ${renderQuestionsReview(review.questions || [])}
        </div>
    `;
}

function renderQuestionsReview(questions) {
    if (questions.length === 0) {
        return '<p class="no-questions">No questions found for this interview.</p>';
    }

    return questions.map((q, index) => {
        const scoreColor = (q.score || 0) >= 7 ? '#00e676' : (q.score || 0) >= 4 ? '#ffeb3b' : '#ff5252';

        return `
            <div class="glass-card question-review-card">
                <div class="question-header">
                    <span class="question-number">Q${index + 1}</span>
                    <span class="question-type badge">${q.question_type || 'General'}</span>
                    ${q.score !== undefined ? `<span class="question-score" style="color: ${scoreColor}">${q.score.toFixed(1)}/10</span>` : ''}
                </div>
                
                <div class="question-body">
                    <div class="question-text">
                        <strong>Question:</strong>
                        <p>${q.question}</p>
                    </div>
                    
                    <div class="answer-section">
                        <strong>Your Answer:</strong>
                        <p class="candidate-answer">${q.candidate_answer || 'No answer provided'}</p>
                    </div>
                    
                    ${q.ideal_answer ? `
                        <div class="ideal-answer-section">
                            <strong>Ideal Answer:</strong>
                            <p class="ideal-answer">${q.ideal_answer}</p>
                        </div>
                    ` : ''}
                    
                    ${q.feedback ? `
                        <div class="feedback-section">
                            <strong>Feedback:</strong>
                            <p class="feedback-text">${q.feedback}</p>
                        </div>
                    ` : ''}
                    
                    ${q.coding_data ? renderCodingData(q.coding_data) : ''}
                </div>
            </div>
        `;
    }).join('');
}

function renderCodingData(codingData) {
    return `
        <div class="coding-data-section">
            <h4>Coding Problem Details</h4>
            <div class="coding-detail">
                <strong>Problem:</strong>
                <p>${codingData.problem_statement}</p>
            </div>
            <div class="coding-detail">
                <strong>Expected Approach:</strong>
                <p>${codingData.expected_approach}</p>
            </div>
            <div class="coding-detail">
                <strong>Sample Solution:</strong>
                <pre class="code-solution"><code>${codingData.code_solution}</code></pre>
            </div>
            <div class="coding-detail">
                <strong>Difficulty:</strong>
                <span class="difficulty-badge ${codingData.difficulty_level.toLowerCase()}">${codingData.difficulty_level}</span>
            </div>
        </div>
    `;
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { InterviewReviewPage, loadInterviewReview, renderInterviewReview, renderQuestionsReview, renderCodingData };
}
