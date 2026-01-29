/**
 * AI Behavior Analyzer
 * Analyzes user behavior and provides real-time feedback
 */

class AIBehaviorAnalyzer {
    constructor(animationEngine) {
        this.animationEngine = animationEngine;
        this.feedbackRules = this.initializeFeedbackRules();
    }
    
    initializeFeedbackRules() {
        return {
            answerLength: {
                min: 50,
                max: 500,
                optimal: 200
            },
            responseTime: {
                min: 2000, // 2 seconds
                max: 30000, // 30 seconds
                optimal: 5000 // 5 seconds
            },
            confidence: {
                threshold: 0.5,
                excellent: 0.8
            },
            clarity: {
                threshold: 0.5,
                excellent: 0.8
            },
            structure: {
                threshold: 0.5,
                excellent: 0.8
            },
            hesitation: {
                threshold: 0.3 // 30% hesitation is concerning
            },
            speakingPace: {
                slow: 100, // words per minute
                optimal: 150,
                fast: 200
            }
        };
    }
    
    analyzeAnswer(answer, metrics = {}) {
        const analysis = {
            timestamp: Date.now(),
            answer: answer,
            metrics: metrics,
            feedback: [],
            score: 0,
            issues: [],
            strengths: []
        };
        
        // Analyze answer length
        this.analyzeLength(analysis);
        
        // Analyze metrics if provided
        if (Object.keys(metrics).length > 0) {
            this.analyzeMetrics(analysis);
        }
        
        // Analyze text content
        this.analyzeContent(analysis);
        
        // Calculate overall score
        analysis.score = this.calculateScore(analysis);
        
        // Queue feedback to animation engine
        this.queueFeedback(analysis);
        
        return analysis;
    }
    
    analyzeLength(analysis) {
        const len = analysis.answer.length;
        const rules = this.feedbackRules.answerLength;
        
        if (len < rules.min) {
            analysis.feedback.push({
                type: 'warning',
                message: 'Answer too short',
                severity: 2,
                suggestion: 'Provide more detail and examples'
            });
            analysis.issues.push('short_answer');
        } else if (len > rules.max) {
            analysis.feedback.push({
                type: 'warning',
                message: 'Answer too long',
                severity: 1,
                suggestion: 'Be more concise, focus on key points'
            });
            analysis.issues.push('long_answer');
        } else {
            analysis.strengths.push('appropriate_length');
        }
    }
    
    analyzeMetrics(analysis) {
        const metrics = analysis.metrics;
        
        // Confidence analysis
        if (metrics.confidence !== undefined) {
            if (metrics.confidence < this.feedbackRules.confidence.threshold) {
                analysis.feedback.push({
                    type: 'warning',
                    message: 'Low confidence detected',
                    severity: 1,
                    suggestion: 'Speak with more certainty'
                });
                analysis.issues.push('low_confidence');
            } else if (metrics.confidence >= this.feedbackRules.confidence.excellent) {
                analysis.feedback.push({
                    type: 'success',
                    message: 'Great confidence!',
                    severity: 0
                });
                analysis.strengths.push('high_confidence');
            }
        }
        
        // Clarity analysis
        if (metrics.clarity !== undefined) {
            if (metrics.clarity < this.feedbackRules.clarity.threshold) {
                analysis.feedback.push({
                    type: 'warning',
                    message: 'Clarity could be improved',
                    severity: 1,
                    suggestion: 'Articulate your words more clearly'
                });
                analysis.issues.push('low_clarity');
            } else if (metrics.clarity >= this.feedbackRules.clarity.excellent) {
                analysis.feedback.push({
                    type: 'success',
                    message: 'Clear articulation!',
                    severity: 0
                });
                analysis.strengths.push('high_clarity');
            }
        }
        
        // Structure analysis
        if (metrics.structure !== undefined) {
            if (metrics.structure < this.feedbackRules.structure.threshold) {
                analysis.feedback.push({
                    type: 'warning',
                    message: 'Answer lacks structure',
                    severity: 2,
                    suggestion: 'Use: Situation → Action → Result format'
                });
                analysis.issues.push('poor_structure');
            } else if (metrics.structure >= this.feedbackRules.structure.excellent) {
                analysis.feedback.push({
                    type: 'success',
                    message: 'Well-structured answer!',
                    severity: 0
                });
                analysis.strengths.push('good_structure');
            }
        }
        
        // Hesitation analysis
        if (metrics.hesitation !== undefined) {
            if (metrics.hesitation > this.feedbackRules.hesitation.threshold) {
                analysis.feedback.push({
                    type: 'info',
                    message: 'Too many hesitations detected',
                    severity: 1,
                    suggestion: 'Pause and collect thoughts before speaking'
                });
                analysis.issues.push('high_hesitation');
            }
        }
        
        // Speaking pace analysis
        if (metrics.pace !== undefined) {
            if (metrics.pace < this.feedbackRules.speakingPace.slow) {
                analysis.feedback.push({
                    type: 'info',
                    message: 'Speaking too slowly',
                    severity: 1,
                    suggestion: 'Pick up your pace slightly'
                });
                analysis.issues.push('slow_pace');
            } else if (metrics.pace > this.feedbackRules.speakingPace.fast) {
                analysis.feedback.push({
                    type: 'warning',
                    message: 'Speaking too quickly',
                    severity: 1,
                    suggestion: 'Slow down to improve clarity'
                });
                analysis.issues.push('fast_pace');
            } else {
                analysis.strengths.push('good_pace');
            }
        }
    }
    
    analyzeContent(analysis) {
        const answer = analysis.answer.toLowerCase();
        
        // Check for STAR method keywords
        const starKeywords = {
            situation: ['situation', 'context', 'faced', 'problem'],
            task: ['task', 'responsibility', 'challenge', 'goal'],
            action: ['action', 'implemented', 'decided', 'created', 'developed'],
            result: ['result', 'outcome', 'achieved', 'improved', 'succeeded']
        };
        
        let starScores = {
            situation: 0,
            task: 0,
            action: 0,
            result: 0
        };
        
        Object.entries(starKeywords).forEach(([component, keywords]) => {
            if (keywords.some(keyword => answer.includes(keyword))) {
                starScores[component] = 1;
            }
        });
        
        const starScore = Object.values(starScores).reduce((a, b) => a + b) / 4;
        
        if (starScore >= 0.75) {
            analysis.feedback.push({
                type: 'success',
                message: 'Good STAR method usage!',
                severity: 0
            });
            analysis.strengths.push('uses_star_method');
        } else if (starScore > 0) {
            analysis.feedback.push({
                type: 'info',
                message: 'Consider using full STAR format',
                severity: 1,
                suggestion: 'Include Situation, Task, Action, Result'
            });
        }
        
        // Check for specific achievements/metrics
        if (/\d+%|increase|improve|reduce|save|generate|revenue|profit/.test(answer)) {
            analysis.feedback.push({
                type: 'success',
                message: 'Good use of metrics!',
                severity: 0
            });
            analysis.strengths.push('includes_metrics');
        }
    }
    
    calculateScore(analysis) {
        let score = 50; // Base score
        
        // Add points for strengths
        score += analysis.strengths.length * 10;
        
        // Deduct points for issues by severity
        analysis.feedback.forEach(fb => {
            if (fb.severity === 2) score -= 10;
            else if (fb.severity === 1) score -= 5;
        });
        
        // Length bonus
        const len = analysis.answer.length;
        const optimalLen = this.feedbackRules.answerLength.optimal;
        const lengthScore = Math.max(0, 20 * (1 - Math.abs(len - optimalLen) / optimalLen));
        score += lengthScore;
        
        return Math.max(0, Math.min(100, Math.round(score)));
    }
    
    queueFeedback(analysis) {
        // Queue up to 3 most important feedback items
        const prioritized = analysis.feedback
            .sort((a, b) => b.severity - a.severity)
            .slice(0, 3);
        
        prioritized.forEach((fb, index) => {
            setTimeout(() => {
                if (this.animationEngine) {
                    this.animationEngine.queueFeedback(
                        fb.message,
                        fb.type,
                        3000 + (index * 500)
                    );
                }
            }, index * 1000);
        });
    }
    
    provideSummary(sessions) {
        const completed = sessions.filter(s => s.status === 'completed');
        
        if (completed.length === 0) {
            return 'No completed interviews yet. Start practicing!';
        }
        
        const recentSessions = completed.slice(-5);
        const avgScore = Math.round(recentSessions.reduce((sum, s) => sum + s.score, 0) / recentSessions.length);
        const improvement = recentSessions.length > 1 
            ? recentSessions[recentSessions.length - 1].score - recentSessions[0].score
            : 0;
        
        let summary = `You've completed ${recentSessions.length} recent interviews. `;
        summary += `Average score: ${avgScore}%. `;
        
        if (improvement > 0) {
            summary += `Excellent improvement of ${improvement} points! `;
        } else if (improvement < 0) {
            summary += `Recent scores trending down. Focus on fundamentals. `;
        }
        
        if (avgScore < 50) {
            summary += 'Keep practicing - consistency is key!';
        } else if (avgScore < 75) {
            summary += 'Good progress! Review feedback and try advanced companies.';
        } else {
            summary += 'Excellent! You\'re interview-ready!';
        }
        
        return summary;
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIBehaviorAnalyzer;
}
