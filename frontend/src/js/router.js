/**
 * Router
 * Single-page application routing system
 */

class Router {
    constructor() {
        this.routes = {};
        this.currentPage = null;
        this.appContainer = document.getElementById('app');
    }

    /**
     * Register a route
     */
    register(path, component, requiresAuth = false) {
        this.routes[path] = { component, requiresAuth };
    }

    /**
     * Navigate to a page
     */
    async navigate(path, params = {}) {
        let route = this.routes[path];
        let matchedParams = { ...params };

        // Support for parameterized routes (e.g., /review/:id)
        if (!route) {
            for (const routePath in this.routes) {
                if (routePath.includes(':')) {
                    const regexPath = routePath.replace(/:[^\s/]+/g, '([^\\/]+)');
                    const match = path.match(new RegExp(`^${regexPath}$`));
                    if (match) {
                        route = this.routes[routePath];
                        const paramNames = routePath.match(/:[^\s/]+/g);
                        paramNames.forEach((name, index) => {
                            matchedParams[name.substring(1)] = match[index + 1];
                        });
                        break;
                    }
                }
            }
        }

        // Check if route exists
        if (!route) {
            console.error('Route not found:', path);
            this.goTo('/login');
            return;
        }

        // Check authentication requirement
        if (route.requiresAuth && !auth.isLoggedIn()) {
            this.goTo('/login');
            return;
        }

        // Skip auth pages if already logged in
        if (!route.requiresAuth && (path === '/login' || path === '/signup') && auth.isLoggedIn()) {
            this.goTo('/dashboard');
            return;
        }

        // Clear container
        this.appContainer.innerHTML = '';

        // Render page
        const content = typeof route.component === 'function' ? route.component(matchedParams) : route.component;
        this.appContainer.innerHTML = content;

        // Re-attach event listeners and initialize components
        this.initializePageComponents();

        // Load interview review if on review page
        // (Matched params already contain 'id' if route was /review/:id)
        if (path.startsWith('/review/') && matchedParams.id) {
            setTimeout(() => {
                if (typeof loadInterviewReview === 'function') {
                    loadInterviewReview(matchedParams.id);
                }
            }, 100);
        }

        this.currentPage = path;
    }

    /**
     * Go to page (with history)
     */
    goTo(path, params = {}) {
        window.history.pushState({ path, params }, '', path);
        this.navigate(path, params);
    }

    /**
     * Initialize page-specific components
     */
    initializePageComponents() {
        // Re-attach event listeners for the new page
        if (typeof attachEventListeners === 'function') {
            attachEventListeners();
        }

        const path = window.location.pathname;
        if (path === '/dashboard/resume' && typeof initResumeAnalyzer === 'function') {
            initResumeAnalyzer();
        } else if (path === '/dashboard/sure-questions' && typeof initSureQuestions === 'function') {
            initSureQuestions();
        } else if (path === '/practice' && typeof initPracticeMode === 'function') {
            initPracticeMode();
        }
    }

    /**
     * Setup URL change listeners
     */
    setupListeners() {
        window.addEventListener('popstate', (e) => {
            const state = e.state || {};
            this.navigate(state.path || '/login', state.params || {});
        });
    }
}

// Create global router instance
window.router = new Router();

// Do NOT initialize router here - let main.js handle it after routes are registered

