#!/bin/bash

echo "🔄 ПРАВИЛЬНЫЙ ПЕРЕЗАПУСК FLUTTER ПРИЛОЖЕНИЙ"
echo "========================================"

# Остановка всех процессов Flutter
echo "🛑 Остановка всех Flutter процессов..."
pkill -f 'flutter.*run'
sleep 2

# Переход в папку проекта
cd barlau_flutter

# Полная очистка кэшей
echo "🧹 Очистка кэшей Flutter..."
flutter clean

# Восстановление зависимостей
echo "📦 Восстановление зависимостей..."
flutter pub get

# Проверка доступных устройств
echo "📱 Проверка доступных устройств..."
flutter devices

# Запуск на Android эмуляторе в фоне
echo "🤖 Запуск Android приложения..."
flutter run -d emulator-5554 &
ANDROID_PID=$!

# Ожидание перед запуском iOS
sleep 5

# Запуск на iOS симуляторе в фоне  
echo "📱 Запуск iOS приложения..."
flutter run -d 350BB8E1-7D11-42D8-9F31-E1E1C38A9957 &
IOS_PID=$!

echo ""
echo "✅ Приложения запускаются..."
echo "   Android PID: $ANDROID_PID"
echo "   iOS PID: $IOS_PID"
echo ""
echo "🔍 Ожидайте полной загрузки (30-60 секунд)"
echo "📊 Проверьте в эмуляторах раздел 'Сотрудники'"
echo ""
echo "🛠️ Полезные команды:"
echo "   Проверить процессы: ps aux | grep flutter | grep run"
echo "   Остановить все: pkill -f 'flutter.*run'"
echo "   Логи Android: flutter logs -d emulator-5554"
echo "   Логи iOS: flutter logs -d 350BB8E1-7D11-42D8-9F31-E1E1C38A9957"
echo ""
echo "🎯 Ожидаемый результат:"
echo "   ✅ Загрузка реальных данных с barlau.org ИЛИ"
echo "   ✅ Демо данные (3 сотрудника) если сервер недоступен"
echo "   ❌ НЕ должно быть ошибки HTTP 404" 