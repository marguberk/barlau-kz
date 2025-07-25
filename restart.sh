#!/bin/bash

# Быстрый перезапуск Flutter приложений
echo "🔄 Быстрый перезапуск..."

# Убиваем все Flutter процессы
pkill -f "flutter.*run" 2>/dev/null

# Переходим в Flutter проект
cd barlau_flutter

# Запускаем на Android и iOS в фоновом режиме
flutter run -d emulator-5554 &
flutter run -d 294C60FA-C0C4-48A2-A075-BA293F671E39 &

echo "✅ Приложения запущены в фоновом режиме"
echo "📊 Активные Flutter процессы:"
sleep 3
ps aux | grep -E "flutter.*run" | grep -v grep 