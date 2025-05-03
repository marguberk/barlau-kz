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
        
        // Инициализация модуля грузовиков (если находимся на странице trucks.html)
        this.initTrucksModule();
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

    // Настройка обработки deep links
    setupDeepLinks: function() {
        // Проверка наличия плагина для deep links
        if (window.universalLinks) {
            // Обработчик для проверки deep link при открытии приложения
            universalLinks.subscribe(null, function(eventData) {
                console.log('Deep link получен:', eventData.url);
                
                // Перенаправляем на соответствующую страницу
                // Например: если ссылка содержит "trucks", открываем страницу грузовиков
                if (eventData.url.includes('/trucks/')) {
                    // Получаем ID грузовика из URL
                    const truckId = eventData.url.split('/trucks/')[1].split('/')[0];
                    window.location.href = `trucks.html?id=${truckId}`;
                }
            });
        }
    },

    // Обработчик перехода приложения в фоновый режим
    onPause: function() {
        console.log('Приложение перешло в фоновый режим');
    },

    // Обработчик возвращения приложения из фонового режима
    onResume: function() {
        console.log('Приложение возобновлено');
        
        // Обновляем состояние сети при возвращении
        this.checkNetworkState();
    },

    // Обработчик нажатия кнопки "Назад" на Android
    onBackButton: function() {
        // Получаем текущий URL
        const currentPath = window.location.pathname;
        const fileName = currentPath.substring(currentPath.lastIndexOf('/') + 1);
        
        if (fileName === 'index.html' || fileName === '') {
            // Если мы на главной странице, подтверждаем выход
            if (confirm('Вы уверены, что хотите выйти из приложения?')) {
                navigator.app.exitApp();
            }
        } else {
            // Если мы на другой странице, просто возвращаемся назад
            window.history.back();
        }
    },

    // Обработчик события отключения от сети
    onOffline: function() {
        console.log('Устройство перешло в автономный режим');
        
        // Проверяем состояние
        this.checkNetworkState();
    },

    // Обработчик события подключения к сети
    onOnline: function() {
        console.log('Устройство снова в сети');
        
        // Проверяем состояние
        this.checkNetworkState();
    },
    
    // Инициализация модуля грузовиков
    initTrucksModule: function() {
        // Проверяем, находимся ли мы на странице trucks.html
        const currentPath = window.location.pathname;
        const fileName = currentPath.substring(currentPath.lastIndexOf('/') + 1);
        
        if (fileName === 'trucks.html') {
            // Проверяем, загружен ли скрипт модуля trucks.js
            if (typeof window.TrucksModule === 'undefined') {
                console.warn('Модуль TrucksModule не найден');
                return;
            }
            
            // Инициализируем демо-данные
            window.TrucksModule.initDemoData();
            
            // Настраиваем уведомления для документов
            setTimeout(function() {
                window.TrucksModule.setupDocumentNotifications();
            }, 5000); // Ждем 5 секунд перед установкой уведомлений
            
            console.log('Модуль грузовиков инициализирован');
        }
    }
};

// Инициализация приложения
App.initialize(); 