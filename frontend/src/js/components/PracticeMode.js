/**
 * Skill Practice Mode Component
 * Educational flow: Explain -> Question -> Feedback
 */

let currentPracticeSessionId = null;

function PracticeModePage() {
    return `
        <div class="practice-container">
            <div id="practiceSetup" class="glass-card setup-card">
                <h2>🎓 Skill Practice Mode</h2>
                <p>Master specific concepts with an explain-first approach.</p>
                
                <div class="skill-selection">
                    <label>Select Skill Area</label>
                    <div class="skill-options">
                        <div class="skill-opt active" data-cat="soft_skills">
                            <span class="icon">💬</span>
                            <span>Soft Skills</span>
                        </div>
                        <div class="skill-opt" data-cat="technical">
                            <span class="icon">⚙️</span>
                            <span>Technical Knowledge</span>
                        </div>
                        <div class="skill-opt" data-cat="coding_basics">
                            <span class="icon">💻</span>
                            <span>Coding Basics</span>
                        </div>
                    </div>
                </div>

                <div class="level-selection">
                    <label>Difficulty Level</label>
                    <div class="level-options">
                        <button class="level-btn active" data-level="Beginner">Beginner</button>
                        <button class="level-btn" data-level="Intermediate">Intermediate</button>
                        <button class="level-btn" data-level="Advanced">Advanced</button>
                    </div>
                </div>

                <button class="btn-primary full-width" id="btnStartPractice">Start Learning</button>
            </div>

            <div id="practiceContent" class="hidden">
                <div class="glass-card explanation-card">
                    <h3 id="practiceConcept"></h3>
                    <div id="practiceExplanation" class="explanation-text markdown"></div>
                </div>

                <div class="glass-card question-card">
                    <h4>Practice Question</h4>
                    <p id="practiceQuestion" class="question-text"></p>
                    <textarea id="practiceAnswer" placeholder="Type your answer here..." class="glass-textarea"></textarea>
                    <div class="actions">
                        <button class="btn-primary" id="btnSubmitPractice">Submit Answer</button>
                    </div>
                </div>
            </div>

            <div id="practiceFeedback" class="hidden">
                <div class="glass-card feedback-card">
                    <h3>Feedback</h3>
                    <div id="feedbackText" class="feedback-text"></div>
                    
                    <div class="approach-box">
                        <h4>Optimal Approach</h4>
                        <div id="approachText"></div>
                    </div>

                    <div class="tips-box">
                        <h4>Improvement Tips</h4>
                        <ul id="tipsList"></ul>
                    </div>

                    <button class="btn-primary full-width" id="btnNextPractice">Next Concept</button>
                </div>
            </div>

            <div id="practiceLoader" class="loader-container hidden">
                <div class="spinner"></div>
                <p id="loaderMessage">Generating your session...</p>
            </div>
        </div>
    `;
}

async function initPracticeMode() {
    const setupEl = document.getElementById('practiceSetup');
    const contentEl = document.getElementById('practiceContent');
    const feedbackEl = document.getElementById('practiceFeedback');
    const skillOpts = document.querySelectorAll('.skill-opt');
    const levelBtns = document.querySelectorAll('.level-btn');

    let selectedCat = 'soft_skills';
    let selectedLevel = 'Beginner';

    skillOpts.forEach(opt => opt.onclick = () => {
        skillOpts.forEach(o => o.classList.remove('active'));
        opt.classList.add('active');
        selectedCat = opt.dataset.cat;
    });

    levelBtns.forEach(btn => btn.onclick = () => {
        levelBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedLevel = btn.dataset.level;
    });

    document.getElementById('btnStartPractice').onclick = async () => {
        try {
            showPracticeLoader(true, "Preparing your lesson...");
            const data = await window.api.startPractice(selectedCat, selectedLevel);
            currentPracticeSessionId = data.session_id;
            displayPracticeStep(data.step);
            setupEl.classList.add('hidden');
            contentEl.classList.remove('hidden');
        } catch (error) {
            console.error('Practice failed:', error);
            alert('Failed to start practice.');
        } finally {
            showPracticeLoader(false);
        }
    };

    document.getElementById('btnSubmitPractice').onclick = async () => {
        const answer = document.getElementById('practiceAnswer').value;
        if (!answer.trim()) return;

        try {
            showPracticeLoader(true, "Evaluating your response...");
            const feedback = await window.api.submitPracticeAnswer(currentPracticeSessionId, answer);
            displayPracticeFeedback(feedback);
            contentEl.classList.add('hidden');
            feedbackEl.classList.remove('hidden');
        } catch (error) {
            console.error('Feedback failed:', error);
        } finally {
            showPracticeLoader(false);
        }
    };

    document.getElementById('btnNextPractice').onclick = async () => {
        try {
            showPracticeLoader(true, "Creating next lesson...");
            const step = await window.api.getNextPracticeStep(currentPracticeSessionId);
            displayPracticeStep(step);
            feedbackEl.classList.add('hidden');
            contentEl.classList.remove('hidden');
            document.getElementById('practiceAnswer').value = '';
        } catch (error) {
            console.error('Next step failed:', error);
        } finally {
            showPracticeLoader(false);
        }
    };
}

function showPracticeLoader(show, message = "") {
    const loader = document.getElementById('practiceLoader');
    if (message) document.getElementById('loaderMessage').textContent = message;
    loader.classList.toggle('hidden', !show);
}

function displayPracticeStep(step) {
    document.getElementById('practiceConcept').textContent = step.concept;
    document.getElementById('practiceExplanation').innerHTML = formatMarkdown(step.explanation);
    document.getElementById('practiceQuestion').textContent = step.practice_question;
}

function displayPracticeFeedback(feedback) {
    document.getElementById('feedbackText').textContent = feedback.feedback;
    document.getElementById('approachText').innerHTML = formatMarkdown(feedback.correct_approach);
    document.getElementById('tipsList').innerHTML = feedback.improvement_tips.map(t => `<li>${t}</li>`).join('');
}

function formatMarkdown(text) {
    // Simple basic markdown formatting if no library present
    return text
        .replace(/\n\n/g, '<br><br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^- (.*)$/gm, '<li>$1</li>')
        .replace(/<li>(.*?)<\/li>/g, (match, content) => `<ul><li>${content}</li></ul>`)
        .replace(/<\/ul><ul>/g, '');
}
