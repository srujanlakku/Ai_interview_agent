/**
 * Readiness Speedometer Component
 * Circular gauge inspired by supercars
 */

class ReadinessSpeedometer {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) throw new Error(`Container with ID "${containerId}" not found`);
        
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        
        this.width = options.width || 300;
        this.height = options.height || 300;
        this.radius = Math.min(this.width, this.height) / 2 - 20;
        this.centerX = this.width / 2;
        this.centerY = this.height / 2;
        
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        this.container.appendChild(this.canvas);
        
        this.readiness = 0; // 0 to 100
        this.animatedReadiness = 0;
        this.animationId = null;
        this.isAnimating = false;
        
        this.draw();
    }
    
    setReadiness(value) {
        this.readiness = Math.max(0, Math.min(100, value));
        if (!this.isAnimating) {
            this.startAnimation();
        }
    }
    
    startAnimation() {
        this.isAnimating = true;
        const animate = () => {
            // Smooth animation to target readiness
            this.animatedReadiness += (this.readiness - this.animatedReadiness) * 0.05;
            
            this.draw();
            
            if (Math.abs(this.readiness - this.animatedReadiness) > 0.5) {
                this.animationId = requestAnimationFrame(animate);
            } else {
                this.isAnimating = false;
                this.animatedReadiness = this.readiness;
                this.draw();
            }
        };
        animate();
    }
    
    draw() {
        // Clear canvas
        this.ctx.fillStyle = 'rgba(10, 14, 39, 0)';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Draw outer circle border
        this.drawOuterBorder();
        
        // Draw gauge background
        this.drawGaugeBackground();
        
        // Draw colored zones
        this.drawZones();
        
        // Draw needle
        this.drawNeedle();
        
        // Draw center circle
        this.drawCenter();
        
        // Draw labels and values
        this.drawLabels();
        
        // Draw glow effect
        this.drawGlow();
    }
    
    drawOuterBorder() {
        this.ctx.strokeStyle = 'rgba(0, 255, 65, 0.6)';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.arc(this.centerX, this.centerY, this.radius + 10, 0, Math.PI * 2);
        this.ctx.stroke();
    }
    
    drawGaugeBackground() {
        this.ctx.fillStyle = 'rgba(10, 14, 39, 0.8)';
        this.ctx.beginPath();
        this.ctx.arc(this.centerX, this.centerY, this.radius, 0, Math.PI * 2);
        this.ctx.fill();
    }
    
    drawZones() {
        const startAngle = Math.PI * 0.75;
        const endAngle = Math.PI * 0.25;
        const angleRange = endAngle > startAngle ? endAngle - startAngle : (Math.PI * 2 - startAngle) + endAngle;
        
        // Red zone (0-33)
        this.drawZone(startAngle, startAngle + angleRange * 0.33, '#ff3333', 'hsla(0, 100%, 50%, 0.3)');
        
        // Yellow zone (33-66)
        this.drawZone(startAngle + angleRange * 0.33, startAngle + angleRange * 0.66, '#ffff00', 'hsla(60, 100%, 50%, 0.3)');
        
        // Green zone (66-100)
        this.drawZone(startAngle + angleRange * 0.66, startAngle + angleRange, '#00ff41', 'hsla(120, 100%, 50%, 0.3)');
    }
    
    drawZone(startAngle, endAngle, color, glowColor) {
        // Draw zone arc
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 8;
        this.ctx.beginPath();
        this.ctx.arc(this.centerX, this.centerY, this.radius - 15, startAngle, endAngle);
        this.ctx.stroke();
        
        // Draw zone fill
        this.ctx.fillStyle = glowColor;
        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX, this.centerY);
        this.ctx.arc(this.centerX, this.centerY, this.radius - 15, startAngle, endAngle);
        this.ctx.lineTo(this.centerX, this.centerY);
        this.ctx.fill();
    }
    
    drawNeedle() {
        const startAngle = Math.PI * 0.75;
        const endAngle = Math.PI * 0.25;
        const angleRange = endAngle > startAngle ? endAngle - startAngle : (Math.PI * 2 - startAngle) + endAngle;
        
        const needleAngle = startAngle + angleRange * (this.animatedReadiness / 100);
        
        // Determine needle color based on readiness
        let needleColor;
        if (this.animatedReadiness < 33) {
            needleColor = '#ff3333';
        } else if (this.animatedReadiness < 66) {
            needleColor = '#ffff00';
        } else {
            needleColor = '#00ff41';
        }
        
        // Draw needle shadow
        this.ctx.strokeStyle = 'rgba(0, 0, 0, 0.5)';
        this.ctx.lineWidth = 6;
        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX, this.centerY);
        this.ctx.lineTo(
            this.centerX + Math.cos(needleAngle) * (this.radius - 30),
            this.centerY + Math.sin(needleAngle) * (this.radius - 30)
        );
        this.ctx.stroke();
        
        // Draw needle
        this.ctx.strokeStyle = needleColor;
        this.ctx.lineWidth = 4;
        this.ctx.lineCap = 'round';
        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX, this.centerY);
        this.ctx.lineTo(
            this.centerX + Math.cos(needleAngle) * (this.radius - 30),
            this.centerY + Math.sin(needleAngle) * (this.radius - 30)
        );
        this.ctx.stroke();
        
        // Draw needle glow
        this.ctx.strokeStyle = `rgba(${this.getRGBFromColor(needleColor)}, 0.6)`;
        this.ctx.shadowColor = needleColor;
        this.ctx.shadowBlur = 15;
        this.ctx.lineWidth = 6;
        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX, this.centerY);
        this.ctx.lineTo(
            this.centerX + Math.cos(needleAngle) * (this.radius - 30),
            this.centerY + Math.sin(needleAngle) * (this.radius - 30)
        );
        this.ctx.stroke();
        this.ctx.shadowColor = 'transparent';
    }
    
    getRGBFromColor(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : '0, 0, 0';
    }
    
    drawCenter() {
        // Inner circle
        this.ctx.fillStyle = 'rgba(0, 255, 65, 0.9)';
        this.ctx.beginPath();
        this.ctx.arc(this.centerX, this.centerY, 10, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Center dot
        this.ctx.fillStyle = '#00ff41';
        this.ctx.shadowColor = '#00ff41';
        this.ctx.shadowBlur = 15;
        this.ctx.beginPath();
        this.ctx.arc(this.centerX, this.centerY, 6, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.shadowColor = 'transparent';
    }
    
    drawLabels() {
        // Draw readiness percentage
        this.ctx.fillStyle = '#00ff41';
        this.ctx.font = 'bold 36px "JetBrains Mono", monospace';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(Math.round(this.animatedReadiness), this.centerX, this.centerY - 20);
        
        // Draw percentage sign
        this.ctx.font = 'bold 20px "JetBrains Mono", monospace';
        this.ctx.fillText('%', this.centerX + 40, this.centerY - 20);
        
        // Draw status text
        this.ctx.font = 'bold 12px "JetBrains Mono", monospace';
        this.ctx.fillText(this.getStatusText(), this.centerX, this.centerY + 30);
        
        // Draw zone labels
        this.ctx.font = '10px "JetBrains Mono", monospace';
        
        // Red zone label
        this.ctx.fillStyle = '#ff3333';
        this.ctx.fillText('NOT READY', this.centerX - 60, this.centerY - 60);
        
        // Yellow zone label
        this.ctx.fillStyle = '#ffff00';
        this.ctx.fillText('ALMOST READY', this.centerX, this.centerY - 85);
        
        // Green zone label
        this.ctx.fillStyle = '#00ff41';
        this.ctx.fillText('INTERVIEW READY', this.centerX + 60, this.centerY - 60);
    }
    
    getStatusText() {
        if (this.animatedReadiness < 33) return 'Keep practicing';
        if (this.animatedReadiness < 66) return 'Almost there';
        return 'Ready to interview!';
    }
    
    drawGlow() {
        const glowIntensity = this.animatedReadiness / 100;
        this.ctx.strokeStyle = `rgba(0, 255, 65, ${glowIntensity * 0.3})`;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(this.centerX, this.centerY, this.radius + 15, 0, Math.PI * 2);
        this.ctx.stroke();
    }
    
    destroy() {
        if (this.animationId) cancelAnimationFrame(this.animationId);
        this.canvas.remove();
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReadinessSpeedometer;
}
