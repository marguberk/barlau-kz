#!/bin/bash

# Скрипт для настройки iOS-проекта Cordova для BARLAU.KZ
# Этот скрипт выполняет все необходимые шаги для подготовки проекта к сборке

echo "=== Начало настройки iOS-проекта Cordova для BARLAU.KZ ==="

# Проверка наличия необходимых инструментов
echo "Проверка наличия Node.js и npm..."
if ! command -v node &> /dev/null; then
    echo "Node.js не найден. Пожалуйста, установите Node.js с https://nodejs.org/"
    exit 1
fi

echo "Проверка наличия Cordova..."
if ! command -v cordova &> /dev/null; then
    echo "Cordova не найдена. Установка Cordova..."
    npm install -g cordova
else
    echo "Cordova найдена: $(cordova -v)"
fi

echo "Проверка наличия cordova-res..."
if ! command -v cordova-res &> /dev/null; then
    echo "cordova-res не найден. Установка cordova-res..."
    npm install -g cordova-res
else
    echo "cordova-res найден"
fi

# Установка зависимостей проекта
echo "Установка зависимостей проекта..."
npm install

# Проверка наличия платформы iOS
echo "Проверка наличия платформы iOS..."
if ! cordova platform ls | grep -q "ios"; then
    echo "Платформа iOS не добавлена. Добавление платформы iOS..."
    cordova platform add ios
else
    echo "Платформа iOS уже добавлена."
    echo "Обновление платформы iOS до последней версии..."
    cordova platform update ios
fi

# Добавление плагинов
echo "Установка необходимых плагинов..."
cordova plugin add cordova-plugin-statusbar
cordova plugin add cordova-plugin-splashscreen
cordova plugin add cordova-plugin-wkwebview-engine
cordova plugin add cordova-plugin-inappbrowser
cordova plugin add cordova-plugin-network-information
cordova plugin add cordova-plugin-geolocation
cordova plugin add cordova-plugin-device

# Создание ресурсов
echo "Проверка наличия изображений для ресурсов..."
if [ ! -f "www/img/logo.png" ]; then
    echo "ВНИМАНИЕ: Файл www/img/logo.png не найден."
    echo "Для генерации иконок и сплэш-экранов необходимо поместить файл logo.png (1024x1024) в директорию www/img/"
    echo "После добавления файла запустите команду: cordova-res ios --skip-config --copy"
else
    echo "Генерация ресурсов (иконки, сплэш-экраны)..."
    cordova-res ios --skip-config --copy
fi

# Проверка требований
echo "Проверка требований для сборки iOS-приложения..."
cordova requirements ios

# Создание отладочной сборки
echo "Создание отладочной сборки..."
cordova build ios

echo "=== Настройка iOS-проекта завершена ==="
echo ""
echo "Следующие шаги:"
echo "1. Откройте проект в Xcode: open platforms/ios/BARLAU.xcworkspace"
echo "2. Настройте учетную запись разработчика и подписи в Xcode"
echo "3. Запустите приложение на симуляторе или устройстве"
echo ""
echo "Для создания релизной сборки выполните: cordova build ios --release"
echo "Для публикации в App Store следуйте инструкциям в CORDOVA_BUILD_GUIDE.md" 
 