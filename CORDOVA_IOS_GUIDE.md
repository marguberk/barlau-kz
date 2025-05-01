# Руководство по созданию iOS-приложения с Apache Cordova

В этом руководстве описан процесс создания iOS-приложения для веб-сайта BARLAU.KZ с использованием фреймворка Apache Cordova (ранее PhoneGap).

## Преимущества Apache Cordova

- **Открытый исходный код**: Cordova - это бесплатное решение с открытым исходным кодом
- **Кросс-платформенность**: один код для Android и iOS
- **Большое сообщество**: множество плагинов и документации
- **Гибкость**: возможность использования нативных API через плагины
- **Доступность**: не требует платной подписки

## Предварительные требования

1. **Для разработки iOS-приложения**:
   - Mac с macOS 10.15+
   - Xcode 12+ (установить из App Store)
   - Аккаунт Apple Developer ($99/год)
   - Node.js и npm (последние версии)

2. **Установка Cordova**:
   ```bash
   npm install -g cordova
   ```

## Шаг 1: Создание проекта Cordova

1. **Создайте новый проект Cordova**:
   ```bash
   cordova create cordova-barlau kz.barlau.app BARLAU
   cd cordova-barlau
   ```

2. **Добавьте платформу iOS**:
   ```bash
   cordova platform add ios
   ```

## Шаг 2: Настройка проекта для веб-приложения

1. **Откройте файл `config.xml`** в корне проекта и настройте основные параметры:

   ```xml
   <widget id="kz.barlau.app" version="1.0.0" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
       <name>BARLAU.KZ</name>
       <description>Система управления логистикой и сотрудниками</description>
       <author email="info@barlau.kz" href="https://barlau.kz">BARLAU Team</author>
       <content src="index.html" />
       
       <preference name="DisallowOverscroll" value="true" />
       <preference name="BackupWebStorage" value="local" />
       <preference name="StatusBarOverlaysWebView" value="false" />
       <preference name="StatusBarBackgroundColor" value="#2563EB" />
       <preference name="StatusBarStyle" value="lightcontent" />
       <preference name="Orientation" value="portrait" />
       <preference name="target-device" value="universal" />
       <preference name="deployment-target" value="12.0" />
       <preference name="EnableViewportScale" value="true" />
       <preference name="MediaTypesRequiringUserActionForPlayback" value="none" />
       <preference name="AllowInlineMediaPlayback" value="true" />
       
       <access origin="*" />
       <allow-intent href="http://*/*" />
       <allow-intent href="https://*/*" />
       <allow-intent href="tel:*" />
       <allow-intent href="sms:*" />
       <allow-intent href="mailto:*" />
       <allow-intent href="geo:*" />
       
       <platform name="ios">
           <allow-intent href="itms:*" />
           <allow-intent href="itms-apps:*" />
           <preference name="WKWebViewOnly" value="true" />
           <feature name="CDVWKWebViewEngine">
               <param name="ios-package" value="CDVWKWebViewEngine" />
           </feature>
           <preference name="CordovaWebViewEngine" value="CDVWKWebViewEngine" />
       </platform>
       
       <!-- Настройки иконок для iOS -->
       <platform name="ios">
           <icon src="res/ios/icon-20.png" width="20" height="20" />
           <icon src="res/ios/icon-20@2x.png" width="40" height="40" />
           <icon src="res/ios/icon-20@3x.png" width="60" height="60" />
           <icon src="res/ios/icon-29.png" width="29" height="29" />
           <icon src="res/ios/icon-29@2x.png" width="58" height="58" />
           <icon src="res/ios/icon-29@3x.png" width="87" height="87" />
           <icon src="res/ios/icon-40.png" width="40" height="40" />
           <icon src="res/ios/icon-40@2x.png" width="80" height="80" />
           <icon src="res/ios/icon-40@3x.png" width="120" height="120" />
           <icon src="res/ios/icon-60@2x.png" width="120" height="120" />
           <icon src="res/ios/icon-60@3x.png" width="180" height="180" />
           <icon src="res/ios/icon-76.png" width="76" height="76" />
           <icon src="res/ios/icon-76@2x.png" width="152" height="152" />
           <icon src="res/ios/icon-83.5@2x.png" width="167" height="167" />
           <icon src="res/ios/icon-1024.png" width="1024" height="1024" />
       </platform>
       
       <!-- Настройки сплэш-экрана для iOS -->
       <platform name="ios">
           <splash src="res/ios/splash-Default@2x~iphone.png" width="640" height="960" />
           <splash src="res/ios/splash-Default-568h@2x~iphone.png" width="640" height="1136" />
           <splash src="res/ios/splash-Default-667h.png" width="750" height="1334" />
           <splash src="res/ios/splash-Default-736h.png" width="1242" height="2208" />
           <splash src="res/ios/splash-Default-Landscape-736h.png" width="2208" height="1242" />
           <splash src="res/ios/splash-Default-Portrait~ipad.png" width="768" height="1024" />
           <splash src="res/ios/splash-Default-Landscape~ipad.png" width="1024" height="768" />
           <splash src="res/ios/splash-Default-Portrait@2x~ipad.png" width="1536" height="2048" />
           <splash src="res/ios/splash-Default-Landscape@2x~ipad.png" width="2048" height="1536" />
           <splash src="res/ios/splash-1125x2436.png" width="1125" height="2436" />
           <splash src="res/ios/splash-2436x1125.png" width="2436" height="1125" />
       </platform>
   </widget>
   ```

2. **Настройте index.html для загрузки вашего веб-приложения**:
   
   Создайте или отредактируйте файл `www/index.html`:

   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <meta charset="utf-8">
       <meta name="viewport" content="initial-scale=1, width=device-width, viewport-fit=cover, user-scalable=no">
       <meta http-equiv="Content-Security-Policy" content="default-src * data: gap: https://ssl.gstatic.com 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; media-src *; connect-src *">
       <title>BARLAU.KZ</title>
       <style>
           body, html {
               margin: 0;
               padding: 0;
               height: 100%;
               width: 100%;
               overflow: hidden;
           }
           #appFrame {
               border: none;
               height: 100%;
               width: 100%;
               position: absolute;
               top: 0;
               left: 0;
               right: 0;
               bottom: 0;
           }
           .app-loading {
               position: absolute;
               top: 0;
               left: 0;
               right: 0;
               bottom: 0;
               background: #ffffff;
               display: flex;
               justify-content: center;
               align-items: center;
               flex-direction: column;
           }
           .app-loading img {
               width: 120px;
               height: 120px;
           }
           .app-loading h1 {
               margin-top: 20px;
               font-family: Arial, sans-serif;
               color: #2563EB;
           }
           .spinner {
               width: 40px;
               height: 40px;
               margin: 20px auto;
               background-color: #2563EB;
               border-radius: 100%;  
               -webkit-animation: sk-scaleout 1.0s infinite ease-in-out;
               animation: sk-scaleout 1.0s infinite ease-in-out;
           }
           @-webkit-keyframes sk-scaleout {
               0% { -webkit-transform: scale(0) }
               100% { -webkit-transform: scale(1.0); opacity: 0; }
           }
           @keyframes sk-scaleout {
               0% { transform: scale(0); -webkit-transform: scale(0); }
               100% { transform: scale(1.0); -webkit-transform: scale(1.0); opacity: 0; }
           }
       </style>
   </head>
   <body>
       <div class="app-loading" id="loading">
           <img src="img/logo.png" alt="BARLAU.KZ">
           <h1>BARLAU.KZ</h1>
           <div class="spinner"></div>
       </div>
       <iframe id="appFrame" style="display:none;"></iframe>
       
       <script type="text/javascript" src="cordova.js"></script>
       <script>
           document.addEventListener('deviceready', onDeviceReady, false);
           
           function onDeviceReady() {
               // Обработка события возврата кнопкой "назад" на Android
               document.addEventListener("backbutton", onBackKeyDown, false);
               
               const frame = document.getElementById('appFrame');
               const loadingEl = document.getElementById('loading');
               
               // Загрузка веб-приложения
               frame.src = 'https://barlau.kz';
               
               // События iframe
               frame.onload = function() {
                   // Скрываем загрузку, показываем iframe
                   loadingEl.style.display = 'none';
                   frame.style.display = 'block';
                   
                   // Попытка автоматического входа, если сохранены учетные данные
                   tryAutoLogin();
               };
               
               // Проверка на наличие сети
               document.addEventListener("offline", onOffline, false);
               document.addEventListener("online", onOnline, false);
           }
           
           function onBackKeyDown() {
               const frame = document.getElementById('appFrame');
               // Отправляем событие нажатия кнопки "назад" в веб-приложение
               frame.contentWindow.postMessage('backbutton', '*');
           }
           
           function onOffline() {
               // Показать сообщение об отсутствии соединения
               alert("Отсутствует подключение к интернету. Некоторые функции могут быть недоступны.");
           }
           
           function onOnline() {
               // Восстановление соединения
               const frame = document.getElementById('appFrame');
               frame.contentWindow.location.reload();
           }
           
           function tryAutoLogin() {
               // Здесь можно добавить код для автоматического входа
               // например, используя сохраненные в localStorage учетные данные
           }
       </script>
   </body>
   </html>
   ```

3. **Добавьте папку с изображениями**:
   ```bash
   mkdir -p www/img
   ```

## Шаг 3: Добавление необходимых плагинов

Установите полезные плагины для улучшения функциональности:

```bash
# Базовые плагины
cordova plugin add cordova-plugin-statusbar
cordova plugin add cordova-plugin-splashscreen
cordova plugin add cordova-plugin-wkwebview-engine
cordova plugin add cordova-plugin-inappbrowser
cordova plugin add cordova-plugin-network-information

# Дополнительные плагины
cordova plugin add cordova-plugin-geolocation
cordova plugin add cordova-plugin-camera
cordova plugin add cordova-plugin-file
cordova plugin add cordova-plugin-device
```

## Шаг 4: Подготовка ресурсов

1. **Создайте папки для ресурсов**:
   ```bash
   mkdir -p res/ios
   ```

2. **Подготовьте иконки и сплэш-экраны** согласно спецификациям в файле config.xml
   
   Вы можете воспользоваться инструментами для автоматической генерации из одного изображения:
   ```bash
   npm install -g cordova-res
   cordova-res ios --skip-config --copy
   ```

## Шаг 5: Сборка и тестирование

1. **Проверьте, что все требования для сборки выполнены**:
   ```bash
   cordova requirements ios
   ```

2. **Создайте отладочную сборку**:
   ```bash
   cordova build ios
   ```

3. **Откройте проект в Xcode**:
   ```bash
   open platforms/ios/BARLAU.xcworkspace
   ```

4. **В Xcode**:
   - Настройте учетную запись разработчика Apple
   - Выберите целевое устройство (iPhone или симулятор)
   - Нажмите кнопку "Run" для сборки и запуска

## Шаг 6: Подготовка к публикации

1. **Создайте релизную сборку**:
   ```bash
   cordova build ios --release
   ```

2. **В Xcode**:
   - Выберите "Product" -> "Archive"
   - Следуйте инструкциям для валидации и загрузки в App Store Connect
   
3. **В App Store Connect**:
   - Заполните информацию о приложении
   - Загрузите скриншоты и метаданные
   - Отправьте на проверку Apple

## Шаг 7: Обновление приложения

Для обновления приложения:

1. **Содержимое веб-приложения**: обновляется автоматически, так как загружается с сервера
2. **Оболочка Cordova**: требует обновления версии в config.xml и публикации новой версии в App Store:
   ```xml
   <widget id="kz.barlau.app" version="1.0.1" ...>
   ```

## Полезные советы

1. **Для отладки**:
   - В Safari: Preferences -> Advanced -> Show Develop menu
   - В Develop меню выберите iOS Simulator или устройство для доступа к веб-инспектору

2. **Для улучшения производительности**:
   - Используйте WKWebView вместо устаревшего UIWebView
   - Оптимизируйте загрузку веб-страницы
   - Используйте локальный кэш для часто используемых ресурсов

3. **Для соответствия правилам App Store**:
   - Убедитесь, что ваше приложение предоставляет нативную функциональность, а не просто отображает веб-сайт
   - Добавьте интеграцию с нативными API через плагины Cordova
   - Обеспечьте хороший пользовательский опыт даже при отсутствии интернет-соединения

## Сравнение с GoNative.io и WebViewGold

| Аспект | Cordova | GoNative.io | WebViewGold |
|--------|---------|-------------|-------------|
| Стоимость | Бесплатно | $79-990 | $40-60 |
| Открытый исходный код | Да | Нет | Нет |
| Кастомизация | Высокая | Средняя | Низкая |
| Сложность настройки | Средняя | Низкая | Низкая |
| Доступ к нативным API | Широкий | Ограниченный | Ограниченный |
| Обновления | Ручные | Автоматические | Ручные |
| Сообщество разработчиков | Большое | Малое | Малое |

## Заключение

Apache Cordova предоставляет мощный и гибкий способ создания iOS-приложения для BARLAU.KZ без лицензионных платежей. Хотя настройка требует больше усилий по сравнению с GoNative.io или WebViewGold, она предлагает более высокую степень контроля и возможность расширения функциональности через разнообразные плагины. 