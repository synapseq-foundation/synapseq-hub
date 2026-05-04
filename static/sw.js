// SynapSeq Hub Player — Service Worker
// Strategy:
//   - App shell (JS/CSS/fonts/images): cache-first, versioned cache
//   - Data files (manifest.json, .spsq): network-first, falls back to cache
//   - Audio streams (external audio.synapseq.org): never cached (large, external)

const CACHE_VERSION = 'synapseq-hub-v1';
const DATA_CACHE = 'synapseq-data-v1';

const APP_SHELL_PATTERNS = [
  /\/_app\/immutable\//,   // SvelteKit hashed bundles
  /\/artwork\//,           // local artwork images
  /fonts\.googleapis\.com/,
  /fonts\.gstatic\.com/,
  /\.webp$/,
  /\.png$/,
  /\.ico$/,
  /\.webmanifest$/,
];

const DATA_PATTERNS = [
  /\/manifest\.json$/,
  /\.spsq$/,
];

const NEVER_CACHE_PATTERNS = [
  /audio\.synapseq\.org/,  // external audio streams
];

function matchesAny(url, patterns) {
  return patterns.some((p) => p.test(url));
}

// ── Install ──────────────────────────────────────────────────────────────────
self.addEventListener('install', (event) => {
  // Precache the bare minimum so the app shell loads offline
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) =>
      cache.addAll([
        '/',
        '/pwa.webmanifest',
        '/artwork/default.webp',
      ])
    )
  );
  self.skipWaiting();
});

// ── Activate ─────────────────────────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k !== CACHE_VERSION && k !== DATA_CACHE)
          .map((k) => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

// ── Fetch ─────────────────────────────────────────────────────────────────────
self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = request.url;

  // Never touch audio streams
  if (matchesAny(url, NEVER_CACHE_PATTERNS)) return;

  // Network-first for dynamic data
  if (matchesAny(url, DATA_PATTERNS)) {
    event.respondWith(networkFirst(request, DATA_CACHE));
    return;
  }

  // Cache-first for app shell assets
  if (matchesAny(url, APP_SHELL_PATTERNS)) {
    event.respondWith(cacheFirst(request, CACHE_VERSION));
    return;
  }

  // Navigation requests (HTML pages) — network-first, fall back to cached root
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match('/'))
    );
  }
});

// ── Helpers ───────────────────────────────────────────────────────────────────
async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response.ok) {
    const cache = await caches.open(cacheName);
    cache.put(request, response.clone());
  }
  return response;
}

async function networkFirst(request, cacheName) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    if (cached) return cached;
    throw new Error(`Network unavailable and no cache for: ${request.url}`);
  }
}
