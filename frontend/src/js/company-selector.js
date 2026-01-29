/**
 * Company Selection Module
 * Allows users to select which MNC to interview with
 * Features:
 * - Browse 25+ Indian MNCs
 * - Filter by company type (Big Tech, IT Services, Startups, etc.)
 * - View company details and roles
 * - Select company for interview
 */

class CompanySelector {
    constructor(apiClient, containerId = 'company-selector') {
        this.apiClient = apiClient;
        this.container = document.getElementById(containerId);
        this.companies = [];
        this.selectedCompany = null;
        this.selectedFilter = 'all';
        this.init();
    }

    async init() {
        try {
            await this.loadCompanies();
            this.render();
        } catch (error) {
            console.error('Error initializing company selector:', error);
            this.showError('Failed to load companies');
        }
    }

    async loadCompanies() {
        try {
            const response = await this.apiClient.get('/api/interview/companies');
            // Backend returns { success: true, companies: [...] }
            this.companies = response.companies || [];
            console.log(`Loaded ${this.companies.length} companies`);
        } catch (error) {
            console.error('Error loading companies:', error);
            throw error;
        }
    }

    getCompanyTypeColor(companyType) {
        const colors = {
            'mnc': '#00D9FF',           // Cyan
            'indian_it': '#00FF88',      // Green
            'startup': '#FF00FF',        // Magenta
            'consulting': '#FFD700',     // Gold
            'fintech': '#FF4444'         // Red
        };
        return colors[companyType] || '#00D9FF';
    }

    getIndustryIcon(industryType) {
        const icons = {
            'tech': '💻',
            'it_services': '🏢',
            'startup': '🚀',
            'consulting': '📊',
            'fintech': '💰',
            'hardware': '🖥️'
        };
        return icons[industryType] || '🏢';
    }

    filterCompanies() {
        if (this.selectedFilter === 'all') {
            return this.companies;
        }
        return this.companies.filter(c => c.company_type === this.selectedFilter);
    }

    render() {
        if (!this.container) return;

        const filtered = this.filterCompanies();

        this.container.innerHTML = `
            <div class="company-selector-wrapper">
                <div class="company-selector-header">
                    <h2>🎯 Select Company for Interview</h2>
                    <p>Choose from 25+ Indian MNCs and tech companies</p>
                </div>

                <div class="company-filter-tabs">
                    ${this.renderFilterTabs()}
                </div>

                <div class="company-grid">
                    ${this.renderCompanyCards(filtered)}
                </div>

                <div class="company-stats">
                    <div class="stat">
                        <span class="stat-label">Total Companies:</span>
                        <span class="stat-value">${this.companies.length}</span>
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

    renderFilterTabs() {
        const filters = [
            { id: 'all', label: '📊 All' },
            { id: 'mnc', label: '🌍 Big Tech' },
            { id: 'indian_it', label: '🏢 Indian IT' },
            { id: 'startup', label: '🚀 Startups' },
            { id: 'consulting', label: '📋 Consulting' },
            { id: 'fintech', label: '💳 FinTech' }
        ];

        return filters.map(filter => `
            <button class="filter-tab ${this.selectedFilter === filter.id ? 'active' : ''}"
                    data-filter="${filter.id}">
                ${filter.label}
            </button>
        `).join('');
    }

    renderCompanyCards(companies) {
        return companies.map(company => `
            <div class="company-card" data-company-id="${company.id}" 
                 style="border-color: ${this.getCompanyTypeColor(company.company_type)}">
                <div class="company-card-header">
                    <h3>${this.getIndustryIcon(company.industry_type)} ${company.name}</h3>
                    <span class="company-type-badge">${this.formatCompanyType(company.company_type)}</span>
                </div>
                
                <div class="company-card-body">
                    <p class="company-description">${company.description || 'Leading tech company'}</p>
                    <div class="company-meta">
                        <div class="meta-item">
                            <span class="meta-label">HQ:</span>
                            <span class="meta-value">${company.headquarters || 'Global'}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Offices in India:</span>
                            <span class="meta-value">${company.india_office_locations || 'Multiple'}</span>
                        </div>
                    </div>
                </div>

                <button class="btn-select-company" data-company-id="${company.id}">
                    Select & Continue →
                </button>
            </div>
        `).join('');
    }

    formatCompanyType(type) {
        return type.split('_').map(word =>
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    attachEventListeners() {
        // Filter tab listeners
        document.querySelectorAll('.filter-tab').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-tab').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.selectedFilter = e.target.dataset.filter;
                this.render();
            });
        });

        // Company selection listeners
        document.querySelectorAll('.btn-select-company').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const companyId = e.target.dataset.companyId;
                await this.selectCompany(companyId);
            });
        });
    }

    async selectCompany(companyId) {
        try {
            const company = this.companies.find(c => c.id === companyId);
            if (!company) {
                throw new Error('Company not found');
            }

            this.selectedCompany = company;

            // Save to session storage
            sessionStorage.setItem('selectedCompany', JSON.stringify(company));

            // Notify listeners
            this.notifySelection(company);

            // Visual feedback
            this.showSuccess(`Selected ${company.name} ✓`);

            // Navigate to role selector
            setTimeout(() => {
                window.dispatchEvent(new CustomEvent('company-selected', { detail: company }));
            }, 500);

        } catch (error) {
            console.error('Error selecting company:', error);
            this.showError('Failed to select company');
        }
    }

    notifySelection(company) {
        const event = new CustomEvent('companySelected', {
            detail: {
                companyId: company.id,
                companyName: company.name,
                companyType: company.company_type
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

    getSelectedCompany() {
        return this.selectedCompany;
    }

    async getCompanyRoles(companyId) {
        try {
            const roles = await this.apiClient.get(`/api/interview/companies/${companyId}/roles`);
            return roles || [];
        } catch (error) {
            console.error('Error loading company roles:', error);
            return [];
        }
    }
}

// Export for use in main.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CompanySelector;
}
