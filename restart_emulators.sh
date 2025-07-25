#!/bin/bash

# Скрипт для перезагрузки Flutter приложений на iOS и Android эмуляторах
# Использование: ./restart_emulators.sh

echo "🔄 Перезагрузка Flutter приложений на эмуляторах..."

# Остановка всех Flutter процессов
echo "🛑 Остановка всех Flutter процессов..."
pkill -f "flutter.*run" 2>/dev/null
pkill -f "flutter.*emulator" 2>/dev/null
pkill -f "flutter.*iPhone" 2>/dev/null
pkill -f "flutter.*simulator" 2>/dev/null

# Ждем завершения процессов
sleep 3

# Переход в директорию Flutter проекта
cd barlau_flutter || {
    echo "❌ Ошибка: директория barlau_flutter не найдена"
    exit 1
}

# Проверка доступных устройств
echo "📱 Проверка доступных устройств..."
flutter devices

# Запуск iOS симулятора если не запущен
echo "📱 Запуск iOS симулятора..."
if ! xcrun simctl list devices | grep -q "Booted"; then
    xcrun simctl boot "iPhone 16 Pro" 2>/dev/null || echo "⚠️  iOS симулятор уже запущен"
    sleep 5
fi

# Запуск Android эмулятора если не запущен  
echo "🤖 Проверка Android эмулятора..."
if ! flutter devices | grep -q "emulator-"; then
    echo "🤖 Запуск Android эмулятора Pixel_7..."
    flutter emulators --launch Pixel_7 2>/dev/null &
    sleep 10
fi

# Получение ID устройств
echo "🔍 Поиск ID устройств..."
ANDROID_ID=$(flutter devices | grep "emulator-" | head -1 | grep -o "emulator-[0-9]*" | head -1)
IOS_ID=$(flutter devices | grep "iPhone" | grep "simulator" | head -1 | grep -o "[A-Z0-9-]\{36\}" | head -1)

echo "📱 Найденные устройства:"
echo "   Android: $ANDROID_ID"
echo "   iOS: $IOS_ID"

# Функция для запуска Flutter приложения
launch_flutter() {
    local device_id=$1
    local device_name=$2
    
    if [ -n "$device_id" ]; then
        echo "🚀 Запуск Flutter приложения на $device_name ($device_id)..."
        flutter run -d "$device_id" &
        local pid=$!
        echo "   Процесс $device_name: PID $pid"
        sleep 5
    else
        echo "❌ $device_name не найден"
    fi
}

# Запуск приложений
if [ -n "$ANDROID_ID" ] || [ -n "$IOS_ID" ]; then
    echo ""
    echo "🚀 Запуск Flutter приложений..."
    
    # Запуск на Android
    launch_flutter "$ANDROID_ID" "Android"
    
    # Запуск на iOS  
    launch_flutter "$IOS_ID" "iOS"
    
    echo ""
    echo "✅ Приложения запущены!"
    echo ""
    echo "📊 Статус процессов:"
    ps aux | grep -E "flutter.*run.*emulator|flutter.*run.*iPhone" | grep -v grep
    
    echo ""
    echo "🎯 Полезные команды:"
    echo "   Просмотр логов Android: flutter logs -d $ANDROID_ID"
    echo "   Просмотр логов iOS: flutter logs -d $IOS_ID"
    echo "   Остановка всех: pkill -f 'flutter.*run'"
    echo "   Hot reload: нажмите 'r' в терминале Flutter"
    echo "   Hot restart: нажмите 'R' в терминале Flutter"
    
else
    echo "❌ Не найдено ни одного эмулятора"
    echo "   Попробуйте:"
    echo "   - flutter emulators"
    echo "   - flutter emulators --launch Pixel_7"
    echo "   - open -a Simulator"
fi

echo ""
echo "🎉 Скрипт завершен!" 