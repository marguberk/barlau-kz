#!/bin/bash

# Скрипт для сборки APK BARLAU Mobile
echo "🚛 Начинаем сборку APK для BARLAU Mobile..."

# Установка переменных окружения
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export ANDROID_HOME=/opt/homebrew/share/android-commandlinetools

echo "✅ JAVA_HOME: $JAVA_HOME"
echo "✅ ANDROID_HOME: $ANDROID_HOME"

# Переход в папку android
cd android

echo "🔧 Очистка предыдущих сборок..."
./gradlew clean

echo "🏗️ Сборка debug APK..."
./gradlew assembleDebug

if [ $? -eq 0 ]; then
    echo "🎉 Сборка завершена успешно!"
    echo "📱 APK файл находится в: app/build/outputs/apk/debug/"
    ls -la app/build/outputs/apk/debug/
else
    echo "❌ Ошибка при сборке APK"
    exit 1
fi

echo "✅ Готово! Можете установить APK на устройство." 