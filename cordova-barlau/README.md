# BARLAU.KZ Mobile App

Мобильное приложение для системы управления логистикой и сотрудниками BARLAU.KZ.

## Описание

Приложение представляет собой веб-приложение с нативной оболочкой, созданное с использованием Apache Cordova. Приложение предоставляет доступ к основным функциям системы BARLAU.KZ:

- Отслеживание местоположения транспорта
- Управление задачами и заказами
- Просмотр статистики и отчетов
- Управление профилем и настройками

## Требования для разработки

- Node.js и npm
- Apache Cordova
- Android SDK (для сборки Android приложения)
- Xcode (для сборки iOS приложения)
- JDK 11+ (для Android)

## Установка и настройка

1. Клонируйте репозиторий:

```bash
git clone <repository-url>
cd cordova-barlau
```

2. Установите зависимости:

```bash
npm install
```

3. Добавьте платформы:

```bash
cordova platform add android
cordova platform add ios
```

## Генерация ресурсов

Для создания иконок и заставок для приложения используйте следующие скрипты:

1. Сначала установите требуемые зависимости:

```bash
npm install canvas sharp
```

2. Сгенерируйте базовые изображения:

```bash
node create-base-images.js
```

3. Сгенерируйте иконки и заставки всех размеров:

```bash
node generate-icons.js
```

## Сборка приложения

### Android

Для сборки Android приложения запустите скрипт:

```bash
./build-android.sh
```

Скрипт создаст отладочную и релизную версии приложения. После успешной сборки вы можете установить отладочную версию на подключенное устройство.

### iOS

Для сборки iOS приложения запустите скрипт:

```bash
./build-ios.sh
```

Скрипт скопирует все необходимые ресурсы и соберет проект. После успешной сборки вы можете открыть проект в Xcode для дальнейшей настройки и подписи.

## Структура проекта

- `www/` - Основной веб-контент приложения
- `res/` - Ресурсы приложения (иконки, заставки)
- `platforms/` - Платформо-зависимый код
- `plugins/` - Плагины Cordova
- `config.xml` - Конфигурация Cordova

## Плагины

Приложение использует следующие плагины Cordova:

- `cordova-plugin-statusbar` - Управление статус-баром
- `cordova-plugin-splashscreen` - Управление заставкой
- `cordova-plugin-inappbrowser` - Встроенный браузер
- `cordova-plugin-network-information` - Информация о сетевом подключении
- `cordova-plugin-geolocation` - Геолокация
- `cordova-plugin-device` - Информация об устройстве

## Публикация

### Android

Для подготовки релизной версии Android приложения:

1. Создайте keystore для подписи (если его еще нет):

```bash
keytool -genkey -v -keystore barlau-release-key.keystore -alias barlau -keyalg RSA -keysize 2048 -validity 10000
```

2. Подпишите APK:

```bash
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore barlau-release-key.keystore platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk barlau
```

3. Оптимизируйте APK:

```bash
zipalign -v 4 platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk barlau.apk
```

### iOS

Для публикации iOS приложения:

1. Откройте проект в Xcode:

```bash
open platforms/ios/BARLAU.KZ.xcworkspace
```

2. Настройте подписывание приложения и App Store Connect
3. Выполните архивацию проекта в Xcode
4. Отправьте архив в App Store Connect

## Лицензия

© 2024 BARLAU.KZ. Все права защищены. 