/**
 * BARLAU.KZ Mobile App
 * Файл для взаимодействия с нативными плагинами Cordova
 */

// Объект для хранения методов приложения
const App = {
    // Инициализация приложения
    initialize: function() {
        document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
    },

    // Обработчик события готовности устройства
    onDeviceReady: function() {
        // Инициализация функциональности приложения
        this.setupStatusBar();
        this.setupGeolocation();
        this.setupNotifications();
        this.setupDeepLinks();
        
        // Подписка на события жизненного цикла приложения
        document.addEventListener("pause", this.onPause.bind(this), false);
        document.addEventListener("resume", this.onResume.bind(this), false);
        document.addEventListener("backbutton", this.onBackButton.bind(this), false);
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
                    frame.src = data.additionalData.url;
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
                frame.src = eventData.url;
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
        
        // Обновление данных при необходимости
        const frame = document.getElementById('appFrame');
        
        // Проверка соединения перед обновлением
        if (navigator.connection && navigator.connection.type !== Connection.NONE) {
            // Можно обновить содержимое
            frame.contentWindow.postMessage('app_resumed', '*');
        }
    },

    // Обработчик нажатия кнопки "назад"
    onBackButton: function() {
        const frame = document.getElementById('appFrame');
        
        // Отправка сообщения в iframe
        frame.contentWindow.postMessage('backbutton', '*');
        
        // Также можно добавить навигацию назад в истории iframe
        // или выход из приложения при нахождении на главной странице
    },

    // Отправка токена на сервер
    sendTokenToServer: function(token) {
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
        fetch('https://barlau.kz/api/register-device', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(deviceInfo)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Устройство зарегистрировано: ', data);
        })
        .catch(error => {
            console.error('Ошибка регистрации устройства: ', error);
        });
    }
};

// Инициализация приложения
App.initialize(); 