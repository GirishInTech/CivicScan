// Form handler for offline form submissions
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a form page
    const form = document.querySelector('form');
    if (!form) return;

    // Add data attribute to indicate this is a form that supports offline
    form.dataset.offline = 'true';
    
    // Add event listener for form submission
    form.addEventListener('submit', async function(e) {
        // Don't submit normally - we'll handle it
        e.preventDefault();
        
        // Check if we're online
        if (navigator.onLine) {
            // If online, submit the form normally
            form.submit();
            return;
        }
        
        // If offline, store the form data and show a message
        const formData = new FormData(form);
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });
        
        // Store the form data in localStorage
        const offlineForms = JSON.parse(localStorage.getItem('offlineForms') || '[]');
        offlineForms.push({
            url: form.action,
            method: form.method,
            data: formObject,
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('offlineForms', JSON.stringify(offlineForms));
        
        // Show success message
        alert('Your form has been saved and will be submitted when you\'re back online.');
        
        // Reset the form
        form.reset();
        
        // If we're on the report submission page, clear the photo preview
        const photoPreview = document.getElementById('photo-preview');
        if (photoPreview) {
            photoPreview.innerHTML = '';
        }
    });
    
    // Check for offline forms to submit when coming back online
    window.addEventListener('online', function() {
        const offlineForms = JSON.parse(localStorage.getItem('offlineForms') || '[]');
        if (offlineForms.length > 0) {
            // Show a notification that we're syncing
            const notification = document.createElement('div');
            notification.className = 'sync-notification';
            notification.textContent = 'Submitting saved forms...';
            document.body.appendChild(notification);
            
            // Submit each form
            Promise.all(offlineForms.map(formData => {
                return fetch(formData.url, {
                    method: formData.method,
                    body: JSON.stringify(formData.data),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
            }))
            .then(() => {
                // Clear the offline forms
                localStorage.removeItem('offlineForms');
                
                // Update the notification
                notification.textContent = 'All forms submitted successfully!';
                setTimeout(() => {
                    notification.remove();
                    // Reload the page to show updated data
                    window.location.reload();
                }, 2000);
            })
            .catch(error => {
                console.error('Error submitting offline forms:', error);
                notification.textContent = 'Error submitting some forms. Please try again later.';
                notification.style.backgroundColor = '#ffebee';
            });
        }
    });
});

// Add some basic styles for the sync notification
const style = document.createElement('style');
style.textContent = `
.sync-notification {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #e3f2fd;
    color: #0d47a1;
    padding: 12px 24px;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
`;
document.head.appendChild(style);
