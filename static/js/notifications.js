// Real-time notification system for CivicScan with WebSocket support
class NotificationSystem {
    constructor() {
        this.container = null;
        this.checkInterval = null;
        this.websocket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000; // Start with 1 second
        this.lastChecked = localStorage.getItem('lastNotificationCheck') || new Date().toISOString();
        this.isConnected = false;
        this.init();
    }

    init() {
        this.createContainer();
        
        // Try WebSocket first, fallback to polling
        if (this.initWebSocket()) {
            console.log('WebSocket initialized');
        } else {
            console.log('WebSocket not available, using polling');
            this.startPolling();
        }
        
        // Check immediately on page load
        this.checkForUpdates();
    }

    initWebSocket() {
        return; // Disabled notification connection
        
        if (!window.WebSocket) {
            return false;
        }

        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;
            
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                console.log('WebSocket connected');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.reconnectDelay = 1000;
                
                // Show connection status
                this.showCustomNotification(
                    'Connected',
                    'Real-time notifications are now active',
                    'success'
                );
                
                // Stop polling if it was running
                this.stopPolling();
            };
            
            this.websocket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleWebSocketMessage(data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            };
            
            this.websocket.onclose = (event) => {
                console.log('WebSocket disconnected');
                this.isConnected = false;
                
                if (event.code !== 1000) { // Not a normal closure
                    this.handleWebSocketDisconnect();
                }
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.handleWebSocketError();
            };
            
            return true;
        } catch (error) {
            console.error('Failed to initialize WebSocket:', error);
            return false;
        }
    }

    createContainer() {
        if (this.container) return;
        
        this.container = document.createElement('div');
        this.container.className = 'notification-container';
        document.body.appendChild(this.container);
    }

    async checkForUpdates() {
        try {
            const response = await fetch('/users/api/check-updates/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const data = await response.json();
                
                if (data.has_updates) {
                    data.updates.forEach(update => {
                        this.showNotification(update);
                    });
                }

                // Update last checked timestamp
                this.lastChecked = new Date().toISOString();
                localStorage.setItem('lastNotificationCheck', this.lastChecked);
            }
        } catch (error) {
            console.error('Error checking for updates:', error);
        }
    }

    showNotification(update) {
        const notification = this.createNotificationElement(update);
        this.container.appendChild(notification);

        // Auto-remove after 7 seconds
        setTimeout(() => {
            this.removeNotification(notification);
        }, 7000);

        // Show browser notification if permitted
        this.showBrowserNotification(update);
    }

    createNotificationElement(update) {
        const notification = document.createElement('div');
        notification.className = `notification-toast ${this.getNotificationClass(update.status)} notification-status-update`;

        const iconClass = this.getStatusIcon(update.status);
        
        notification.innerHTML = `
            <div class="notification-icon">
                <i class="fas ${iconClass}"></i>
            </div>
            <div class="notification-content">
                <div class="notification-title">Report #${update.report_id} Status Update</div>
                <p class="notification-message">${update.message}</p>
                <div class="notification-meta">
                    <i class="fas fa-clock"></i>
                    <span>${this.formatTime(update.timestamp)}</span>
                    ${update.authority ? `<i class="fas fa-user-shield"></i><span>by ${update.authority}</span>` : ''}
                </div>
                <a href="/users/report/${update.report_id}/" class="notification-action">
                    <i class="fas fa-arrow-right"></i>
                    View Details
                </a>
            </div>
            <button class="notification-close" onclick="notificationSystem.removeNotification(this.parentElement)">
                <i class="fas fa-times"></i>
            </button>
        `;

        return notification;
    }

    getNotificationClass(status) {
        switch(status) {
            case 'under_review': return 'info';
            case 'resolved': return 'success';
            case 'rejected': return 'error';
            case 'pending': return 'warning';
            default: return 'info';
        }
    }

    getStatusIcon(status) {
        switch(status) {
            case 'under_review': return 'fa-eye';
            case 'resolved': return 'fa-check-circle';
            case 'rejected': return 'fa-times-circle';
            case 'pending': return 'fa-clock';
            default: return 'fa-bell';
        }
    }

    getStatusMessage(status, authority = null) {
        const authorityText = authority ? ` by ${authority}` : '';
        
        switch(status) {
            case 'under_review': 
                return `Your report is now being reviewed${authorityText}`;
            case 'resolved': 
                return `Your report has been marked as resolved${authorityText}`;
            case 'rejected': 
                return `Your report has been rejected${authorityText}`;
            case 'pending': 
                return `Your report status has been updated to pending`;
            default: 
                return `Your report status has been updated`;
        }
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffInMinutes = Math.floor((now - date) / 60000);
        
        if (diffInMinutes < 1) return 'Just now';
        if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
        if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
        return date.toLocaleDateString();
    }

    removeNotification(notification) {
        if (notification && notification.parentElement) {
            notification.classList.add('hiding');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.parentElement.removeChild(notification);
                }
            }, 300);
        }
    }

    async showBrowserNotification(update) {
        if (!('Notification' in window)) return;

        if (Notification.permission === 'granted') {
            const notification = new Notification(`CivicScan - Report #${update.report_id}`, {
                body: update.message,
                icon: '/static/icons/notification-icon.png',
                badge: '/static/icons/badge-icon.png',
                tag: `report-${update.report_id}`,
                requireInteraction: false,
                silent: false
            });

            notification.onclick = () => {
                window.focus();
                window.location.href = `/users/report/${update.report_id}/`;
                notification.close();
            };

            setTimeout(() => notification.close(), 5000);
        } else if (Notification.permission === 'default') {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                this.showBrowserNotification(update);
            }
        }
    }

    startRealTimeChecking() {
        // Check every 30 seconds for new updates
        this.checkInterval = setInterval(() => {
            this.checkForUpdates();
        }, 30000);
    }

    stopRealTimeChecking() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
    }

    // Public method to manually trigger a check
    manualCheck() {
        this.checkForUpdates();
    }

    // Show a custom notification (for testing or manual notifications)
    showCustomNotification(title, message, type = 'info', reportId = null) {
        const update = {
            report_id: reportId || 0,
            message: message,
            status: type,
            timestamp: new Date().toISOString(),
            authority: null
        };
        this.showNotification(update);
    }

    // Clean up when page unloads
    cleanup() {
        this.stopRealTimeChecking();
        if (this.container && this.container.parentElement) {
            this.container.parentElement.removeChild(this.container);
        }
    }
}

// Initialize the notification system
let notificationSystem;

document.addEventListener('DOMContentLoaded', function() {
    notificationSystem = new NotificationSystem();
    
    // Request notification permission on first visit
    if ('Notification' in window && Notification.permission === 'default') {
        // Show a subtle prompt to enable notifications
        setTimeout(() => {
            if (confirm('Would you like to receive real-time notifications when your report status changes?')) {
                Notification.requestPermission();
            }
        }, 3000);
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (notificationSystem) {
        notificationSystem.cleanup();
    }
});

// Add live indicator to dashboard
function addLiveIndicator() {
    const headerSection = document.querySelector('.section-header');
    if (headerSection && !document.querySelector('.live-indicator')) {
        const liveIndicator = document.createElement('div');
        liveIndicator.className = 'live-indicator';
        liveIndicator.innerHTML = 'Live Updates';
        liveIndicator.style.position = 'absolute';
        liveIndicator.style.top = '20px';
        liveIndicator.style.right = '20px';
        headerSection.style.position = 'relative';
        headerSection.appendChild(liveIndicator);
    }
}

// Add live indicator when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    addLiveIndicator();
});

// Export for global access
window.notificationSystem = notificationSystem;