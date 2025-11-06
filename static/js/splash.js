// Splash Screen Handler
(function() {
    'use strict';
    
    // Configuration
    const SPLASH_DURATION = 1500; // milliseconds (1.5 seconds)
    const SHOW_ON_MOBILE_ONLY = true; // Set to false to show on all devices
    const SHOW_ONLY_ON_HOME = true; // Only show on home page
    
    // Check if splash should be shown
    function shouldShowSplash() {
        // Check if it's a mobile device
        const isMobile = window.innerWidth <= 768;
        
        // Check if splash was already shown in this session
        const splashShown = sessionStorage.getItem('splashShown');
        
        // Check if this is a page navigation (not initial load)
        const isPageNavigation = performance.navigation.type === 1 || // Reload
                                 performance.navigation.type === 2 || // Back/Forward
                                 window.performance.getEntriesByType('navigation')[0]?.type === 'navigate';
        
        // Only show on home page if configured
        if (SHOW_ONLY_ON_HOME) {
            const path = window.location.pathname;
            if (path !== '/' && path !== '/home/') {
                return false;
            }
        }
        
        if (SHOW_ON_MOBILE_ONLY && !isMobile) {
            return false;
        }
        
        // Show splash only once per session
        if (splashShown) {
            return false;
        }
        
        // Don't show on page refresh or back/forward navigation
        if (performance.navigation.type !== 0) {
            return false;
        }
        
        return true;
    }
    
    // Initialize splash screen
    function initSplash() {
        // Get splash element first
        const splash = document.getElementById('splashScreen');
        
        if (!splash) {
            return;
        }
        
        // Check if splash should be shown
        if (!shouldShowSplash()) {
            // Immediately hide splash if it shouldn't be shown
            splash.style.display = 'none';
            splash.remove(); // Remove from DOM to prevent any issues
            return;
        }
        
        // Add splash-active class to body
        document.body.classList.add('splash-active');
        
        // Mark splash as shown
        sessionStorage.setItem('splashShown', 'true');
        
        // Show splash with animation
        splash.classList.add('show');
        
        // Force reflow to ensure animation works
        splash.offsetHeight;
        
        // Hide splash after duration
        const hideTimer = setTimeout(function() {
            hideSplash();
        }, SPLASH_DURATION);
        
        // Also hide on tap/click
        splash.addEventListener('click', function() {
            clearTimeout(hideTimer);
            hideSplash();
        }, { once: true }); // Only trigger once
    }
    
    // Hide splash screen
    function hideSplash() {
        const splash = document.getElementById('splashScreen');
        
        if (!splash) {
            return;
        }
        
        // Prevent multiple calls
        if (splash.classList.contains('fade-out')) {
            return;
        }
        
        // Add fade-out class
        splash.classList.add('fade-out');
        
        // Remove splash-active from body
        document.body.classList.remove('splash-active');
        
        // Remove element after transition
        setTimeout(function() {
            splash.style.display = 'none';
            splash.remove(); // Completely remove from DOM
        }, 500);
    }
    
    // Check if page is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSplash);
    } else {
        initSplash();
    }
    
    // Expose function to manually show splash (for testing)
    window.showSplash = function() {
        sessionStorage.removeItem('splashShown');
        location.reload();
    };
    
})();
