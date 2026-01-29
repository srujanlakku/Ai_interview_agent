/**
 * Sure Questions Component
 * Displays curated questions for specific company and role.
 */

function SureQuestionsPage() {
    return `
        <div class="sure-questions-container">
            <div class="glass-card selection-card">
                <h2>🎯 "Sure" Questions</h2>
                <p>Most common questions asked by top companies, curated from past interviews.</p>
                
                <div class="row">
                    <div class="form-group col">
                        <label>Company</label>
                        <select id="sureCompanySelect" class="glass-input">
                            <option value="">Select Company</option>
                            <option value="Google">Google</option>
                            <option value="Amazon">Amazon</option>
                            <option value="Microsoft">Microsoft</option>
                            <option value="Meta">Meta</option>
                            <option value="Generic">Generic / All</option>
                        </select>
                    </div>
                    <div class="form-group col">
                        <label>Role</label>
                        <select id="sureRoleSelect" class="glass-input">
                            <option value="Software Engineer">Software Engineer</option>
                            <option value="Frontend Engineer">Frontend Engineer</option>
                            <option value="Backend Engineer">Backend Engineer</option>
                            <option value="Data Scientist">Data Scientist</option>
                            <option value="Product Manager">Product Manager</option>
                        </select>
                    </div>
                </div>
                <button class="btn-primary" id="btnGetSureQuestions">Show Questions</button>
            </div>

            <div id="sureQuestionsList" class="questions-list-container">
                <!-- Groups will appear here -->
            </div>
        </div>
    `;
}

async function initSureQuestions() {
    const btn = document.getElementById('btnGetSureQuestions');

    btn.onclick = async () => {
        const company = document.getElementById('sureCompanySelect').value;
        const role = document.getElementById('sureRoleSelect').value;

        if (!company) {
            alert('Please select a company');
            return;
        }

        try {
            const data = await window.api.getSureQuestions(company, role);
            renderSureQuestions(data);
        } catch (error) {
            console.error('Failed to load sure questions:', error);
            alert('Failed to load questions.');
        }
    };
}

function renderSureQuestions(data) {
    const container = document.getElementById('sureQuestionsList');
    const categories = ['behavioral', 'technical', 'coding'];

    container.innerHTML = categories.map(cat => {
        const questions = data.questions[cat] || [];
        if (questions.length === 0) return '';

        return `
            <div class="question-group">
                <h3 class="category-title">${cat.charAt(0).toUpperCase() + cat.slice(1)}</h3>
                <div class="questions-grid">
                    ${questions.map(q => `
                        <div class="question-card">
                            <div class="q-header">
                                <span class="difficulty ${q.difficulty.toLowerCase()}">${q.difficulty}</span>
                                <span class="frequency">🔥 ${q.frequency_score} times</span>
                            </div>
                            <p class="q-text">${q.question_text}</p>
                            <div class="q-footer">
                                <button class="btn-small-outline" onclick="prepareAnswer('${btoa(q.question_text)}')">Practice Answer</button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }).join('');
}

function prepareAnswer(qBase64) {
    const q = atob(qBase64);
    alert('This feature is coming soon! You can practice this in Skill Practice mode.');
}
