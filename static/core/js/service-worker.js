// Service Worker для BARLAU.KZ PWA
const CACHE_NAME = 'barlau-cache-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/static/core/css/tailwind.min.css',
  '/static/core/js/main.js',
  '/static/core/img/logo.png',
  '/static/core/img/icons/icon-72x72.png',
  '/static/core/img/icons/icon-96x96.png',
  '/static/core/img/icons/icon-128x128.png',
  '/static/core/img/icons/icon-144x144.png',
  '/static/core/img/icons/icon-152x152.png',
  '/static/core/img/icons/icon-192x192.png',
  '/static/core/img/icons/icon-384x384.png',
  '/static/core/img/icons/icon-512x512.png',
  '/static/core/img/mobile/home.svg',
  '/static/core/img/mobile/check-square.svg',
  '/static/core/img/mobile/location.svg',
  '/static/core/img/mobile/truck.svg',
  '/static/core/img/mobile/employee.svg',
  '/static/core/img/home.svg',
  '/static/core/img/check-square.svg',
  '/static/core/img/location.svg',
  '/static/core/img/truck.svg',
  '/static/core/img/employee.svg',
  '/static/core/img/bell.svg',
  '/static/core/img/avatars/placeholder.jpg'
];

// Установка сервис-воркера и кэширование ресурсов
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Открыт кэш');
        return cache.addAll(urlsToCache);
      })
  );
});

// Активация сервис-воркера и очистка старых кэшей
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Стратегия кэширования: сначала кэш, затем сеть
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Если ресурс в кэше, возвращаем его
        if (response) {
          return response;
        }
        
        // Иначе делаем запрос к сети
        return fetch(event.request)
          .then((response) => {
            // Проверяем валидность ответа
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // Клонируем ответ, так как он может быть использован только один раз
            const responseToCache = response.clone();
            
            // Добавляем ответ в кэш для будущих запросов
            caches.open(CACHE_NAME)
              .then((cache) => {
                // Кэшируем только GET-запросы к статическим ресурсам
                if (event.request.method === 'GET' && 
                   (event.request.url.includes('/static/') || 
                    event.request.url.endsWith('/') || 
                    event.request.url.includes('/media/'))) {
                  cache.put(event.request, responseToCache);
                }
              });
            
            return response;
          });
      })
      .catch(() => {
        // Для страниц при отсутствии сети возвращаем офлайн-страницу
        if (event.request.headers.get('accept').includes('text/html')) {
          return caches.match('/offline.html');
        }
      })
  );
});

// Добавляем синхронизацию при восстановлении подключения
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-data') {
    event.waitUntil(syncData());
  }
});

// Функция для синхронизации данных
function syncData() {
  // Здесь логика для синхронизации офлайн-данных с сервером
  return fetch('/api/v1/sync-data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      timestamp: new Date().toISOString()
    })
  });
} 