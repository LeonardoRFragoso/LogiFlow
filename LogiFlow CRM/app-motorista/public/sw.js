// LogiFlow CRM - Service Worker (PWA)
// Permite funcionamento offline do App do Motorista

const CACHE_NAME = 'logiflow-motorista-v1';
const OFFLINE_URL = '/offline.html';

// Arquivos para cachear (App Shell)
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/offline.html',
  '/manifest.json'
];

// URLs da API que devem ser cacheadas
const API_CACHE_NAME = 'logiflow-api-v1';
const API_URLS_TO_CACHE = [
  '/pedidos/em-andamento',
  '/motoristas/me'
];

// ==========================================
// Instalação do Service Worker
// ==========================================
self.addEventListener('install', (event) => {
  console.log('[SW] Instalando Service Worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Cacheando arquivos estáticos');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('[SW] Service Worker instalado');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[SW] Erro na instalação:', error);
      })
  );
});

// ==========================================
// Ativação do Service Worker
// ==========================================
self.addEventListener('activate', (event) => {
  console.log('[SW] Ativando Service Worker...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name !== CACHE_NAME && name !== API_CACHE_NAME)
            .map((name) => {
              console.log('[SW] Removendo cache antigo:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        console.log('[SW] Service Worker ativado');
        return self.clients.claim();
      })
  );
});

// ==========================================
// Interceptação de Requisições (Fetch)
// ==========================================
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Ignorar requisições não-GET
  if (request.method !== 'GET') {
    return;
  }
  
  // Ignorar extensões do navegador
  if (url.protocol === 'chrome-extension:') {
    return;
  }
  
  // Estratégia para requisições de API
  if (url.pathname.startsWith('/api') || url.hostname.includes('localhost:8000')) {
    event.respondWith(networkFirstStrategy(request));
    return;
  }
  
  // Estratégia para arquivos estáticos
  event.respondWith(cacheFirstStrategy(request));
});

// ==========================================
// Estratégias de Cache
// ==========================================

// Cache First: Primeiro tenta o cache, depois a rede
async function cacheFirstStrategy(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    // Atualiza o cache em background
    fetchAndCache(request);
    return cachedResponse;
  }
  
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    // Se falhar e for navegação, mostra página offline
    if (request.mode === 'navigate') {
      return caches.match(OFFLINE_URL);
    }
    throw error;
  }
}

// Network First: Primeiro tenta a rede, depois o cache
async function networkFirstStrategy(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cacheia resposta de API bem-sucedida
      const cache = await caches.open(API_CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Rede falhou, buscando no cache:', request.url);
    
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Retorna resposta de erro personalizada para API
    return new Response(
      JSON.stringify({
        success: false,
        offline: true,
        message: 'Você está offline. Os dados exibidos podem estar desatualizados.'
      }),
      {
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

// Atualiza cache em background
async function fetchAndCache(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
  } catch (error) {
    // Silenciosamente falha - o usuário já tem a versão cacheada
  }
}

// ==========================================
// Background Sync (Sincronização Offline)
// ==========================================
self.addEventListener('sync', (event) => {
  console.log('[SW] Background Sync:', event.tag);
  
  if (event.tag === 'sync-entregas') {
    event.waitUntil(syncEntregas());
  }
  
  if (event.tag === 'sync-posicao') {
    event.waitUntil(syncPosicaoGPS());
  }
});

async function syncEntregas() {
  try {
    // Busca atualizações pendentes do IndexedDB
    const pendingUpdates = await getPendingUpdates();
    
    for (const update of pendingUpdates) {
      await fetch(update.url, {
        method: update.method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(update.data)
      });
      
      // Remove do IndexedDB após sucesso
      await removePendingUpdate(update.id);
    }
    
    console.log('[SW] Sincronização de entregas concluída');
  } catch (error) {
    console.error('[SW] Erro na sincronização:', error);
    throw error; // Tenta novamente depois
  }
}

async function syncPosicaoGPS() {
  try {
    const pendingPositions = await getPendingPositions();
    
    if (pendingPositions.length > 0) {
      await fetch('/api/rastreamento/posicao/batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ posicoes: pendingPositions })
      });
      
      await clearPendingPositions();
    }
    
    console.log('[SW] Sincronização de posições GPS concluída');
  } catch (error) {
    console.error('[SW] Erro na sincronização de GPS:', error);
    throw error;
  }
}

// ==========================================
// Push Notifications
// ==========================================
self.addEventListener('push', (event) => {
  console.log('[SW] Push recebido');
  
  let data = {
    title: 'LogiFlow',
    body: 'Nova notificação',
    icon: '/icons/icon-192.png',
    badge: '/icons/badge-72.png'
  };
  
  if (event.data) {
    try {
      data = { ...data, ...event.data.json() };
    } catch (e) {
      data.body = event.data.text();
    }
  }
  
  const options = {
    body: data.body,
    icon: data.icon,
    badge: data.badge,
    vibrate: [200, 100, 200],
    tag: data.tag || 'logiflow-notification',
    renotify: true,
    data: data.data || {},
    actions: data.actions || [
      { action: 'open', title: 'Abrir' },
      { action: 'close', title: 'Fechar' }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Clique na notificação
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notificação clicada:', event.action);
  
  event.notification.close();
  
  if (event.action === 'close') {
    return;
  }
  
  // Abre o app ou foca na janela existente
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        // Se já tem uma janela aberta, foca nela
        for (const client of clientList) {
          if (client.url.includes('/') && 'focus' in client) {
            return client.focus();
          }
        }
        // Senão, abre uma nova
        if (clients.openWindow) {
          const url = event.notification.data?.url || '/';
          return clients.openWindow(url);
        }
      })
  );
});

// ==========================================
// Helpers para IndexedDB (Stubs)
// ==========================================

// Em produção, implementar com IndexedDB real
async function getPendingUpdates() {
  return [];
}

async function removePendingUpdate(id) {
  return true;
}

async function getPendingPositions() {
  return [];
}

async function clearPendingPositions() {
  return true;
}

// ==========================================
// Mensagens do App
// ==========================================
self.addEventListener('message', (event) => {
  console.log('[SW] Mensagem recebida:', event.data);
  
  if (event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data.type === 'CACHE_URLS') {
    cacheUrls(event.data.urls);
  }
});

async function cacheUrls(urls) {
  const cache = await caches.open(CACHE_NAME);
  await cache.addAll(urls);
  console.log('[SW] URLs cacheadas:', urls.length);
}

console.log('[SW] Service Worker carregado');
