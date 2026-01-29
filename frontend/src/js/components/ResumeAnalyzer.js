/**
 * Resume Analyzer Component
 * Logic for uploading and displaying resume analysis.
 */

function ResumeAnalyzerPage() {
    return `
        <div class="resume-analyzer-container">
            <div class="glass-card analyzer-card">
                <h2>📄 Resume Analyzer</h2>
                <p class="subtitle">Get instantly rated and receive actionable improvement tips for your target role.</p>
                
                <div class="analyzer-form">
                    <div class="form-group">
                        <label>Target Role</label>
                        <input type="text" id="resumeTargetRole" placeholder="e.g. Senior Software Engineer" class="glass-input">
                    </div>
                    <div class="form-group">
                        <label>Target Company (Optional)</label>
                        <input type="text" id="resumeTargetCompany" placeholder="e.g. Google" class="glass-input">
                    </div>
                    <div class="file-upload-zone" id="resumeUploadZone">
                        <input type="file" id="resumeFile" accept=".pdf,.docx" hidden>
                        <div class="upload-content">
                            <span class="upload-icon">☁️</span>
                            <p>Click to upload or drag and drop</p>
                            <p class="file-info">PDF or DOCX (Max 5MB)</p>
                        </div>
                        <div id="selectedFileName" class="selected-file-name"></div>
                    </div>
                    
                    <button class="btn-primary full-width" id="btnAnalyzeResume">
                        Analyze Resume
                    </button>
                </div>
            </div>

            <div id="resumeAnalysisResults" class="results-container hidden">
                <!-- Analysis results will be rendered here -->
            </div>

            <div id="analyzerLoader" class="loader-container hidden">
                <div class="spinner"></div>
                <p>Analyzing your resume against industry standards...</p>
            </div>
        </div>
    `;
}

async function initResumeAnalyzer() {
    const uploadZone = document.getElementById('resumeUploadZone');
    const fileInput = document.getElementById('resumeFile');
    const fileNameEl = document.getElementById('selectedFileName');
    const btnAnalyze = document.getElementById('btnAnalyzeResume');

    uploadZone.onclick = () => fileInput.click();

    fileInput.onchange = (e) => {
        if (e.target.files.length > 0) {
            fileNameEl.textContent = `Selected: ${e.target.files[0].name}`;
            fileNameEl.classList.add('active');
        }
    };

    btnAnalyze.onclick = async () => {
        const file = fileInput.files[0];
        const role = document.getElementById('resumeTargetRole').value;
        const company = document.getElementById('resumeTargetCompany').value;

        if (!file || !role) {
            alert('Please select a file and enter a target role.');
            return;
        }

        try {
            showAnalyzerLoader(true);
            const results = await window.api.analyzeResume(file, role, company);

            // If results is null (e.g. from 401 redirect), don't try to render
            if (!results) return;

            renderResumeResults(results);
        } catch (error) {
            console.error('Analysis failed:', error);
            alert('Analysis failed: ' + error.message);
        } finally {
            showAnalyzerLoader(false);
        }
    };
}

function showAnalyzerLoader(show) {
    document.getElementById('analyzerLoader').classList.toggle('hidden', !show);
    document.getElementById('resumeAnalysisResults').classList.toggle('hidden', show);
}

function renderResumeResults(data) {
    if (!data) return;

    const container = document.getElementById('resumeAnalysisResults');
    container.classList.remove('hidden');

    const rating = data.rating ?? 0;
    const ratingColor = rating >= 4 ? '#00e676' : (rating >= 3 ? '#ffeb3b' : '#ff5252');

    container.innerHTML = `
        <div class="glass-card results-card">
            <div class="rating-header">
                <div class="rating-circle" style="border-color: ${ratingColor}">
                    <span class="rating-value" style="color: ${ratingColor}">${rating}</span>
                    <span class="rating-total">/ 5</span>
                </div>
                <div class="rating-text">
                    <h3>Overall Rating</h3>
                    <p>${getRatingLabel(rating)}</p>
                </div>
            </div>

            <div class="analysis-grid">
                <div class="analysis-section">
                    <h4>✅ Strengths</h4>
                    <ul>${(data.strengths ?? []).map(s => `<li>${s}</li>`).join('')}</ul>
                </div>
                <div class="analysis-section">
                    <h4>⚠️ Weaknesses</h4>
                    <ul>${(data.weaknesses ?? []).map(w => `<li>${w}</li>`).join('')}</ul>
                </div>
            </div>

            <div class="analysis-section missing-skills">
                <h4>🎯 Missing Critical Skills</h4>
                <div class="skills-tags">
                    ${(data.missing_skills ?? []).map(s => `<span class="skill-tag">${s}</span>`).join('')}
                </div>
            </div>

            <div class="analysis-section suggestions">
                <h4>💡 Improvement Suggestions</h4>
                <div class="suggestion-items">
                    ${(data.replace_suggestions ?? []).map(s => `
                        <div class="suggestion-item">
                            <span class="original">Replace: "${s.original}"</span>
                            <span class="arrow">→</span>
                            <span class="suggested">"${s.suggested}"</span>
                        </div>
                    `).join('')}
                </div>
            </div>

            <div class="analysis-section rewrites">
                <h4>✍️ Power Rewrites</h4>
                ${(data.rewrite_examples ?? []).map(ex => `
                    <div class="rewrite-card">
                        <div class="rewrite-before"><strong>Before:</strong> ${ex.before}</div>
                        <div class="rewrite-after"><strong>After:</strong> ${ex.after}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function getRatingLabel(rating) {
    if (rating >= 4.5) return "Excellent - Interview Ready!";
    if (rating >= 3.5) return "Good - Some minor tweaks needed";
    if (rating >= 2.5) return "Fair - Needs improvement";
    return "Weak - Requires significant rework";
}
