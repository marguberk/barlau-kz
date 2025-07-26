#!/bin/bash

# Остановка всех Flutter приложений и эмуляторов
echo "🛑 Остановка всех Flutter приложений и эмуляторов..."

# Остановка Flutter процессов
echo "🔴 Остановка Flutter процессов..."
pkill -f "flutter.*run" 2>/dev/null
pkill -f "flutter.*emulator" 2>/dev/null  
pkill -f "flutter.*iPhone" 2>/dev/null
pkill -f "flutter.*simulator" 2>/dev/null

# Остановка Android эмуляторов
echo "🤖 Остановка Android эмулятора..."
adb emu kill 2>/dev/null

# Остановка iOS симуляторов
echo "📱 Остановка iOS симулятора..."
xcrun simctl shutdown all 2>/dev/null

sleep 2

echo "✅ Все эмуляторы остановлены"
echo "📊 Оставшиеся Flutter процессы:"
ps aux | grep flutter | grep -v grep || echo "   Нет активных Flutter процессов" 