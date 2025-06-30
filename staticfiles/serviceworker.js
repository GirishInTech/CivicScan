const CACHE_NAME = 'bb-cache-v2';

const urlsToCache = [
  '/',                            // Homepage
  // '/offline/',                    // Offline fallback
  '/static/css/style.css',        // Main CSS
  '/static/js/script.js',         // Main JS
  '/static/icons/icon-192.png',   // Icon
  '/static/icons/icon-512.png'    // Icon
];

// Log that service worker is loaded
console.log('[ServiceWorker] Loaded');


// Install Event
self.addEventListener('install', event => {
  console.log('[ServiceWorker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[ServiceWorker] Caching assets:', urlsToCache);
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting())
      .catch(error => {
        console.error('[ServiceWorker] Failed to cache:', error);
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


// Fetch Event
self.addEventListener('fetch', event => {
  console.log('[ServiceWorker] Fetching:', event.request.url);
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request).catch(() => {
        if (event.request.mode === 'navigate') {
          console.warn('[ServiceWorker] Offline fallback triggered.');
          return caches.match('/offline/');
        }
      });
    })
  );
});
