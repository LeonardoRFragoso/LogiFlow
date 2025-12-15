// LogiFlow - Service Worker PWA
const CACHE_NAME = 'logiflow-motorista-v1.0.0'
const API_CACHE = 'logiflow-api-v1'

// Arquivos para cache offline
const STATIC_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png'
]

// Instalar Service Worker
self.addEventListener('install', (event) => {
  console.log('[SW] Instalando Service Worker...')
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Cache aberto, adicionando arquivos estáticos...')
        return cache.addAll(STATIC_FILES)
      })
      .then(() => self.skipWaiting())
  )
})

// Ativar Service Worker
self.addEventListener('activate', (event) => {
  console.log('[SW] Ativando Service Worker...')
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME && cacheName !== API_CACHE) {
            console.log('[SW] Removendo cache antigo:', cacheName)
            return caches.delete(cacheName)
          }
        })
      )
    }).then(() => self.clients.claim())
  )
})

// Interceptar requisições
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // Estratégia: Network First para API, Cache First para assets
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(request))
  } else {
    event.respondWith(cacheFirst(request))
  }
})

// Cache First: busca no cache primeiro, depois na rede
async function cacheFirst(request) {
  const cache = await caches.open(CACHE_NAME)
  const cached = await cache.match(request)
  
  if (cached) {
    console.log('[SW] Retornando do cache:', request.url)
    return cached
  }

  try {
    const response = await fetch(request)
    if (response.status === 200) {
      cache.put(request, response.clone())
    }
    return response
  } catch (error) {
    console.error('[SW] Erro ao buscar:', request.url, error)
    return new Response('Offline - Recurso não disponível', {
      status: 503,
      statusText: 'Service Unavailable'
    })
  }
}

// Network First: tenta rede primeiro, fallback para cache
async function networkFirst(request) {
  const cache = await caches.open(API_CACHE)
  
  try {
    const response = await fetch(request)
    if (response.status === 200) {
      cache.put(request, response.clone())
    }
    return response
  } catch (error) {
    console.log('[SW] Rede indisponível, buscando no cache:', request.url)
    const cached = await cache.match(request)
    if (cached) {
      return cached
    }
    return new Response(JSON.stringify({
      error: 'Offline',
      message: 'Você está offline. Algumas funcionalidades podem estar limitadas.'
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}

// Sincronização em background
self.addEventListener('sync', (event) => {
  console.log('[SW] Background Sync:', event.tag)
  
  if (event.tag === 'sync-entregas') {
    event.waitUntil(syncEntregas())
  }
})

async function syncEntregas() {
  try {
    console.log('[SW] Sincronizando entregas...')
    const response = await fetch('/api/v1/entregas/sync')
    if (response.ok) {
      console.log('[SW] Entregas sincronizadas com sucesso')
      // Notificar clientes (tabs abertas)
      const clients = await self.clients.matchAll()
      clients.forEach(client => {
        client.postMessage({
          type: 'SYNC_COMPLETE',
          data: { entregas: true }
        })
      })
    }
  } catch (error) {
    console.error('[SW] Erro ao sincronizar entregas:', error)
  }
}

// Push Notifications
self.addEventListener('push', (event) => {
  console.log('[SW] Push recebido:', event.data?.text())
  
  const data = event.data ? event.data.json() : {}
  const title = data.title || 'LogiFlow'
  const options = {
    body: data.body || 'Nova notificação',
    icon: '/icons/icon-192.png',
    badge: '/icons/badge.png',
    vibrate: [200, 100, 200],
    data: data.data || {},
    actions: data.actions || []
  }

  event.waitUntil(
    self.registration.showNotification(title, options)
  )
})

// Clique na notificação
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notificação clicada:', event.notification.tag)
  event.notification.close()

  const urlToOpen = event.notification.data?.url || '/'
  
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        // Se já tem uma janela aberta, foca nela
        for (let client of clientList) {
          if (client.url === urlToOpen && 'focus' in client) {
            return client.focus()
          }
        }
        // Senão, abre nova janela
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen)
        }
      })
  )
})

// Mensagens dos clientes
self.addEventListener('message', (event) => {
  console.log('[SW] Mensagem recebida:', event.data)
  
  if (event.data.type === 'SKIP_WAITING') {
    self.skipWaiting()
  }
  
  if (event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(CACHE_NAME)
        .then(cache => cache.addAll(event.data.urls))
    )
  }
})

console.log('[SW] Service Worker carregado!')
