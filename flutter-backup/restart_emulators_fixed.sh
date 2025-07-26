#!/bin/bash

echo "🔄 УЛУЧШЕННЫЙ ПЕРЕЗАПУСК ЭМУЛЯТОРОВ С ДИАГНОСТИКОЙ"
echo "=================================================="
echo ""

# Остановка всех процессов
echo "🛑 Остановка всех Flutter приложений и эмуляторов..."
pkill -f "flutter.*run" 2>/dev/null || true
killall "Android Emulator" 2>/dev/null || true

# Остановка iOS симулятора
echo "📱 Остановка iOS симулятора..."
xcrun simctl shutdown all 2>/dev/null || true
pkill -f Simulator 2>/dev/null || true

echo ""

# Проверка доступных устройств
echo "🔍 Поиск доступных эмуляторов..."
flutter emulators

echo ""

# Запуск Android эмулятора
echo "🤖 Запуск Android эмулятора..."
flutter emulators --launch Pixel_7 &
ANDROID_PID=$!

# Запуск iOS симулятора
echo "📱 Запуск iOS симулятора..."
flutter emulators --launch apple_ios_simulator &
IOS_PID=$!

# Ждем запуска эмуляторов
echo "⏳ Ожидание запуска эмуляторов (60 секунд)..."
sleep 60

# Принудительный запуск iOS симулятора если не запустился
echo "🔧 Проверка и принудительный запуск iOS симулятора..."
IOS_STATUS=$(xcrun simctl list devices | grep "294C60FA-C0C4-48A2-A075-BA293F671E39" | grep -o "(.*)")
if [[ "$IOS_STATUS" == *"Shutdown"* ]]; then
    echo "   ⚠️  iOS симулятор не запустился, принудительный запуск..."
    xcrun simctl boot 294C60FA-C0C4-48A2-A075-BA293F671E39
    sleep 10
fi

# Проверка статуса устройств
echo ""
echo "📊 СТАТУС УСТРОЙСТВ:"
echo "-------------------"
flutter devices

echo ""

# Поиск ID устройств
echo "🔍 Поиск ID устройств..."
ANDROID_ID=$(flutter devices | grep "emulator-" | awk '{print $NF}' | tr -d '()')
IOS_ID=$(flutter devices | grep "294C60FA" | awk '{print $NF}' | tr -d '()')

echo "   Android: $ANDROID_ID"
echo "   iOS: $IOS_ID"

echo ""

# Запуск Flutter приложений
if [ ! -z "$ANDROID_ID" ]; then
    echo "🚀 Запуск Flutter приложения на Android ($ANDROID_ID)..."
    cd barlau_flutter
    flutter run -d "$ANDROID_ID" &
    FLUTTER_ANDROID_PID=$!
    echo "   Процесс Android: PID $FLUTTER_ANDROID_PID"
    cd ..
fi

if [ ! -z "$IOS_ID" ]; then
    echo "🚀 Запуск Flutter приложения на iOS ($IOS_ID)..."
    cd barlau_flutter
    flutter run -d "$IOS_ID" &
    FLUTTER_IOS_PID=$!
    echo "   Процесс iOS: PID $FLUTTER_IOS_PID"
    cd ..
fi

echo ""
echo "✅ Приложения запущены!"
echo ""

# Показать статус процессов
echo "📊 Статус процессов:"
ps aux | grep -E "flutter.*run" | grep -v grep | while read line; do
    echo "   $line"
done

echo ""
echo "🎯 Полезные команды:"
echo "   Просмотр логов Android: flutter logs -d $ANDROID_ID"
echo "   Просмотр логов iOS: flutter logs -d $IOS_ID"
echo "   Остановка всех: pkill -f 'flutter.*run'"
echo "   Hot reload: нажмите 'r' в терминале Flutter"
echo "   Hot restart: нажмите 'R' в терминале Flutter"

echo ""
echo "🎉 Скрипт завершен!" 