// ===== MODERN DOM ELEMENTS =====
let navToggle, navMenu, reportModal, reportForm, languageSelect, navbar;

// Wait for DOM to be ready before getting elements
document.addEventListener('DOMContentLoaded', function() {
    navToggle = document.getElementById('navToggle');
    navMenu = document.getElementById('navMenu');
    reportModal = document.getElementById('reportModal');
    reportForm = document.getElementById('reportForm');
    languageSelect = document.getElementById('languageSelect');
    navbar = document.querySelector('.navbar');
    
    console.log('DOM Elements loaded:', {
        navToggle: !!navToggle,
        navMenu: !!navMenu,
        reportModal: !!reportModal,
        reportForm: !!reportForm,
        languageSelect: !!languageSelect,
        navbar: !!navbar
    });
});

// ===== MODERN NAVIGATION FUNCTIONALITY =====
document.addEventListener('DOMContentLoaded', function () {
    // Initialize after DOM elements are loaded
    setTimeout(() => {
        initializeNavigation();
        initializeScrollAnimations();
        initializeParallaxEffects();
        initializeCounterAnimations();
        initializeModalFunctionality();
        initializeFormHandlers();
        
        console.log('🚀 BrillianBengaluru - Modern UI initialized successfully!');
    }, 100);
});

function initializeNavigation() {
    console.log('Initializing navigation...'); // Debug log
    console.log('navToggle:', navToggle); // Debug log
    console.log('navMenu:', navMenu); // Debug log
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Mobile menu toggle clicked'); // Debug log
            console.log('navToggle classes before:', navToggle.classList.toString()); // Debug log
            console.log('navMenu classes before:', navMenu.classList.toString()); // Debug log
            
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            console.log('navToggle classes after:', navToggle.classList.toString()); // Debug log
            console.log('navMenu classes after:', navMenu.classList.toString()); // Debug log
            
            document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
        });
    } else {
        console.error('Navigation elements not found!'); // Debug log
    }

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });

    // Fallback: Add click handler to document to close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (navMenu && navMenu.classList.contains('active') && 
            !navMenu.contains(e.target) && 
            !navToggle.contains(e.target)) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
            document.body.style.overflow = '';
        }
    });

    // Close mobile menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
            document.body.style.overflow = '';
        }
    });

    // Handle navbar scroll effect
    window.addEventListener('scroll', handleNavbarScroll);
}

// Mobile menu functionality is now handled in initializeNavigation()

// Smooth scrolling function
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Update active nav link on scroll
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let currentSection = '';
    
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= 100 && rect.bottom >= 100) {
            currentSection = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
}

// ===== MODERN SCROLL ANIMATIONS =====
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, observerOptions);
    
    // Add animation classes to elements
    const animateElements = document.querySelectorAll('.feature-card, .stat-card, .help-item, .insight-item, .section-header');
    animateElements.forEach((el, index) => {
        el.classList.add('animate-on-scroll');
        
        // Add staggered animation delays
        if (index % 2 === 0) {
            el.classList.add('animate-left');
        } else {
            el.classList.add('animate-right');
        }
        
        observer.observe(el);
    });
}

// ===== MODERN NAVBAR SCROLL EFFECT =====
function handleNavbarScroll() {
    if (!navbar) return;
    
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}

// ===== MODERN MODAL FUNCTIONALITY =====
function initializeModalFunctionality() {
    if (!reportModal) return;
    
    // Add click handlers for all report buttons
    document.addEventListener('click', (e) => {
        const target = e.target.closest('button');
        if (target && (target.textContent.includes('Report') || target.textContent.includes('Start Reporting'))) {
            openReportModal();
        }
    });
    
    // Close modal when clicking outside
    reportModal.addEventListener('click', (e) => {
        if (e.target === reportModal) {
            closeReportModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && reportModal.style.display === 'block') {
            closeReportModal();
        }
    });
}

function openReportModal() {
    if (!reportModal) return;
    reportModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Add entrance animation
    setTimeout(() => {
        reportModal.style.opacity = '1';
        reportModal.querySelector('.modal-content').style.transform = 'translateY(0) scale(1)';
    }, 10);
}

function closeReportModal() {
    if (!reportModal) return;
    
    // Add exit animation
    reportModal.style.opacity = '0';
    reportModal.querySelector('.modal-content').style.transform = 'translateY(-50px) scale(0.9)';
    
    setTimeout(() => {
        reportModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }, 300);
}

// ===== MODERN FORM HANDLERS =====
function initializeFormHandlers() {
    if (!reportForm) return;
    
    reportForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(reportForm);
        const issueType = formData.get('issueType') || document.getElementById('issueType')?.value;
        const location = formData.get('location') || document.getElementById('location')?.value;
        const description = formData.get('description') || document.getElementById('description')?.value;
        const photo = document.getElementById('photo')?.files[0];
        
        // Show loading state
        const submitBtn = reportForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;
        
        // Simulate form submission with delay
        setTimeout(() => {
            showNotification('Report submitted successfully! Thank you for helping make Bengaluru better.', 'success');
            reportForm.reset();
            closeReportModal();
            
            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 1500);
    });
    
    // Close modal when clicking the X
    const closeBtn = document.querySelector('.close');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeReportModal);
    }
}

// ===== MODERN EVENT LISTENERS =====
window.addEventListener('scroll', () => {
    updateActiveNavLink();
    handleNavbarScroll();
});

window.addEventListener('resize', () => {
    // Close mobile menu on resize
    if (window.innerWidth > 768) {
        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
});

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 3000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 400px;
    `;
    
    notification.querySelector('.notification-content').style.cssText = `
        display: flex;
        align-items: center;
        gap: 0.75rem;
    `;
    
    notification.querySelector('.notification-close').style.cssText = `
        background: none;
        border: none;
        color: white;
        font-size: 1.25rem;
        cursor: pointer;
        margin-left: auto;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Close functionality
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => notification.remove(), 300);
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    return icons[type] || icons.info;
}

function getNotificationColor(type) {
    const colors = {
        success: 'linear-gradient(135deg, #10b981, #059669)',
        error: 'linear-gradient(135deg, #ef4444, #dc2626)',
        warning: 'linear-gradient(135deg, #f59e0b, #d97706)',
        info: 'linear-gradient(135deg, #3b82f6, #2563eb)'
    };
    return colors[type] || colors.info;
}

// Language switching
// const languageSelect = document.getElementById('languageSelect');
if (languageSelect) {
    languageSelect.addEventListener('change', (e) => {
        const selectedLanguage = e.target.value;
        switchLanguage(selectedLanguage);
        showNotification(`Language switched to ${getLanguageName(selectedLanguage)}`, 'info');
    });
}

// languageSelect.addEventListener('change', (e) => {
//     const selectedLanguage = e.target.value;
//     switchLanguage(selectedLanguage);
//     showNotification(`Language switched to ${getLanguageName(selectedLanguage)}`, 'info');
// });

function switchLanguage(language) {
    // This is a simplified language switching function
    // In a real application, you would have translation files
    const translations = {
        en: {
            title: 'BrillianBengaluru',
            subtitle: "Let's Build a Cleaner, Smarter City Together",
            reportIssue: 'Report Issue',
            learnMore: 'Learn More'
        },
        kn: {
            title: 'ಬ್ರಿಲಿಯನ್‌ಬೆಂಗಳೂರು',
            subtitle: 'ಒಂದು ಸ್ವಚ್ಛ, ಸ್ಮಾರ್ಟ್ ನಗರವನ್ನು ನಿರ್ಮಿಸೋಣ',
            reportIssue: 'ಸಮಸ್ಯೆಯನ್ನು ವರದಿ ಮಾಡಿ',
            learnMore: 'ಇನ್ನಷ್ಟು ತಿಳಿಯಿರಿ'
        },
        hi: {
            title: 'ब्रिलियनबेंगलुरु',
            subtitle: 'आइए मिलकर एक स्वच्छ, स्मार्ट शहर बनाएं',
            reportIssue: 'समस्या की रिपोर्ट करें',
            learnMore: 'और जानें'
        }
    };
    
    // Update text content based on selected language
    // This is a basic implementation - in production, you'd use a proper i18n library
    console.log(`Language switched to: ${language}`);
}

function getLanguageName(code) {
    const names = {
        en: 'English',
        kn: 'ಕನ್ನಡ',
        hi: 'हिंदी'
    };
    return names[code] || 'English';
}

// ===== MODERN PARALLAX EFFECTS =====
function initializeParallaxEffects() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.3;
        
        hero.style.transform = `translateY(${rate}px)`;
    });
}

// ===== MODERN COUNTER ANIMATIONS =====
function initializeCounterAnimations() {
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    const statsSection = document.querySelector('.problem-section');
    const insightsSection = document.querySelector('.insights-section');
    
    if (statsSection) observer.observe(statsSection);
    if (insightsSection) observer.observe(insightsSection);
}

// Intersection Observer for animations
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate in
    const animateElements = document.querySelectorAll('.feature-card, .stat-card, .help-item, .insight-item');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Counter animation for statistics
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number, .insight-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent.replace(/[^\d]/g, ''));
        const duration = 2000;
        const start = performance.now();
        
        function updateCounter(currentTime) {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.floor(progress * target);
            
            // Preserve original formatting (%, K, etc.)
            const originalText = counter.textContent;
            if (originalText.includes('%')) {
                counter.textContent = current + '%';
            } else if (originalText.includes('K')) {
                counter.textContent = (current / 1000).toFixed(1) + 'K';
            } else {
                counter.textContent = current;
            }
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        }
        
        requestAnimationFrame(updateCounter);
    });
}

// Initialize counter animation when section comes into view
function setupCounterAnimation() {
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    const statsSection = document.querySelector('.problem-section');
    const insightsSection = document.querySelector('.insights-section');
    
    if (statsSection) observer.observe(statsSection);
    if (insightsSection) observer.observe(insightsSection);
}

// ===== MODERN UTILITY FUNCTIONS =====
const utils = {
    // Debounce function for performance
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function for performance
    throttle: (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // Format numbers with animations
    formatNumber: (num) => {
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    },
    
    // Smooth scroll to element
    smoothScrollTo: (element, offset = 80) => {
        const targetPosition = element.offsetTop - offset;
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    },
    
    // Check if element is in viewport
    isInViewport: (element) => {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
};

// ===== PERFORMANCE OPTIMIZATIONS =====
// Use throttled scroll handlers for better performance
const throttledScrollHandler = utils.throttle(() => {
    updateActiveNavLink();
    handleNavbarScroll();
}, 16); // ~60fps

window.addEventListener('scroll', throttledScrollHandler);

// ===== ACCESSIBILITY IMPROVEMENTS =====
// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    // Tab navigation for mobile menu
    if (e.key === 'Tab' && navMenu && navMenu.classList.contains('active')) {
        const focusableElements = navMenu.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
        }
    }
});

console.log('🎨 Modern UI enhancements loaded successfully!');

// Test function to manually trigger mobile menu
window.testMobileMenu = function() {
    console.log('Testing mobile menu...');
    if (navToggle && navMenu) {
        navToggle.click();
        console.log('Mobile menu test completed');
    } else {
        console.error('Mobile menu elements not found for testing');
    }
};


