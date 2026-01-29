/**
 * Authentication Module
 * User authentication state management
 */

class Auth {
    constructor() {
        this.user = null;
        this.token = localStorage.getItem('accessToken');
        this.loadUser();
    }

    /**
     * Load user from localStorage
     */
    loadUser() {
        const userData = localStorage.getItem('user');
        if (userData) {
            try {
                this.user = JSON.parse(userData);
            } catch (e) {
                this.clearAuth();
            }
        }
    }

    /**
     * Check if user is logged in
     */
    isLoggedIn() {
        return !!(this.token && this.user);
    }

    /**
     * Get current user
     */
    getCurrentUser() {
        return this.user;
    }

    /**
     * Sign up
     */
    async signup(email, password, full_name = '') {
        try {
            const response = await window.api.signup(email, password, full_name);
            // Signup returns user directly, not with token
            if (response && response.id) {
                // After signup, need to login
                const loginResult = await this.login(email, password);
                return loginResult;
            }
            return { success: false, error: 'Signup failed' };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Login
     */
    async login(email, password) {
        try {
            const response = await window.api.login(email, password);
            // Set token first
            window.api.setToken(response.access_token);
            this.token = response.access_token;
            localStorage.setItem('accessToken', response.access_token);

            // Fetch user data using the token
            const user = await window.api.getCurrentUser();
            this.user = user;
            localStorage.setItem('user', JSON.stringify(user));

            return { success: true, user: user };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    /**
     * Logout
     */
    async logout() {
        try {
            await window.api.logout();
        } catch (e) {
            // Ignore error
        }
        this.clearAuth();
    }

    /**
     * Set authentication state
     */
    setAuth(token, user) {
        this.token = token;
        this.user = user;
        window.api.setToken(token);
        localStorage.setItem('accessToken', token);
        localStorage.setItem('user', JSON.stringify(user));
    }

    /**
     * Clear authentication state
     */
    clearAuth() {
        this.token = null;
        this.user = null;
        window.api.removeToken();
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
    }

    /**
     * Get user email
     */
    getEmail() {
        return this.user?.email || '';
    }

    /**
     * Get user name
     */
    getName() {
        return this.user?.name || this.user?.email?.split('@')[0] || 'User';
    }

    /**
     * Get user initials
     */
    getInitials() {
        const name = this.getName();
        return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    }
}

// Create global auth instance
window.auth = new Auth();
