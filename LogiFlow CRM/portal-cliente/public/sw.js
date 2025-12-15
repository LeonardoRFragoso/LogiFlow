// LogiFlow Portal - Service Worker
const CACHE_NAME = 'logiflow-portal-v1.0.0'

const STATIC_FILES = [
  '/',
  '/index.html',
  '/manifest.json'
]

// Instalar
self.addEventListener('install', (event) => {
  console.log('[Portal SW] Instalando...')
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(STATIC_FILES))
      .then(() => self.skipWaiting())
  )
})

// Ativar
self.addEventListener('activate', (event) => {
  console.log('[Portal SW] Ativando...')
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName)
          }
        })
      )
    }).then(() => self.clients.claim())
  )
})

// Interceptar requisições
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  )
})

console.log('[Portal SW] Carregado!')

