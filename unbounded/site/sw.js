var CACHE = 'unbounded-v1';
var URLS = [
  './',
  './portal.html',
  './dashboard.html',
  './index.html',
  './favicon.svg',
  './manifest.json',
  './pages/index.html',
  './pages/docs/manifesto.html',
  './pages/docs/platform-blueprint.html',
  './pages/docs/roadmap.html',
  './pages/docs/index.html',
  './pages/unbounded/welcome.html',
  './pages/unbounded/governance.html',
  './pages/unbounded/contributing.html',
  './pages/unbounded/index.html',
  './pages/termite/master-summary.html',
  './pages/termite/cross-verification.html',
  './pages/termite/readme.html',
  './pages/termite/lab-notebook.html',
  './pages/termite/pitch.html',
  './pages/termite/index.html',
  './pages/calls/open-letter.html',
  './pages/calls/for-developers.html',
  './pages/calls/for-creatives.html',
  './pages/calls/index.html'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      return cache.addAll(URLS);
    }).then(function() {
      return self.skipWaiting();
    })
  );
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(names) {
      return Promise.all(
        names.filter(function(n) { return n !== CACHE; }).map(function(n) { return caches.delete(n); })
      );
    }).then(function() {
      return self.clients.claim();
    })
  );
});

self.addEventListener('fetch', function(e) {
  var url = new URL(e.request.url);

  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(
      caches.match(e.request).then(function(cached) { return cached || fetch(e.request).then(function(res) { return caches.open(CACHE).then(function(cache) { cache.put(e.request, res.clone()); return res; }); }); })
    );
    return;
  }

  if (url.hostname !== location.hostname) {
    return;
  }

  if (url.pathname.match(/\.(js|css|png|jpg|gif|svg|woff2?|ico)$/)) {
    e.respondWith(
      caches.match(e.request).then(function(cached) { return cached || fetch(e.request); })
    );
    return;
  }

  e.respondWith(
    fetch(e.request).then(function(res) {
      var clone = res.clone();
      caches.open(CACHE).then(function(cache) { if (res.ok) cache.put(e.request, clone); });
      return res;
    }).catch(function() {
      return caches.match(e.request);
    })
  );
});
