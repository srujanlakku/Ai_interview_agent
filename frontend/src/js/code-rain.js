/**
 * Code Rain Animation
 * Matrix-style falling characters with Canvas 2D API
 */

class CodeRain {
    constructor(canvasId = 'codeRainCanvas') {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        
        // Set canvas size
        this.resizeCanvas();
        
        // Characters to rain
        this.characters = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン":<>[]{}()|!@#$%^&*';
        
        // Columns array (each column stores y position of falling characters)
        this.columns = [];
        
        // Settings
        this.fontSize = 16;
        this.speed = 1.5;
        this.opacity = 0.5;
        
        // Initialize columns
        this.initColumns();
        
        // Animation state
        this.animationId = null;
        this.isRunning = false;
        
        // Listen for window resize
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    /**
     * Resize canvas to match window size
     */
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.initColumns();
    }

    /**
     * Initialize columns array based on canvas width
     */
    initColumns() {
        const columnCount = Math.ceil(this.canvas.width / this.fontSize);
        this.columns = new Array(columnCount).fill(0);
    }

    /**
     * Get random character from the character set
     */
    getRandomChar() {
        return this.characters.charAt(Math.floor(Math.random() * this.characters.length));
    }

    /**
     * Draw a single frame of the animation
     */
    draw() {
        // Semi-transparent background for trail effect
        this.ctx.fillStyle = `rgba(5, 8, 18, 0.1)`;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Set text properties
        this.ctx.font = `bold ${this.fontSize}px 'JetBrains Mono'`;
        this.ctx.textBaseline = 'top';

        // Draw each column
        for (let i = 0; i < this.columns.length; i++) {
            const x = i * this.fontSize;
            const y = this.columns[i] * this.fontSize;

            // Random character
            const char = this.getRandomChar();

            // Create gradient for character - bright at top, fading at bottom
            const alpha = Math.max(0, Math.min(1, 1 - (this.columns[i] * 0.02)));
            
            // Color alternation for visual interest
            if (Math.random() > 0.95) {
                // Cyan color (accent)
                this.ctx.fillStyle = `rgba(0, 212, 255, ${alpha * 0.7})`;
            } else if (Math.random() > 0.98) {
                // Purple color
                this.ctx.fillStyle = `rgba(176, 0, 255, ${alpha * 0.5})`;
            } else {
                // Main green color
                this.ctx.fillStyle = `rgba(0, 255, 65, ${alpha * this.opacity})`;
            }

            this.ctx.fillText(char, x, y);

            // Update position for next frame
            this.columns[i]++;

            // Reset column if it goes off screen
            if (y > this.canvas.height && Math.random() > 0.98) {
                this.columns[i] = 0;
            }
        }
    }

    /**
     * Animation loop
     */
    animate() {
        this.draw();
        
        if (this.isRunning) {
            this.animationId = requestAnimationFrame(() => this.animate());
        }
    }

    /**
     * Start the animation
     */
    start() {
        if (!this.isRunning) {
            this.isRunning = true;
            this.animate();
        }
    }

    /**
     * Stop the animation
     */
    stop() {
        this.isRunning = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }

    /**
     * Change animation speed
     */
    setSpeed(speed) {
        this.speed = Math.max(0.5, Math.min(3, speed));
    }

    /**
     * Change opacity
     */
    setOpacity(opacity) {
        this.opacity = Math.max(0, Math.min(1, opacity));
    }
}

// Initialize code rain on page load
document.addEventListener('DOMContentLoaded', () => {
    const codeRain = new CodeRain();
    codeRain.start();

    // Store instance globally for access
    window.codeRain = codeRain;
});
