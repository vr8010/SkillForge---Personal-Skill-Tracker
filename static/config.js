// API Configuration
// Update this with your Render backend URL after deployment
const API_CONFIG = {
    // For local development
    local: 'http://localhost:5000/api',
    
    // For production (update with your Render URL)
    production: 'https://skillforge-personal-skill-tracker.onrender.com/api',
    
    // Auto-detect environment
    getBaseURL: function() {
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return this.local;
        }
        return this.production;
    }
};

// Export for use in app.js
window.API_CONFIG = API_CONFIG;
