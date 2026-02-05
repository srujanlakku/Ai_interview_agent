/**
 * API Client
 * HTTP client for communicating with InterviewPilot backend
 */

class APIClient {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
        this.timeout = 10000;
        this.token = localStorage.getItem('accessToken');
    }

    /**
     * Set authentication token
     */
    setToken(token) {
        this.token = token;
        localStorage.setItem('accessToken', token);
    }

    /**
     * Get authentication token
     */
    getToken() {
        return this.token || localStorage.getItem('accessToken');
    }

    /**
     * Remove authentication token
     */
    removeToken() {
        this.token = null;
        localStorage.removeItem('accessToken');
    }

    /**
     * Build request headers
     */
    buildHeaders(options = {}) {
        const headers = {
            ...options
        };

        // Only add JSON content type if not explicitly set to null or other value
        if (options['Content-Type'] === undefined) {
            headers['Content-Type'] = 'application/json';
        } else if (options['Content-Type'] === null) {
            delete headers['Content-Type'];
        }

        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        return headers;
    }

    /**
     * Make HTTP request with timeout
     */
    async request(method, endpoint, data = null, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        let body = data;
        if (data && !(data instanceof FormData) && options.headers?.['Content-Type'] !== null) {
            body = JSON.stringify(data);
        }

        const config = {
            method,
            headers: this.buildHeaders(options.headers),
            signal: AbortSignal.timeout(this.timeout)
        };

        if (body) {
            config.body = body;
        }

        try {
            const response = await fetch(url, config);

            // Handle 401 Unauthorized
            if (response.status === 401) {
                console.warn('Session expired or invalid credentials. Redirecting to login.');
                this.removeToken();
                // Clear other auth state if global auth exists
                if (window.auth) window.auth.clearAuth();
                window.location.href = '/';
                return null;
            }

            const responseData = await response.json();

            if (!response.ok) {
                let errorMessage = responseData.message || responseData.detail || 'API Error';
                if (Array.isArray(responseData.detail)) {
                    errorMessage = responseData.detail.map(err => err.msg || JSON.stringify(err)).join(', ');
                }
                throw new Error(errorMessage);
            }

            return responseData;
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timeout');
            }
            throw error;
        }
    }

    /**
     * GET request
     */
    async get(endpoint, options = {}) {
        return this.request('GET', endpoint, null, options);
    }

    /**
     * POST request
     */
    async post(endpoint, data, options = {}) {
        return this.request('POST', endpoint, data, options);
    }

    /**
     * PUT request
     */
    async put(endpoint, data, options = {}) {
        return this.request('PUT', endpoint, data, options);
    }

    /**
     * DELETE request
     */
    async delete(endpoint, options = {}) {
        return this.request('DELETE', endpoint, null, options);
    }

    /**
     * PATCH request
     */
    async patch(endpoint, data, options = {}) {
        return this.request('PATCH', endpoint, data, options);
    }

    /**
     * Authentication Endpoints
     */

    async signup(email, password, full_name = '') {
        return this.post('/api/auth/signup', { email, password, full_name });
    }

    async login(email, password) {
        return this.post('/api/auth/login', { email, password });
    }

    async logout() {
        return this.post('/api/auth/logout', {});
    }

    async getCurrentUser() {
        return this.get('/api/auth/me');
    }

    /**
     * Profile Endpoints
     */

    async onboardUser(data) {
        return this.post('/api/profile/onboard', data);
    }

    async getProfile() {
        return this.get('/api/profile/get');
    }

    async prepareProfile(role) {
        return this.post('/api/profile/prepare', { role });
    }

    /**
     * Interview Endpoints
     */

    async createInterview(companyName, role = 'Software Engineer', difficulty = 'medium') {
        const data = typeof companyName === 'object' ? companyName : {
            company_name: companyName,
            job_role: role,
            interview_type: 'mock'
        };

        // Ensure interview_type is present as it's required by the backend
        if (!data.interview_type) {
            data.interview_type = 'mock';
        }

        return this.post('/api/interviews/create', data);
    }

    async getInterview(interviewId) {
        return this.get(`/api/interviews/${interviewId}`);
    }

    async getUserInterviews(limit = 10) {
        return this.get('/api/interviews/user/list?limit=' + limit);
    }

    async getInterviewQuestions(interviewId) {
        return this.get(`/api/interviews/${interviewId}/questions`);
    }

    async submitAnswer(interviewId, answer) {
        return this.post(`/api/interviews/${interviewId}/submit-answer`, { answer: answer });
    }

    async getNextQuestion(interviewId) {
        return this.post(`/api/interviews/${interviewId}/start-question`, {});
    }

    async finalizeInterview(interviewId) {
        return this.post(`/api/interviews/${interviewId}/finalize`, {});
    }

    async getInterviewStatistics() {
        return this.get('/api/interviews/all/statistics');
    }

    /**
     * Memory Endpoints
     */

    async getMemorySummary() {
        return this.get('/api/memory/summary');
    }

    async getStrengths() {
        return this.get('/api/memory/strengths');
    }

    async getWeaknesses() {
        return this.get('/api/memory/weaknesses');
    }

    async getCoveredTopics() {
        return this.get('/api/memory/covered-topics');
    }

    async getMissedTopics() {
        return this.get('/api/memory/missed-topics');
    }

    /**
     * Speech Endpoints
     */

    async transcribeAudio(audioData) {
        const formData = new FormData();
        formData.append('file', audioData);

        return fetch(`${this.baseURL}/api/speech/transcribe`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`
            },
            body: formData
        }).then(r => r.json());
    }

    async getSpeechLanguages() {
        return this.get('/api/speech/languages');
    }

    async getTranscriptionStatus(transcriptionId) {
        return this.get(`/api/speech/status/${transcriptionId}`);
    }

    /**
     * Health Check
     */

    async healthCheck() {
        try {
            return await this.get('/health');
        } catch (error) {
            return { status: 'unhealthy', error: error.message };
        }
    }

    /**
     * NEW: Interview Review API
     */
    async getInterviewReview(interviewId) {
        return this.get(`/api/interviews/${interviewId}/review`);
    }

    /**
     * NEW: Dashboard Analytics APIs
     */
    async getTopQuestions(company, role, limit = 20) {
        return this.get(`/api/dashboard/top-questions?company=${encodeURIComponent(company)}&role=${encodeURIComponent(role)}&limit=${limit}`);
    }

    async getCompanyStats(company) {
        return this.get(`/api/dashboard/company-stats?company=${encodeURIComponent(company)}`);
    }

    async getRoleCategories(role) {
        return this.get(`/api/dashboard/role-categories?role=${encodeURIComponent(role)}`);
    }

    /**
     * FEATURE 1: Resume Analyzer
     */
    async analyzeResume(file, role, company = "") {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('target_role', role);
        if (company) formData.append('target_company', company);

        // For FormData, we must NOT set Content-Type header manually
        // so the browser can set it with the correct boundary
        return this.request('POST', '/api/resume/analyze', formData, {
            headers: { 'Content-Type': null }
        });
    }

    /**
     * FEATURE 2: Sure Questions
     */
    async getSureQuestions(company, role) {
        return this.get(`/api/dashboard/sure-questions?company=${encodeURIComponent(company)}&role=${encodeURIComponent(role)}`);
    }

    /**
     * FEATURE 3: Practice Mode
     */
    async startPractice(skillCategory, level) {
        return this.post('/api/practice/start', {
            skill_category: skillCategory,
            level: level
        });
    }

    async submitPracticeAnswer(sessionId, answer) {
        return this.post('/api/practice/submit', {
            session_id: sessionId,
            user_answer: answer
        });
    }

    async getNextPracticeStep(sessionId) {
        return this.get(`/api/practice/${sessionId}/next`);
    }
}

// Create global API client instance
window.api = new APIClient();
