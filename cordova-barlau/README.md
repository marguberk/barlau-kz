# BARLAU.KZ Mobile App (Cordova)

Мобильное приложение для системы управления логистикой и сотрудниками BARLAU.KZ, созданное с использованием Apache Cordova.

## Описание

Это приложение представляет собой оболочку для веб-сайта BARLAU.KZ, предоставляющую следующие возможности:

- Полноэкранный просмотр веб-приложения без элементов браузера
- Доступ к нативным функциям устройства через плагины Cordova (геолокация, камера и т.д.)
- Возможность работы в офлайн-режиме и локальное кэширование
- Push-уведомления
- Интеграция с системой авторизации

## Предварительные требования

Для работы с проектом необходимо:

1. **Node.js и npm** (последние версии)
2. **Cordova CLI**:
   ```bash
   npm install -g cordova
   ```
3. **macOS** и **Xcode** (для сборки iOS-приложения)
4. **Аккаунт Apple Developer** (для публикации в App Store)

## Установка и запуск

### Клонирование и настройка проекта

```bash
# Клонирование репозитория
git clone https://github.com/yourusername/barlau-kz.git
cd barlau-kz/cordova-barlau

# Установка зависимостей
npm install

# Добавление платформы iOS
npm run prepare-ios
# или
cordova platform add ios
```

### Подготовка ресурсов

```bash
# Установка инструмента для генерации иконок и сплэш-экранов
npm install -g cordova-res

# Генерация ресурсов
npm run prepare-resources
# или
cordova-res ios --skip-config --copy
```

### Сборка и запуск

```bash
# Сборка для iOS
npm run build-ios
# или
cordova build ios

# Запуск в симуляторе
npm run emulate-ios
# или
cordova emulate ios

# Запуск на подключенном устройстве
npm run run-ios
# или
cordova run ios
```

## Структура проекта

```
cordova-barlau/
├── config.xml         # Конфигурация Cordova
├── package.json       # Зависимости и скрипты npm
├── www/               # Веб-приложение
│   ├── index.html     # Основной HTML-файл
│   ├── css/           # Стили
│   ├── js/            # JavaScript-файлы
│   │   └── app.js     # Основная логика приложения
│   └── img/           # Изображения
├── res/               # Ресурсы (иконки, сплэш-экраны)
│   └── ios/           # Ресурсы для iOS
└── platforms/         # Платформо-специфичный код (добавляется автоматически)
    └── ios/           # Проект Xcode для iOS
```

## Плагины

В проекте используются следующие плагины Cordova:

- `cordova-plugin-statusbar`: Управление статус-баром
- `cordova-plugin-splashscreen`: Управление сплэш-экраном
- `cordova-plugin-wkwebview-engine`: Использование WKWebView для лучшей производительности
- `cordova-plugin-inappbrowser`: Открытие ссылок во внешнем браузере
- `cordova-plugin-network-information`: Проверка состояния сети
- `cordova-plugin-geolocation`: Доступ к геолокации
- `cordova-plugin-device`: Информация об устройстве

## Публикация в App Store

Для публикации в App Store:

1. Создайте релизную сборку:
   ```bash
   cordova build ios --release
   ```

2. Откройте проект Xcode:
   ```bash
   open platforms/ios/BARLAU.xcworkspace
   ```

3. В Xcode настройте подписи, идентификаторы и сертификаты

4. Выберите "Product" -> "Archive" для создания архива

5. Следуйте инструкциям Xcode для валидации и загрузки в App Store Connect

6. Заполните информацию в App Store Connect и отправьте на проверку

## Контакты и поддержка

Для получения поддержки или дополнительной информации:

- Email: info@barlau.kz
- Веб-сайт: https://barlau.kz 