/**
 * BARLAU.KZ Mobile App
 * Файл для взаимодействия с нативными плагинами Cordova
 */

// Объект для хранения методов приложения
const App = {
    // Основные настройки
    config: {
        appUrl: 'https://barlau.kz',
        maxLoadTime: 30000,
        maxLoadAttempts: 3
    },
    
    // Инициализация приложения
    initialize: function() {
        document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
    },

    // Обработчик события готовности устройства
    onDeviceReady: function() {
        console.log('Устройство готово');
        
        // Инициализация функциональности приложения
        this.setupStatusBar();
        this.setupGeolocation();
        this.setupNotifications();
        this.setupDeepLinks();
        this.setupNetworkListeners();
        
        // Предзагрузка ресурсов
        this.preloadResources();
        
        // Подписка на события жизненного цикла приложения
        document.addEventListener("pause", this.onPause.bind(this), false);
        document.addEventListener("resume", this.onResume.bind(this), false);
        document.addEventListener("backbutton", this.onBackButton.bind(this), false);
        
        // Проверяем состояние сети после загрузки
        this.checkNetworkState();
    },
    
    // Предзагрузка ресурсов
    preloadResources: function() {
        const resources = ['img/logo.png'];
        resources.forEach(url => {
            if (url.endsWith('.png') || url.endsWith('.jpg') || url.endsWith('.jpeg') || url.endsWith('.gif')) {
                const img = new Image();
                img.src = url;
            }
        });
    },
    
    // Проверка состояния сети
    checkNetworkState: function() {
        let online = true;
        let networkType = 'unknown';
        
        if (navigator.connection) {
            networkType = navigator.connection.type;
            online = (networkType !== Connection.NONE);
        }
        
        console.log('Состояние сети:', online ? 'онлайн' : 'офлайн', 'тип:', networkType);
        
        if (!online) {
            // Отображаем сообщение об отсутствии соединения
            this.showConnectionError();
            // Проверяем наличие кэшированного контента
            this.checkCachedContent();
            return false;
        } else {
            // У нас есть соединение
            this.hideConnectionError();
            return true;
        }
    },
    
    // Проверка наличия кэшированного контента
    checkCachedContent: function() {
        if ('caches' in window) {
            caches.match(this.config.appUrl)
                .then(response => {
                    if (response) {
                        console.log('Найден кэшированный контент');
                        // Имеется кэшированная версия сайта
                        const errorContainer = document.getElementById('error-container');
                        const errorMessage = document.getElementById('error-message');
                        if (errorContainer && errorMessage) {
                            errorMessage.innerHTML = "Отсутствует подключение к интернету. Загружена кэшированная версия.<br>Некоторые функции могут быть недоступны.";
                        }
                    }
                })
                .catch(error => {
                    console.error('Ошибка при проверке кэша:', error);
                });
        }
    },
    
    // Показать ошибку соединения
    showConnectionError: function() {
        const errorContainer = document.getElementById('error-container');
        const errorMessage = document.getElementById('error-message');
        const loadingSpinner = document.getElementById('loading-spinner');
        
        if (errorContainer && errorMessage && loadingSpinner) {
            errorMessage.textContent = "Отсутствует подключение к интернету. Пожалуйста, проверьте ваше соединение.";
            errorContainer.style.display = 'block';
            loadingSpinner.style.display = 'none';
        }
    },
    
    // Скрыть ошибку соединения
    hideConnectionError: function() {
        const errorContainer = document.getElementById('error-container');
        const loadingSpinner = document.getElementById('loading-spinner');
        
        if (errorContainer && loadingSpinner) {
            errorContainer.style.display = 'none';
            loadingSpinner.style.display = 'block';
        }
    },
    
    // Настройка слушателей сетевых событий
    setupNetworkListeners: function() {
        document.addEventListener("offline", this.onOffline.bind(this), false);
        document.addEventListener("online", this.onOnline.bind(this), false);
    },

    // Настройка статус-бара
    setupStatusBar: function() {
        if (window.StatusBar) {
            // Установка цвета и стиля
            StatusBar.backgroundColorByHexString("#2563EB");
            StatusBar.styleLightContent();
            
            // Проверка платформы
            if (cordova.platformId === 'ios') {
                // iOS-специфические настройки
                StatusBar.overlaysWebView(false);
            }
        }
    },

    // Настройка геолокации
    setupGeolocation: function() {
        // Запрос разрешения на геолокацию при необходимости
        if (cordova.plugins && cordova.plugins.diagnostic) {
            cordova.plugins.diagnostic.isLocationAvailable(function(available) {
                if (!available) {
                    cordova.plugins.diagnostic.requestLocationAuthorization(
                        function(status) {
                            console.log("Статус авторизации геолокации: " + status);
                        }, 
                        function(error) {
                            console.error("Ошибка запроса геолокации: " + error);
                        }
                    );
                }
            });
        }
    },

    // Настройка push-уведомлений
    setupNotifications: function() {
        // Проверка наличия плагина уведомлений
        if (window.PushNotification) {
            const push = PushNotification.init({
                android: {},
                ios: {
                    alert: true,
                    badge: true,
                    sound: true
                }
            });

            push.on('registration', function(data) {
                // Отправка токена на сервер
                console.log("Токен регистрации: " + data.registrationId);
                
                // Здесь мы можем отправить токен на сервер
                // App.sendTokenToServer(data.registrationId);
            });

            push.on('notification', function(data) {
                // Обработка входящего уведомления
                console.log("Получено уведомление: ", data);
                
                // Можно выполнить действие в зависимости от данных уведомления
                if (data.additionalData && data.additionalData.url) {
                    // Например, открыть конкретную страницу
                    const frame = document.getElementById('appFrame');
                    if (frame) {
                        frame.src = data.additionalData.url;
                    }
                }
            });

            push.on('error', function(e) {
                console.error("Ошибка push-уведомлений: " + e.message);
            });
        }
    },

    // Настройка обработки deeplinks
    setupDeepLinks: function() {
        // Универсальные ссылки для iOS и App Links для Android
        if (window.universalLinks) {
            universalLinks.subscribe('openURL', function(eventData) {
                // Обработка deeplink
                console.log('Получен deeplink: ', eventData.url);
                
                // Загрузка нужного URL
                const frame = document.getElementById('appFrame');
                if (frame) {
                    frame.src = eventData.url;
                }
            });
        }
    },

    // Обработчик события приостановки приложения
    onPause: function() {
        // Что делать при переходе приложения в фоновый режим
        console.log("Приложение перешло в фоновый режим");
    },

    // Обработчик события возобновления приложения
    onResume: function() {
        // Что делать при возвращении приложения из фона
        console.log("Приложение вернулось из фонового режима");
        
        // Проверяем состояние сети
        if (this.checkNetworkState()) {
            // Обновление данных при необходимости
            const frame = document.getElementById('appFrame');
            if (frame && frame.contentWindow) {
                // Можно обновить содержимое
                frame.contentWindow.postMessage('app_resumed', '*');
            }
        }
    },
    
    // Обработчик потери соединения
    onOffline: function() {
        console.log("Соединение потеряно");
        this.showConnectionError();
        // Проверяем наличие кэша
        this.checkCachedContent();
    },
    
    // Обработчик восстановления соединения
    onOnline: function() {
        console.log("Соединение восстановлено");
        
        // Проверяем, есть ли действительно соединение
        if (this.checkNetworkState()) {
            const frame = document.getElementById('appFrame');
            const loadingEl = document.getElementById('loading');
            
            // Если iframe скрыт или отсутствует, попробуем перезагрузить приложение
            if (!frame || frame.style.display !== 'block') {
                // Если элемент загрузки отображается, перезагружаем страницу
                if (loadingEl && loadingEl.style.display === 'block') {
                    // Обновляем страницу
                    window.location.reload();
                }
            } else if (frame.contentWindow) {
                // Если iframe уже отображается, обновляем его содержимое
                frame.contentWindow.location.reload();
            }
        }
    },

    // Обработчик нажатия кнопки "назад"
    onBackButton: function() {
        const frame = document.getElementById('appFrame');
        
        if (frame && frame.style.display === 'block' && frame.contentWindow) {
            // Отправка сообщения в iframe
            frame.contentWindow.postMessage('backbutton', '*');
        } else {
            // Выходим из приложения, если мы на экране загрузки или ошибки
            if (navigator.app && navigator.app.exitApp) {
                navigator.app.exitApp();
            }
        }
    },

    // Отправка токена на сервер
    sendTokenToServer: function(token) {
        if (!this.checkNetworkState()) {
            console.log('Нет соединения, отправка токена отложена');
            
            // Сохраняем для последующей отправки
            localStorage.setItem('pendingToken', token);
            return;
        }
        
        // Получаем информацию об устройстве
        const deviceInfo = {
            uuid: device.uuid,
            platform: device.platform,
            version: device.version,
            manufacturer: device.manufacturer,
            model: device.model,
            token: token
        };
        
        // Отправляем на сервер
        fetch(this.config.appUrl + '/api/register-device', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(deviceInfo)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Устройство зарегистрировано: ', data);
            
            // Удаляем сохраненный токен
            localStorage.removeItem('pendingToken');
        })
        .catch(error => {
            console.error('Ошибка регистрации устройства: ', error);
        });
    },
    
    // Проверка и отправка отложенных данных
    checkPendingData: function() {
        // Проверка отложенного токена
        const pendingToken = localStorage.getItem('pendingToken');
        if (pendingToken) {
            this.sendTokenToServer(pendingToken);
        }
    }
};

// Инициализация приложения
App.initialize(); 