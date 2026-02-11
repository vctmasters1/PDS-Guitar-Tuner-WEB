/**
 * Guitar Tuner - Main Application
 * Entry point and initialization
 */

/**
 * Initialize the application when page loads
 */
function initApp() {
    calculateFrequencies();
    initUI();
}

// Run initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
