#!/bin/bash

# Путь к Django проекту
DJANGO_PROJECT_PATH="/var/www/barlau"

# Путь к виртуальному окружению
VENV_PATH="$DJANGO_PROJECT_PATH/venv"

# Путь к скрипту синхронизации
SYNC_SCRIPT_PATH="/home/ubuntu/auto_sync_stavtrack.py"

# Файл для хранения PID
PID_FILE="/home/ubuntu/stavtrack_auto_sync.pid"

# Файл для логов
LOG_FILE="/home/ubuntu/stavtrack_auto_sync.log"

echo "🚀 Запуск автоматической синхронизации StavTrack GPS..."

# Проверяем, запущен ли уже процесс
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
        echo "⚠️ Процесс уже запущен с PID: $PID. Остановите его вручную, если нужно."
        exit 1
    else
        echo "ℹ️ Обнаружен старый PID файл, но процесс не запущен. Удаляем старый PID файл."
        rm "$PID_FILE"
    fi
fi

# Запускаем скрипт в фоновом режиме
cd "$DJANGO_PROJECT_PATH" && source "$VENV_PATH/bin/activate" && \
PYTHONPATH="$DJANGO_PROJECT_PATH" nohup python3 "$SYNC_SCRIPT_PATH" > "$LOG_FILE" 2>&1 &

# Сохраняем PID
echo $! > "$PID_FILE"

echo "✅ Автоматическая синхронизация StavTrack запущена с PID: $(cat "$PID_FILE")"
echo "📝 Логи: $LOG_FILE"
echo "🛑 Для остановки: kill $(cat "$PID_FILE")"


