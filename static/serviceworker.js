const CACHE_NAME = 'bb-cache-v5';  // Bumped version to force update
const OFFLINE_URL = '/offline/';

// Get the current origin
const CURRENT_ORIGIN = self.location.origin;

const urlsToCache = [
  '/',                            // Homepage
  OFFLINE_URL,                   // Offline fallback
  '/static/css/style.css',       // Main CSS
  '/static/js/script.js',        // Main JS
  '/static/icons/icon-192.png',  // Icons
  '/static/icons/icon-512.png',
  '/static/icons/icon-96.png',
  '/static/manifest.json',       // Manifest
  '/reports/submit/',            // Report submission
  '/users/signup/',              // User signup
  '/accounts/login/',            // User login
  '/static/images/offline-illustration.svg',  // Offline illustration
  '/static/js/form-handler.js'   // Form handling script
].map(url => new URL(url, self.location.origin).pathname);

console.log('[ServiceWorker] Caching URLs:', urlsToCache);

// Log that service worker is loaded
console.log('[ServiceWorker] Loaded');


// Install Event
self.addEventListener('install', event => {
  console.log('[ServiceWorker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[ServiceWorker] Caching assets:', urlsToCache);
        return cache.addAll(urlsToCache.map(url => {
          // Ensure URLs are absolute
          return url.startsWith('http') ? url : new URL(url, self.location.origin).href;
        }));
      })
      .then(() => self.skipWaiting())
      .catch(error => {
        console.error('[ServiceWorker] Failed to cache:', error);
        // Don't fail the installation if some assets fail to cache
        return self.skipWaiting();
      })
  );
});


// Activate Event
self.addEventListener('activate', event => {
  console.log('[ServiceWorker] Activating...');
  event.waitUntil(
    caches.keys().then(cacheNames =>
      Promise.all(
        cacheNames.map(name => {
          if (name !== CACHE_NAME) {
            console.log('[ServiceWorker] Deleting old cache:', name);
            return caches.delete(name);
          }
        })
      )
    )
  );
  self.clients.claim();
});


// Fetch Event - Enhanced caching strategy
self.addEventListener('fetch', event => {
  // Skip non-GET requests and chrome-extension requests
  if (event.request.method !== 'GET' || 
      event.request.url.startsWith('chrome-extension://') ||
      event.request.url.includes('browser-sync') ||
      event.request.url.includes('sockjs') ||
      event.request.url.includes('hot-update')) {
    return;
  }

  // Handle navigation requests (pages)
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .catch(() => {
          console.log('[ServiceWorker] Navigation failed, serving offline page');
          return caches.match(OFFLINE_URL);
        })
    );
    return;
  }

  // For other requests, try cache first, then network
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached response if found
        if (response) {
          console.log('[ServiceWorker] Serving from cache:', event.request.url);
          return response;
        }
        
        // For non-GET requests or non-http(s) requests, just fetch
        if (event.request.method !== 'GET' || !event.request.url.startsWith('http')) {
          return fetch(event.request);
        }
        
        // Special handling for form pages - return them even if offline
        const url = new URL(event.request.url);
        const isFormPage = url.pathname === '/reports/submit/' || 
                           url.pathname === '/users/signup/' || 
                           url.pathname === '/accounts/login/';
                           
        if (isFormPage) {
          return caches.match(event.request).then(response => {
            return response || fetch(event.request).catch(() => caches.match(OFFLINE_URL));
          });
        }

        // Otherwise, fetch from network
        return fetch(event.request)
          .then(fetchResponse => {
            // Check if we received a valid response
            if (!fetchResponse || fetchResponse.status !== 200 || fetchResponse.type !== 'basic') {
              return fetchResponse;
            }

            // Clone the response for caching
            const responseToCache = fetchResponse.clone();

            // Cache static assets and important pages
            const url = new URL(event.request.url);
            const isImportantPage = ['/reports/submit/', '/users/signup/', '/accounts/login/'].some(path => 
              url.pathname.startsWith(path)
            );
            
            if (event.request.url.includes('/static/') || 
                isImportantPage ||
                event.request.url.includes('/reports/') ||
                event.request.url.includes('/users/')) {
              caches.open(CACHE_NAME)
                .then(cache => cache.put(event.request, responseToCache))
                .catch(err => console.error('[ServiceWorker] Cache put error:', err));
            }

            return fetchResponse;
          })
          .catch(error => {
            console.error('[ServiceWorker] Fetch failed:', error);
            // For API/data requests, return a more specific offline response
            if (event.request.url.includes('/api/')) {
              return new Response(JSON.stringify({ error: 'You are offline' }), {
                status: 503,
                statusText: 'Service Unavailable',
                headers: new Headers({
                  'Content-Type': 'application/json'
                })
              });
            }
            // For other failed requests, return nothing
            return new Response('', { status: 408, statusText: 'Request Timeout' });
          });
      })
  );
});

// Background Sync for offline form submissions
self.addEventListener('sync', event => {
  console.log('[ServiceWorker] Background sync triggered:', event.tag);
  
  if (event.tag === 'background-sync-reports') {
    event.waitUntil(syncOfflineReports());
  }
});

// Function to sync offline reports
async function syncOfflineReports() {
  try {
    // Get offline reports from IndexedDB (to be implemented)
    console.log('[ServiceWorker] Syncing offline reports...');
    // Implementation will be added when we implement offline storage
  } catch (error) {
    console.error('[ServiceWorker] Sync failed:', error);
  }
}
