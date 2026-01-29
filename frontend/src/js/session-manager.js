/**
 * Interview Session Manager
 * Handles interview sessions, timeline, playback, and persistence
 */

class InterviewSessionManager {
    constructor() {
        this.sessions = this.loadSessions();
        this.currentSession = null;
        this.interviewMode = 'practice';
    }
    
    createSession(companyName, difficulty, targetReadiness) {
        const session = {
            id: this.generateId(),
            createdAt: new Date().toISOString(),
            company: companyName,
            difficulty: difficulty,
            mode: this.interviewMode,
            status: 'in-progress', // in-progress, completed, paused
            startTime: Date.now(),
            endTime: null,
            duration: 0,
            questions: [],
            answers: [],
            score: 0,
            feedback: [],
            readinessGain: 0,
            targetReadiness: targetReadiness,
            voiceData: [] // For voice reactivity analysis
        };
        
        this.currentSession = session;
        this.sessions.push(session);
        this.saveSessions();
        return session;
    }
    
    addQuestion(question) {
        if (!this.currentSession) return;
        
        this.currentSession.questions.push({
            text: question,
            timestamp: Date.now(),
            index: this.currentSession.questions.length
        });
        
        this.saveSessions();
    }
    
    addAnswer(answer, confidence = 0, clarity = 0, structure = 0) {
        if (!this.currentSession) return;
        
        const answerData = {
            text: answer,
            timestamp: Date.now(),
            confidence,
            clarity,
            structure,
            quality: (confidence + clarity + structure) / 3,
            feedback: this.generateFeedback(answer, confidence, clarity, structure)
        };
        
        this.currentSession.answers.push(answerData);
        this.saveSessions();
        
        return answerData;
    }
    
    generateFeedback(answer, confidence, clarity, structure) {
        const feedback = [];
        
        if (answer.length < 50) {
            feedback.push({ type: 'warning', message: 'Answer too short', severity: 2 });
        }
        if (answer.length > 500) {
            feedback.push({ type: 'warning', message: 'Answer too long', severity: 1 });
        }
        
        if (clarity < 0.5) {
            feedback.push({ type: 'warning', message: 'Lack of clarity', severity: 2 });
        }
        if (structure < 0.5) {
            feedback.push({ type: 'warning', message: 'Lack of structure', severity: 2 });
        }
        
        if (confidence > 0.8) {
            feedback.push({ type: 'success', message: 'Good confidence', severity: 0 });
        }
        if (clarity > 0.8) {
            feedback.push({ type: 'success', message: 'Clear articulation', severity: 0 });
        }
        if (structure > 0.8) {
            feedback.push({ type: 'success', message: 'Well-structured', severity: 0 });
        }
        
        return feedback;
    }
    
    completeSession(score, feedback = []) {
        if (!this.currentSession) return;
        
        this.currentSession.endTime = new Date().toISOString();
        this.currentSession.duration = Date.now() - this.currentSession.startTime;
        this.currentSession.score = score;
        this.currentSession.feedback = feedback;
        this.currentSession.status = 'completed';
        
        // Calculate readiness gain
        this.currentSession.readinessGain = Math.min(score * 0.5, 25);
        
        this.saveSessions();
        
        return this.currentSession;
    }
    
    pauseSession() {
        if (!this.currentSession) return;
        this.currentSession.status = 'paused';
        this.saveSessions();
    }
    
    resumeSession() {
        if (!this.currentSession) return;
        this.currentSession.status = 'in-progress';
        this.currentSession.startTime = Date.now() - (this.currentSession.duration || 0);
        this.saveSessions();
    }
    
    getCurrentSession() {
        return this.currentSession;
    }
    
    getSession(id) {
        return this.sessions.find(s => s.id === id);
    }
    
    getSessions() {
        return this.sessions;
    }
    
    getSessionsByCompany(company) {
        return this.sessions.filter(s => s.company.toLowerCase() === company.toLowerCase());
    }
    
    getCompletedSessions() {
        return this.sessions.filter(s => s.status === 'completed');
    }
    
    getStats() {
        const completed = this.getCompletedSessions();
        
        if (completed.length === 0) {
            return {
                totalInterviews: 0,
                averageScore: 0,
                highestScore: 0,
                totalPracticeTime: 0,
                companiesInterviewed: 0,
                readinessGain: 0,
                improvementTrend: []
            };
        }
        
        return {
            totalInterviews: completed.length,
            averageScore: Math.round(completed.reduce((sum, s) => sum + s.score, 0) / completed.length),
            highestScore: Math.max(...completed.map(s => s.score)),
            totalPracticeTime: completed.reduce((sum, s) => sum + s.duration, 0),
            companiesInterviewed: new Set(completed.map(s => s.company)).size,
            readinessGain: Math.round(completed.reduce((sum, s) => sum + s.readinessGain, 0)),
            improvementTrend: this.calculateTrend(completed)
        };
    }
    
    calculateTrend(sessions) {
        // Calculate score trend over last 5 sessions
        return sessions.slice(-5).map((s, i) => ({
            index: i,
            score: s.score,
            company: s.company,
            date: new Date(s.createdAt).toLocaleDateString()
        }));
    }
    
    getSessionTimeline() {
        return this.sessions
            .filter(s => s.status === 'completed')
            .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
            .map(s => ({
                id: s.id,
                company: s.company,
                score: s.score,
                difficulty: s.difficulty,
                mode: s.mode,
                duration: Math.round(s.duration / 1000 / 60), // minutes
                date: new Date(s.createdAt),
                readinessGain: s.readinessGain
            }));
    }
    
    deleteSession(id) {
        const index = this.sessions.findIndex(s => s.id === id);
        if (index !== -1) {
            this.sessions.splice(index, 1);
            if (this.currentSession && this.currentSession.id === id) {
                this.currentSession = null;
            }
            this.saveSessions();
            return true;
        }
        return false;
    }
    
    generateId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    saveSessions() {
        try {
            localStorage.setItem('interviewSessions', JSON.stringify(this.sessions));
        } catch (e) {
            console.error('Failed to save sessions:', e);
        }
    }
    
    loadSessions() {
        try {
            const data = localStorage.getItem('interviewSessions');
            return data ? JSON.parse(data) : [];
        } catch (e) {
            console.error('Failed to load sessions:', e);
            return [];
        }
    }
    
    exportSessions() {
        return JSON.stringify(this.sessions, null, 2);
    }
    
    importSessions(jsonData) {
        try {
            const imported = JSON.parse(jsonData);
            if (Array.isArray(imported)) {
                this.sessions = [...this.sessions, ...imported];
                this.saveSessions();
                return true;
            }
        } catch (e) {
            console.error('Failed to import sessions:', e);
        }
        return false;
    }
    
    clearAllSessions() {
        if (confirm('Are you sure you want to delete all interview sessions? This cannot be undone.')) {
            this.sessions = [];
            this.currentSession = null;
            this.saveSessions();
            return true;
        }
        return false;
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = InterviewSessionManager;
}
