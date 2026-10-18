// The demo app used to live at the site root and registered a service worker here.
// This replacement clears its caches and unregisters itself so visitors get the plain site again.
// The demo now lives under /demo/ with its own worker (cache prefix "havn-demo-").
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(
  caches.keys()
    .then(ks => Promise.all(ks.filter(k => !k.startsWith('havn-demo-')).map(k => caches.delete(k))))
    .then(() => self.registration.unregister())
));
