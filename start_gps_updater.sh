#!/bin/bash
# Скрипт для запуска автоматического обновления GPS данных

echo "🛰️ Запуск автоматического обновления GPS данных..."

cd /var/www/barlau
source venv/bin/activate
export PYTHONPATH=/var/www/barlau

# Запускаем скрипт в фоновом режиме
nohup python3 /home/ubuntu/auto_gps_updater.py > /home/ubuntu/gps_updater.log 2>&1 &
echo $! > /home/ubuntu/gps_updater.pid

echo "✅ GPS обновлятор запущен с PID: $(cat /home/ubuntu/gps_updater.pid)"
echo "📝 Логи: /home/ubuntu/gps_updater.log"
echo "🛑 Для остановки: kill $(cat /home/ubuntu/gps_updater.pid)"


