self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('glasses-v1').then((cache) => {
      return cache.addAll([
        '/mobile.html',
        '/manifest.json',
        '/sw.js'
      ]);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
