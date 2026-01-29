/**
 * Elite Animation Engine
 * Advanced code rain with voice reactivity, interview modes, and AI behavior feedback
 */

class EliteAnimationEngine {
    constructor(canvasId, config = {}) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) throw new Error(`Canvas with ID "${canvasId}" not found`);
        
        this.ctx = this.canvas.getContext('2d');
        this.setupCanvas();
        
        // Configuration
        this.config = {
            speed: config.speed || 1.5,
            opacity: config.opacity || 0.6,
            density: config.density || 0.15,
            glowIntensity: config.glowIntensity || 0.8,
            voiceReactive: config.voiceReactive !== false,
            ...config
        };
        
        // State
        this.columns = [];
        this.isRunning = false;
        this.animationId = null;
        this.characters = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
        
        // Voice reactivity
        this.audioContext = null;
        this.analyser = null;
        this.dataArray = null;
        this.voiceIntensity = 0;
        this.targetIntensity = 0;
        
        // Interview mode
        this.interviewMode = 'practice'; // practice, pressure, extreme
        this.modeIntensityMultiplier = {
            practice: 0.6,
            pressure: 1.2,
            extreme: 2.0
        };
        
        // AI feedback system
        this.feedbackQueue = [];
        this.activeFeedback = null;
        this.feedbackTimeout = null;
        
        // Performance metrics
        this.frameCount = 0;
        this.fps = 60;
        this.lastTime = Date.now();
        
        // Initialize columns
        this.initColumns();
        
        // Setup event listeners
        window.addEventListener('resize', () => this.handleResize());
        
        // Setup voice reactivity if enabled
        if (this.config.voiceReactive) {
            this.setupVoiceReactivity();
        }
    }
    
    setupCanvas() {
        const dpr = window.devicePixelRatio || 1;
        this.canvas.width = window.innerWidth * dpr;
        this.canvas.height = window.innerHeight * dpr;
        this.ctx.scale(dpr, dpr);
    }
    
    handleResize() {
        this.setupCanvas();
        this.initColumns();
    }
    
    initColumns() {
        const width = this.canvas.width / window.devicePixelRatio;
        const charWidth = 10;
        this.columns = [];
        
        const columnCount = Math.ceil(width / charWidth);
        for (let i = 0; i < columnCount; i++) {
            this.columns.push({
                x: i * charWidth,
                y: Math.random() * this.canvas.height,
                speed: this.config.speed,
                opacity: this.config.opacity,
                chars: this.getRandomCharSequence(20)
            });
        }
    }
    
    getRandomCharSequence(length) {
        let sequence = '';
        for (let i = 0; i < length; i++) {
            sequence += this.characters.charAt(Math.floor(Math.random() * this.characters.length));
        }
        return sequence;
    }
    
    setupVoiceReactivity() {
        // Request microphone access
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                if (!this.audioContext) {
                    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                }
                
                const source = this.audioContext.createMediaStreamSource(stream);
                this.analyser = this.audioContext.createAnalyser();
                this.analyser.fftSize = 256;
                
                source.connect(this.analyser);
                
                const bufferLength = this.analyser.frequencyBinCount;
                this.dataArray = new Uint8Array(bufferLength);
                
                // Start analyzing
                this.updateVoiceIntensity();
            })
            .catch(err => {
                console.log('Microphone access denied - voice reactivity disabled', err);
            });
    }
    
    updateVoiceIntensity() {
        if (!this.analyser || !this.dataArray) return;
        
        this.analyser.getByteFrequencyData(this.dataArray);
        
        // Calculate average frequency
        let sum = 0;
        for (let i = 0; i < this.dataArray.length; i++) {
            sum += this.dataArray[i];
        }
        
        this.targetIntensity = (sum / this.dataArray.length) / 255; // 0 to 1
        this.voiceIntensity += (this.targetIntensity - this.voiceIntensity) * 0.1; // Smooth transition
        
        requestAnimationFrame(() => this.updateVoiceIntensity());
    }
    
    applyVoiceReactivity() {
        if (!this.config.voiceReactive) return;
        
        const multiplier = this.modeIntensityMultiplier[this.interviewMode] || 1;
        
        // Apply voice intensity to visual properties
        this.columns.forEach(col => {
            const intensity = this.voiceIntensity * multiplier;
            
            // Speed increases with voice intensity
            col.speed = this.config.speed * (1 + intensity * 2);
            
            // Opacity increases with voice intensity
            col.opacity = Math.min(this.config.opacity * (1 + intensity), 1);
        });
    }
    
    setInterviewMode(mode) {
        if (!['practice', 'pressure', 'extreme'].includes(mode)) {
            console.warn(`Unknown interview mode: ${mode}`);
            return;
        }
        this.interviewMode = mode;
    }
    
    queueFeedback(message, type = 'info', duration = 3000) {
        this.feedbackQueue.push({ message, type, duration, timestamp: Date.now() });
    }
    
    showNextFeedback() {
        if (this.feedbackTimeout) clearTimeout(this.feedbackTimeout);
        
        if (this.feedbackQueue.length === 0) {
            this.activeFeedback = null;
            return;
        }
        
        this.activeFeedback = this.feedbackQueue.shift();
        
        this.feedbackTimeout = setTimeout(() => {
            this.showNextFeedback();
        }, this.activeFeedback.duration);
    }
    
    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.animate();
    }
    
    stop() {
        this.isRunning = false;
        if (this.animationId) cancelAnimationFrame(this.animationId);
    }
    
    animate() {
        if (!this.isRunning) return;
        
        // Clear canvas
        this.ctx.fillStyle = 'rgba(10, 14, 39, 0.3)';
        this.ctx.fillRect(0, 0, this.canvas.width / window.devicePixelRatio, this.canvas.height / window.devicePixelRatio);
        
        // Apply voice reactivity
        this.applyVoiceReactivity();
        
        // Draw code rain
        this.drawCodeRain();
        
        // Draw feedback overlay
        this.drawFeedbackOverlay();
        
        // Draw performance metrics (debug)
        this.updateFPS();
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }
    
    drawCodeRain() {
        const width = this.canvas.width / window.devicePixelRatio;
        const height = this.canvas.height / window.devicePixelRatio;
        
        this.columns.forEach((col, idx) => {
            // Create gradient for glow effect
            const gradient = this.ctx.createLinearGradient(col.x, col.y - 100, col.x, col.y + 100);
            
            const hue = this.interviewMode === 'extreme' ? 0 : 120; // Red for extreme mode
            const saturation = this.interviewMode === 'extreme' ? 100 : 50;
            const lightness = this.interviewMode === 'extreme' ? 50 : 50;
            
            gradient.addColorStop(0, `hsla(${hue}, ${saturation}%, ${lightness}%, 0)`);
            gradient.addColorStop(0.5, `hsla(${hue}, ${saturation}%, ${lightness}%, ${col.opacity})`);
            gradient.addColorStop(1, `hsla(${hue}, ${saturation}%, ${lightness}%, 0)`);
            
            this.ctx.fillStyle = gradient;
            this.ctx.font = '14px "JetBrains Mono", monospace';
            this.ctx.shadowColor = `hsla(${hue}, ${saturation}%, ${lightness}%, ${this.config.glowIntensity})`;
            this.ctx.shadowBlur = 10 + (this.voiceIntensity * 10);
            
            // Draw characters
            const chars = col.chars.split('');
            chars.forEach((char, i) => {
                const y = col.y + i * 16;
                if (y < height + 100) {
                    this.ctx.fillText(char, col.x, y);
                }
            });
            
            // Update position
            col.y += col.speed * 2;
            
            // Reset column if it goes off screen
            if (col.y > height) {
                col.y = -100;
                col.chars = this.getRandomCharSequence(20);
            }
        });
        
        this.ctx.shadowColor = 'transparent';
    }
    
    drawFeedbackOverlay() {
        if (!this.activeFeedback) return;
        
        const width = this.canvas.width / window.devicePixelRatio;
        const height = this.canvas.height / window.devicePixelRatio;
        
        // Calculate position (HUD-style, bottom-right)
        const x = width - 300;
        const y = height - 100;
        
        // Draw HUD box
        this.ctx.strokeStyle = `hsla(${this.getFeedbackHue()}, 100%, 50%, 0.8)`;
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x - 10, y - 10, 280, 60);
        
        // Draw corner accents
        this.ctx.fillStyle = `hsla(${this.getFeedbackHue()}, 100%, 50%, 0.8)`;
        this.ctx.fillRect(x - 10, y - 10, 20, 3);
        this.ctx.fillRect(x - 10, y - 10, 3, 20);
        this.ctx.fillRect(x + 270, y - 10, 20, 3);
        this.ctx.fillRect(x + 267, y - 10, 3, 20);
        
        // Draw text
        this.ctx.fillStyle = `hsla(${this.getFeedbackHue()}, 100%, 70%, 1)`;
        this.ctx.font = 'bold 14px "JetBrains Mono", monospace';
        this.ctx.fillText(this.activeFeedback.message, x + 5, y + 15);
        
        // Draw icon based on type
        const icon = this.activeFeedback.type === 'warning' ? '⚠' : this.activeFeedback.type === 'success' ? '✓' : 'ℹ';
        this.ctx.fillStyle = `hsla(${this.getFeedbackHue()}, 100%, 50%, 0.8)`;
        this.ctx.font = 'bold 16px "JetBrains Mono", monospace';
        this.ctx.fillText(icon, x + 250, y + 15);
    }
    
    getFeedbackHue() {
        if (!this.activeFeedback) return 120;
        switch (this.activeFeedback.type) {
            case 'success': return 120; // Green
            case 'warning': return 60; // Yellow
            case 'error': return 0; // Red
            default: return 180; // Cyan
        }
    }
    
    updateFPS() {
        const now = Date.now();
        const delta = now - this.lastTime;
        
        if (delta > 1000) {
            this.fps = this.frameCount;
            this.frameCount = 0;
            this.lastTime = now;
        }
        this.frameCount++;
    }
    
    setSpeed(speed) {
        this.config.speed = speed;
        this.initColumns();
    }
    
    setOpacity(opacity) {
        this.config.opacity = Math.max(0, Math.min(1, opacity));
        this.initColumns();
    }
    
    destroy() {
        this.stop();
        if (this.feedbackTimeout) clearTimeout(this.feedbackTimeout);
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EliteAnimationEngine;
}
