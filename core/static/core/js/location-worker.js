// Service Worker для фонового отслеживания геопозиции водителей
// v1.0.0

console.log('[SW] Service Worker загружен');

const CACHE_NAME = 'barlau-gps-cache-v1';
const LOCATION_UPDATE_INTERVAL = 30000; // 30 секунд

// Кэшируемые ресурсы для offline работы
const urlsToCache = [
    '/static/core/css/styles.css',
    '/static/core/js/app.js',
    '/offline/',
    '/static/core/img/logo.png'
];

// Установка Service Worker
self.addEventListener('install', function(event) {
    console.log('[SW] Установка Service Worker');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('[SW] Кэширование ресурсов');
                return cache.addAll(urlsToCache);
            })
    );
});

// Активация Service Worker
self.addEventListener('activate', function(event) {
    console.log('[SW] Активация Service Worker');
    
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[SW] Удаление старого кэша:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Обработка сетевых запросов
self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // Возвращаем кэшированную версию или делаем сетевой запрос
                if (response) {
                    return response;
                }
                
                return fetch(event.request).catch(function() {
                    // В случае отсутствия сети показываем offline страницу
                    if (event.request.destination === 'document') {
                        return caches.match('/offline/');
                    }
                });
            })
    );
});

// Фоновое отслеживание геопозиции
let locationTracking = {
    active: false,
    interval: null,
    lastPosition: null
};

// Сообщения от главной страницы
self.addEventListener('message', function(event) {
    console.log('[SW] Получено сообщение:', event.data);
    
    if (event.data.type === 'START_LOCATION_TRACKING') {
        startLocationTracking(event.data.options);
    } else if (event.data.type === 'STOP_LOCATION_TRACKING') {
        stopLocationTracking();
    } else if (event.data.type === 'GET_LOCATION_STATUS') {
        event.ports[0].postMessage({
            type: 'LOCATION_STATUS',
            active: locationTracking.active,
            lastPosition: locationTracking.lastPosition
        });
    }
});

// Запуск отслеживания геопозиции
function startLocationTracking(options = {}) {
    console.log('[SW] Запуск фонового отслеживания геопозиции');
    
    if (locationTracking.active) {
        console.log('[SW] Отслеживание уже активно');
        return;
    }
    
    locationTracking.active = true;
    
    // Периодическое обновление позиции
    locationTracking.interval = setInterval(function() {
        updateLocation(options);
    }, LOCATION_UPDATE_INTERVAL);
    
    // Первоначальное обновление
    updateLocation(options);
}

// Остановка отслеживания
function stopLocationTracking() {
    console.log('[SW] Остановка фонового отслеживания геопозиции');
    
    locationTracking.active = false;
    
    if (locationTracking.interval) {
        clearInterval(locationTracking.interval);
        locationTracking.interval = null;
    }
    
    locationTracking.lastPosition = null;
}

// Обновление позиции
async function updateLocation(options = {}) {
    if (!locationTracking.active) {
        return;
    }
    
    try {
        console.log('[SW] Попытка получить геопозицию');
        
        // В Service Worker нет прямого доступа к navigator.geolocation
        // Поэтому используем альтернативные методы или работаем через сообщения
        
        // Можно использовать Geolocation API через clients
        const clients = await self.clients.matchAll();
        
        if (clients.length > 0) {
            // Отправляем запрос на получение геопозиции активным клиентам
            clients[0].postMessage({
                type: 'REQUEST_LOCATION_UPDATE',
                timestamp: Date.now()
            });
        } else {
            console.log('[SW] Нет активных клиентов для получения геопозиции');
        }
        
    } catch (error) {
        console.error('[SW] Ошибка обновления геопозиции:', error);
    }
}

// Push уведомления (для будущего расширения)
self.addEventListener('push', function(event) {
    console.log('[SW] Получено push уведомление');
    
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body || 'Уведомление от Barlau.kz',
            icon: '/static/core/img/logo.png',
            badge: '/static/core/img/logo.png',
            vibrate: [200, 100, 200],
            data: data,
            actions: [
                {
                    action: 'open',
                    title: 'Открыть',
                    icon: '/static/core/img/logo.png'
                },
                {
                    action: 'close',
                    title: 'Закрыть'
                }
            ]
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title || 'Barlau.kz', options)
        );
    }
});

// Обработка кликов по уведомлениям
self.addEventListener('notificationclick', function(event) {
    console.log('[SW] Клик по уведомлению:', event.notification.tag);
    
    event.notification.close();
    
    if (event.action === 'open') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Фоновая синхронизация (для будущего расширения)
self.addEventListener('sync', function(event) {
    console.log('[SW] Фоновая синхронизация:', event.tag);
    
    if (event.tag === 'location-sync') {
        event.waitUntil(syncLocationData());
    }
});

// Синхронизация данных геопозиции
async function syncLocationData() {
    try {
        console.log('[SW] Синхронизация данных геопозиции');
        
        // Получаем сохраненные в IndexedDB данные геопозиции
        // и отправляем их на сервер при восстановлении соединения
        
        // Это можно расширить для офлайн работы
        
    } catch (error) {
        console.error('[SW] Ошибка синхронизации:', error);
    }
}

// Обработка видимости страницы
self.addEventListener('visibilitychange', function(event) {
    console.log('[SW] Изменение видимости страницы');
    
    // Когда страница становится невидимой, продолжаем отслеживание в фоне
    if (document.hidden && locationTracking.active) {
        console.log('[SW] Страница скрыта, продолжаем фоновое отслеживание');
    }
});

console.log('[SW] Service Worker инициализирован'); 