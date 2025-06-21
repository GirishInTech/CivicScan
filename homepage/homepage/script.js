// DOM Elements
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');
const reportModal = document.getElementById('reportModal');
const reportForm = document.getElementById('reportForm');
const languageSelect = document.getElementById('languageSelect');

// Navigation functionality
hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

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

// Navbar scroll effect
function handleNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
}

// Modal functionality
function openReportModal() {
    reportModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeReportModal() {
    reportModal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Event listeners for modal
document.querySelectorAll('button:contains("Report Issue"), button:contains("Start Reporting")').forEach(button => {
    if (button.textContent.includes('Report') || button.textContent.includes('Start Reporting')) {
        button.addEventListener('click', openReportModal);
    }
});

// Close modal when clicking the X or outside
document.querySelector('.close').addEventListener('click', closeReportModal);

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

// Form submission
reportForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(reportForm);
    const issueType = formData.get('issueType') || document.getElementById('issueType').value;
    const location = formData.get('location') || document.getElementById('location').value;
    const description = formData.get('description') || document.getElementById('description').value;
    const photo = document.getElementById('photo').files[0];
    
    // Simulate form submission
    showNotification('Report submitted successfully! Thank you for helping make Bengaluru better.', 'success');
    
    // Reset form and close modal
    reportForm.reset();
    closeReportModal();
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
languageSelect.addEventListener('change', (e) => {
    const selectedLanguage = e.target.value;
    switchLanguage(selectedLanguage);
    showNotification(`Language switched to ${getLanguageName(selectedLanguage)}`, 'info');
});

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

// Parallax effect for hero section
function handleParallax() {
    const hero = document.querySelector('.hero');
    const scrolled = window.pageYOffset;
    const rate = scrolled * -0.5;
    
    if (hero) {
        hero.style.transform = `translateY(${rate}px)`;
    }
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

// Event listeners
window.addEventListener('scroll', () => {
    updateActiveNavLink();
    handleNavbarScroll();
    handleParallax();
});

window.addEventListener('resize', () => {
    // Close mobile menu on resize
    if (window.innerWidth > 768) {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    }
});

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    setupScrollAnimations();
    setupCounterAnimation();
    
    // Add click handlers for all report buttons
    document.addEventListener('click', (e) => {
        const target = e.target.closest('button');
        if (target && (target.textContent.includes('Report') || target.textContent.includes('Start Reporting'))) {
            openReportModal();
        }
    });
    
    console.log('BrillianBengaluru website initialized successfully!');
});

// Service Worker registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Add utility functions
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
    
    // Format numbers
    formatNumber: (num) => {
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }
};

// Export utils for potential use in other scripts
window.BrillianBengaluruUtils = utils;