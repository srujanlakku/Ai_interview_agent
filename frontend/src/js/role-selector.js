/**
 * Role Selection Module
 * Allows users to select which role to interview for
 * Features:
 * - View roles available for selected company
 * - Filter by level (Junior, Mid, Senior)
 * - See role descriptions and requirements
 * - Select role for interview
 */

class RoleSelector {
    constructor(apiClient, company, containerId = 'role-selector') {
        this.apiClient = apiClient;
        this.company = company;
        this.container = document.getElementById(containerId);
        this.roles = [];
        this.selectedRole = null;
        this.selectedLevel = 'all';
        this.init();
    }

    async init() {
        try {
            await this.loadCompanyRoles();
            this.render();
        } catch (error) {
            console.error('Error initializing role selector:', error);
            this.showError('Failed to load roles');
        }
    }

    async loadCompanyRoles() {
        try {
            const response = await this.apiClient.get(
                `/api/interview/companies/${this.company.id}/roles`
            );
            // Backend returns { success: true, company_id: ..., company_name: ..., roles: [...] }
            this.roles = response.roles || [];
            console.log(`Loaded ${this.roles.length} roles for ${this.company.name}`);
        } catch (error) {
            console.error('Error loading roles:', error);
            throw error;
        }
    }

    getLevelColor(level) {
        const colors = {
            'junior': '#4CAF50',         // Green
            'mid': '#FFC107',             // Amber
            'senior': '#FF6F00',          // Orange
            'lead': '#9C27B0',            // Purple
            'staff': '#E91E63'            // Pink
        };
        return colors[level?.toLowerCase()] || '#2196F3';
    }

    getRoleIcon(roleName) {
        const icons = {
            'software': '💻',
            'backend': '🔧',
            'frontend': '🎨',
            'full stack': '⚙️',
            'data': '📊',
            'ai': '🤖',
            'devops': '🔌',
            'qa': '✅',
            'design': '🎭',
            'product': '📦',
            'manager': '👔'
        };

        for (const [key, icon] of Object.entries(icons)) {
            if (roleName.toLowerCase().includes(key)) {
                return icon;
            }
        }
        return '💼';
    }

    filterRoles() {
        if (this.selectedLevel === 'all') {
            return this.roles;
        }
        return this.roles.filter(r =>
            r.level && r.level.toLowerCase() === this.selectedLevel.toLowerCase()
        );
    }

    render() {
        if (!this.container) return;

        const filtered = this.filterRoles();

        this.container.innerHTML = `
            <div class="role-selector-wrapper">
                <div class="role-selector-header">
                    <div class="back-button" onclick="window.history.back()">← Back</div>
                    <div class="header-content">
                        <h2>🎯 Select Role for ${this.company.name}</h2>
                        <p class="header-subtitle">Choose your target position</p>
                    </div>
                </div>

                <div class="role-filter-tabs">
                    ${this.renderLevelTabs()}
                </div>

                <div class="role-grid">
                    ${this.renderRoleCards(filtered)}
                </div>

                <div class="role-stats">
                    <div class="stat">
                        <span class="stat-label">Total Roles:</span>
                        <span class="stat-value">${this.roles.length}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Showing:</span>
                        <span class="stat-value">${filtered.length}</span>
                    </div>
                </div>
            </div>
        `;

        this.attachEventListeners();
    }

    renderLevelTabs() {
        const levels = [
            { id: 'all', label: '📋 All Levels' },
            { id: 'junior', label: '🌱 Junior' },
            { id: 'mid', label: '📈 Mid-Level' },
            { id: 'senior', label: '⭐ Senior' },
            { id: 'lead', label: '👑 Lead' }
        ];

        return levels.map(level => `
            <button class="level-tab ${this.selectedLevel === level.id ? 'active' : ''}"
                    data-level="${level.id}">
                ${level.label}
            </button>
        `).join('');
    }

    renderRoleCards(roles) {
        return roles.map(role => `
            <div class="role-card" data-role-id="${role.id}"
                 style="border-left-color: ${this.getLevelColor(role.level)}">
                <div class="role-card-header">
                    <h3>${this.getRoleIcon(role.name)} ${role.name}</h3>
                    <span class="role-level-badge" style="background-color: ${this.getLevelColor(role.level)}">
                        ${role.level || 'Standard'}
                    </span>
                </div>

                <div class="role-card-body">
                    <p class="role-description">${role.description || 'Build amazing products'}</p>
                    <div class="role-details">
                        <div class="detail-item">
                            <span class="detail-icon">🎯</span>
                            <span class="detail-text">Practice common interview questions</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-icon">📊</span>
                            <span class="detail-text">Track your progress</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-icon">🔄</span>
                            <span class="detail-text">Get AI feedback on answers</span>
                        </div>
                    </div>
                </div>

                <button class="btn-select-role" data-role-id="${role.id}">
                    Select This Role →
                </button>
            </div>
        `).join('');
    }

    attachEventListeners() {
        // Level tab listeners
        document.querySelectorAll('.level-tab').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.level-tab').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.selectedLevel = e.target.dataset.level;
                this.render();
            });
        });

        // Role selection listeners
        document.querySelectorAll('.btn-select-role').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const roleId = e.target.dataset.roleId;
                await this.selectRole(roleId);
            });
        });
    }

    async selectRole(roleId) {
        try {
            const role = this.roles.find(r => r.id === roleId);
            if (!role) {
                throw new Error('Role not found');
            }

            this.selectedRole = role;

            // Save to session storage
            const interviewContext = {
                company: this.company,
                role: role,
                selectedAt: new Date().toISOString()
            };
            sessionStorage.setItem('interviewContext', JSON.stringify(interviewContext));

            // Visual feedback
            this.showSuccess(`Selected ${role.name} ✓`);

            // Notify listeners
            this.notifySelection(role);

            // Navigate to interview
            setTimeout(() => {
                window.dispatchEvent(new CustomEvent('role-selected', { detail: role }));
            }, 500);

        } catch (error) {
            console.error('Error selecting role:', error);
            this.showError('Failed to select role');
        }
    }

    notifySelection(role) {
        const event = new CustomEvent('roleSelected', {
            detail: {
                roleId: role.id,
                roleName: role.name,
                roleLevel: role.level,
                company: this.company
            }
        });
        document.dispatchEvent(event);
    }

    showError(message) {
        const notification = document.createElement('div');
        notification.className = 'notification error-notification';
        notification.textContent = `❌ ${message}`;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }

    showSuccess(message) {
        const notification = document.createElement('div');
        notification.className = 'notification success-notification';
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 2000);
    }

    getSelectedRole() {
        return this.selectedRole;
    }

    async getCompanyRoleQuestions(roundId = null) {
        try {
            let url = `/api/interview/questions/company/${this.company.id}/role/${this.selectedRole.id}`;
            if (roundId) {
                url += `?round_id=${roundId}`;
            }
            const response = await this.apiClient.get(url);
            // Backend returns { success: true, ..., questions: [...] }
            return response.questions || [];
        } catch (error) {
            console.error('Error loading questions:', error);
            return [];
        }
    }
}

// Export for use in main.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RoleSelector;
}
