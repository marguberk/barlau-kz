// Имя кэша
const CACHE_NAME = 'barlau-app-cache-v1';

// Ресурсы для кэширования
const urlsToCache = [
  '/',
  '/index.html',
  '/cordova.js',
  '/js/app.js',
  '/img/logo.png',
  'https://barlau.kz'
];

// Установка Service Worker
self.addEventListener('install', event => {
  // Выполняем установку
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Кэш открыт');
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('Ошибка кэширования:', error);
      })
  );
});

// Активация Service Worker
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Перехват запросов
self.addEventListener('fetch', event => {
  // Для запросов к основному сайту, всегда проверяем сеть сначала,
  // а затем возвращаемся к кэшу если сеть недоступна
  if (event.request.url.includes('barlau.kz')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // Если получили корректный ответ, клонируем его и кэшируем
          if (response && response.status === 200) {
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
            return response;
          }
          
          return response;
        })
        .catch(() => {
          // При ошибке сети пробуем вернуть из кэша
          return caches.match(event.request);
        })
    );
  } else {
    // Для локальных ресурсов используем стратегию "кэш с отказом на сеть"
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          if (response) {
            return response;
          }
          
          return fetch(event.request)
            .then(response => {
              // Не кэшируем ответы с ошибками
              if (!response || response.status !== 200) {
                return response;
              }
              
              // Клонируем ответ
              const responseToCache = response.clone();
              
              caches.open(CACHE_NAME)
                .then(cache => {
                  cache.put(event.request, responseToCache);
                });
                
              return response;
            })
            .catch(error => {
              console.error('Fetch failed:', error);
              // При ошибке возвращаем специальное сообщение или пустой ответ
            });
        })
    );
  }
}); 