// Service Worker для BARLAU.KZ
const CACHE_NAME = 'barlau-cache-v1';
const URLS_TO_CACHE = [
  '/',
  '/app.html',
  '/manifest.json',
  '/icons/icon-72x72.png',
  '/icons/icon-96x96.png',
  '/icons/icon-128x128.png',
  '/icons/icon-144x144.png',
  '/icons/icon-152x152.png',
  '/icons/icon-192x192.png',
  '/icons/icon-384x384.png',
  '/icons/icon-512x512.png',
  '/icons/maskable-icon.png'
];

// Установка Service Worker и кэширование ресурсов
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Кэширование ресурсов');
        return cache.addAll(URLS_TO_CACHE);
      })
      .then(() => self.skipWaiting())
  );
});

// Активация и очистка старых кэшей
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.filter(cacheName => {
            return cacheName.startsWith('barlau-') && cacheName !== CACHE_NAME;
          }).map(cacheName => {
            return caches.delete(cacheName);
          })
        );
      })
      .then(() => self.clients.claim())
  );
});

// Стратегия кэширования: сначала кэш, затем сеть
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Если ресурс найден в кэше, возвращаем его
        if (response) {
          return response;
        }

        // Клонируем запрос, так как он может быть использован только один раз
        const fetchRequest = event.request.clone();

        // Делаем запрос к сети
        return fetch(fetchRequest)
          .then(response => {
            // Проверяем корректность ответа
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Клонируем ответ, так как его тело также может быть использовано только один раз
            const responseToCache = response.clone();

            // Добавляем новый ответ в кэш
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });

            return response;
          })
          .catch(() => {
            // Если запрос не удался и это запрос страницы, возвращаем страницу из кэша
            if (event.request.mode === 'navigate') {
              return caches.match('/app.html');
            }
            // Для других ресурсов можно вернуть запасное изображение или другой контент
            return new Response('Нет интернет-соединения');
          });
      })
  );
});

// Обработка событий синхронизации для отправки данных при восстановлении соединения
self.addEventListener('sync', event => {
  if (event.tag === 'sync-data') {
    event.waitUntil(
      // Здесь можно реализовать логику для синхронизации данных
      console.log('Синхронизация данных при восстановлении соединения')
    );
  }
});

// Обработка push-уведомлений
self.addEventListener('push', event => {
  if (!event.data) return;

  const data = event.data.json();
  const options = {
    body: data.body || 'Новое уведомление',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/'
    }
  };

  event.waitUntil(
    self.registration.showNotification(data.title || 'BARLAU.KZ', options)
  );
});

// Обработка клика по уведомлению
self.addEventListener('notificationclick', event => {
  event.notification.close();

  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
}); 