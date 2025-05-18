// Service Worker для BARLAU.KZ PWA
const CACHE_NAME = 'barlau-cache-v1';

// Ресурсы, которые будут закэшированы при установке
const CACHE_URLS = [
  '/',
  '/dashboard/',
  '/tasks/',
  '/trips/',
  '/employees/',
  '/static/core/css/styles.css',
  '/static/core/js/main.js',
  '/static/core/js/pwa.js',
  '/static/core/img/logo.png',
  '/static/core/img/mobile/home.svg',
  '/static/core/img/mobile/truck.svg',
  '/static/core/img/mobile/employee.svg',
  '/static/core/img/mobile/check-square.svg',
  '/static/core/img/mobile/location.svg'
];

// Дополнительные статические ресурсы для долгосрочного кэширования
const STATIC_CACHE_URLS = [
  '/static/core/css/bootstrap.min.css',
  '/static/core/js/bootstrap.bundle.min.js',
  '/static/core/js/sweetalert2.min.js',
  '/static/core/css/sweetalert2.min.css',
  '/static/core/js/flatpickr.min.js',
  '/static/core/css/flatpickr.min.css',
  '/manifest.json'
];

// Установка сервис-воркера и кэширование ресурсов
self.addEventListener('install', (event) => {
  console.log('Service Worker устанавливается');
  
  // Кэш основных ресурсов для офлайн работы
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Кэширование основных ресурсов');
        return cache.addAll(CACHE_URLS);
      })
      .then(() => {
        // Кэширование статических ресурсов
        return caches.open('static-assets-cache')
          .then(cache => {
            console.log('Кэширование статических ресурсов');
            return cache.addAll(STATIC_CACHE_URLS);
          });
      })
      .then(() => {
        // Принудительная активация service worker
        return self.skipWaiting();
      })
  );
});

// Активация сервис-воркера и очистка старых кэшей
self.addEventListener('activate', (event) => {
  console.log('Service Worker активируется');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(cacheName => {
          // Удаляем все старые кэши
          return cacheName.startsWith('barlau-') && cacheName !== CACHE_NAME;
        }).map(cacheName => {
          console.log('Удаление устаревшего кэша', cacheName);
          return caches.delete(cacheName);
        })
      );
    }).then(() => {
      // Контролирование всех клиентов (страниц)
      return self.clients.claim();
    })
  );
});

// Стратегия кэширования - сначала сеть, затем кэш
async function networkFirstThenCache(request) {
  try {
    // Пробуем получить ресурс из сети
    const networkResponse = await fetch(request);
    
    // Если ответ успешный, кэшируем и возвращаем его
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
      return networkResponse;
    }
    
    // Если ответ не успешный, ищем в кэше
    throw new Error('Ответ сети не успешный');
  } catch (error) {
    console.log('Ошибка сети, пробуем получить из кэша', error);
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Если ресурса нет в кэше, возвращаем страницу офлайн (для HTML запросов)
    if (request.headers.get('Accept').includes('text/html')) {
      return caches.match('/offline.html');
    }
    
    // Возвращаем ошибку для остальных типов запросов
    throw error;
  }
}

// Стратегия кэширования для API - только сеть, с сохранением запроса для синхронизации
async function networkOnlyWithBackup(request) {
  try {
    return await fetch(request);
  } catch (error) {
    // Если запрос к API и метод не GET, сохраняем для последующей синхронизации
    if (request.url.includes('/api/') && request.method !== 'GET') {
      await saveRequestForSync(request.clone());
      
      // Возвращаем "успешный" ответ клиенту
      return new Response(JSON.stringify({
        success: true,
        offline: true,
        message: 'Запрос будет отправлен, когда соединение с интернетом восстановится'
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    throw error;
  }
}

// Стратегия кэширования для статических ресурсов - сначала кэш, затем сеть
async function cacheFirstThenNetwork(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // Если нет в кэше, пробуем получить из сети и кэшируем
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open('static-assets-cache');
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('Ошибка получения из сети', error);
    
    // Возвращаем ошибку офлайн для статического контента
    if (request.url.endsWith('.png') || request.url.endsWith('.jpg') || request.url.endsWith('.svg')) {
      return caches.match('/static/core/img/placeholder.png');
    }
    
    throw error;
  }
}

// Обработка запросов fetch
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  
  // Для API запросов используем только сеть
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .catch(error => {
          console.error('Ошибка при запросе к API:', error);
          return new Response(
            JSON.stringify({
              error: 'Нет соединения с сервером'
            }), {
              status: 503,
              headers: {
                'Content-Type': 'application/json'
              }
            }
          );
        })
    );
    return;
  }
  
  // Для статических ресурсов используем стратегию сначала кэш, затем сеть
  if (url.pathname.startsWith('/static/') || 
      url.pathname.endsWith('.js') || 
      url.pathname.endsWith('.css') || 
      url.pathname.endsWith('.png') || 
      url.pathname.endsWith('.jpg') ||
      url.pathname.endsWith('.svg')) {
    event.respondWith(
      caches.match(request)
        .then(response => {
          return response || fetch(request)
            .then(response => {
              const responseClone = response.clone();
              caches.open(CACHE_NAME)
                .then(cache => {
                  cache.put(request, responseClone);
                });
              return response;
            });
        })
    );
    return;
  }
  
  // Для HTML-страниц используем стратегию сначала сеть, затем кэш
  if (request.headers.get('Accept').includes('text/html')) {
    event.respondWith(
      fetch(request)
        .catch(() => {
          return caches.match(request)
            .then(response => {
              return response || caches.match('/offline.html');
            });
        })
    );
    return;
  }
  
  // Для остальных запросов
  event.respondWith(
    caches.match(request)
      .then(response => {
        return response || fetch(request);
      })
  );
});

// Сохранение запроса для последующей синхронизации
async function saveRequestForSync(request) {
  // Клонируем запрос и извлекаем детали
  const requestDetails = {
    url: request.url,
    method: request.method,
    headers: Object.fromEntries(request.headers.entries()),
    body: await request.text(),
    timestamp: Date.now()
  };
  
  // Открываем или создаем IndexedDB для хранения запросов
  const db = await openDatabase();
  
  // Сохраняем запрос в IndexedDB
  const tx = db.transaction('requests', 'readwrite');
  await tx.objectStore('requests').add(requestDetails);
  await tx.complete;
  
  console.log('Запрос сохранен для синхронизации', requestDetails);
}

// Функция для открытия IndexedDB
function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('barlau-offline-requests', 1);
    
    request.onupgradeneeded = event => {
      const db = event.target.result;
      db.createObjectStore('requests', { keyPath: 'timestamp' });
    };
    
    request.onsuccess = event => resolve(event.target.result);
    request.onerror = event => reject(event.target.error);
  });
}

// Обработка события синхронизации
self.addEventListener('sync', event => {
  if (event.tag === 'sync-data') {
    console.log('Выполняется синхронизация данных');
    event.waitUntil(syncData());
  }
});

// Функция синхронизации данных
async function syncData() {
  try {
    const db = await openDatabase();
    const tx = db.transaction('requests', 'readonly');
    const store = tx.objectStore('requests');
    const requests = await store.getAll();
    
    // Если есть сохраненные запросы, отправляем их
    if (requests.length > 0) {
      console.log(`Найдено ${requests.length} запросов для синхронизации`);
      
      for (const requestDetails of requests) {
        try {
          // Создаем новый запрос из сохраненных данных
          const request = new Request(requestDetails.url, {
            method: requestDetails.method,
            headers: new Headers(requestDetails.headers),
            body: requestDetails.method !== 'GET' && requestDetails.method !== 'HEAD' ? 
                  requestDetails.body : undefined
          });
          
          // Отправляем запрос
          const response = await fetch(request);
          
          if (response.ok) {
            console.log('Запрос успешно синхронизирован', requestDetails.url);
            
            // Удаляем успешно отправленный запрос
            const deleteTx = db.transaction('requests', 'readwrite');
            await deleteTx.objectStore('requests').delete(requestDetails.timestamp);
            await deleteTx.complete;
          } else {
            console.error('Ошибка при синхронизации запроса', response.status, response.statusText);
          }
        } catch (error) {
          console.error('Ошибка при синхронизации запроса', error);
        }
      }
      
      // Уведомляем клиента о завершении синхронизации
      const clients = await self.clients.matchAll();
      clients.forEach(client => {
        client.postMessage({
          type: 'sync-complete',
          success: true
        });
      });
    }
  } catch (error) {
    console.error('Ошибка при синхронизации данных', error);
  }
}

// Обработка событий push уведомлений
self.addEventListener('push', event => {
  if (!event.data) return;
  
  // Извлекаем данные из push-уведомления
  const data = event.data.json();
  
  // Показываем уведомление
  const options = {
    body: data.body || 'Новое уведомление от BARLAU.KZ',
    icon: '/static/core/img/logo.png',
    badge: '/static/core/img/logo.png',
    data: data.data || {},
    vibrate: [100, 50, 100],
    actions: data.actions || []
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title || 'BARLAU.KZ', options)
  );
});

// Обработка клика по уведомлению
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  // Открытие соответствующей страницы при клике на уведомление
  const urlToOpen = event.notification.data.url || '/';
  
  event.waitUntil(
    self.clients.matchAll({ type: 'window' }).then(clients => {
      // Если есть открытое окно, фокусируемся на нем
      for (const client of clients) {
        if (client.url === urlToOpen && 'focus' in client) {
          return client.focus();
        }
      }
      
      // Если нет открытого окна, открываем новое
      if (self.clients.openWindow) {
        return self.clients.openWindow(urlToOpen);
      }
    })
  );
}); 