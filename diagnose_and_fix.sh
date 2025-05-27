#!/bin/bash

# Скрипт диагностики и исправления Django приложения

echo "=== Диагностика Django приложения Barlau.kz ==="

# 1. Проверяем статус сервисов
echo "1. Проверяем статус сервисов..."
echo "--- Статус Django (barlau) ---"
sudo systemctl status barlau --no-pager

echo ""
echo "--- Статус Nginx ---"
sudo systemctl status nginx --no-pager

echo ""
echo "--- Статус MySQL ---"
sudo systemctl status mysql --no-pager

# 2. Проверяем сетевые подключения
echo ""
echo "2. Проверяем сетевые подключения..."
echo "--- Порт 8000 (Django/Gunicorn) ---"
netstat -tulpn | grep :8000 || echo "Порт 8000 не слушается!"

echo ""
echo "--- Порт 80 (HTTP) ---"
netstat -tulpn | grep :80

echo ""
echo "--- Порт 443 (HTTPS) ---"
netstat -tulpn | grep :443

# 3. Проверяем логи Django
echo ""
echo "3. Проверяем логи Django..."
echo "--- Последние 10 строк логов Django ---"
sudo journalctl -u barlau -n 10 --no-pager

# 4. Проверяем конфигурацию Nginx
echo ""
echo "4. Проверяем конфигурацию Nginx..."
sudo nginx -t

# 5. Проверяем файлы проекта
echo ""
echo "5. Проверяем файлы проекта..."
echo "--- Содержимое /var/www/barlau ---"
ls -la /var/www/barlau/

echo ""
echo "--- Проверяем .env файл ---"
if [ -f /var/www/barlau/.env ]; then
    echo ".env файл существует"
    echo "Содержимое (без паролей):"
    grep -v PASSWORD /var/www/barlau/.env
else
    echo ".env файл НЕ НАЙДЕН!"
fi

echo ""
echo "--- Проверяем виртуальное окружение ---"
if [ -d /var/www/barlau/venv ]; then
    echo "Виртуальное окружение существует"
    ls -la /var/www/barlau/venv/bin/
else
    echo "Виртуальное окружение НЕ НАЙДЕНО!"
fi

# 6. Попытка исправления
echo ""
echo "6. Попытка исправления проблем..."

# Проверяем и создаем пользователя barlau если нужно
if ! id "barlau" &>/dev/null; then
    echo "Создаем пользователя barlau..."
    sudo adduser --system --group --home /var/www/barlau barlau
fi

# Проверяем права доступа
echo "Исправляем права доступа..."
sudo chown -R barlau:barlau /var/www/barlau
sudo chown -R barlau:barlau /var/log/barlau

# Если Django не запущен, пытаемся запустить
if ! systemctl is-active --quiet barlau; then
    echo "Django не запущен. Пытаемся запустить..."
    
    # Проверяем что проект существует
    if [ -f /var/www/barlau/manage.py ]; then
        echo "Проект Django найден. Запускаем сервис..."
        sudo systemctl start barlau
        sleep 3
        sudo systemctl status barlau --no-pager
    else
        echo "ПРОЕКТ DJANGO НЕ НАЙДЕН! Нужно выполнить деплой."
        echo "Выполните команды:"
        echo "cd /var/www/barlau"
        echo "sudo -u barlau git clone https://github.com/marguberk/barlau-kz.git ."
        echo "sudo -u barlau python3 -m venv venv"
        echo "sudo -u barlau bash -c 'source venv/bin/activate && pip install -r requirements.txt'"
    fi
fi

# 7. Финальная проверка
echo ""
echo "7. Финальная проверка..."
echo "--- Статус после исправлений ---"
sudo systemctl status barlau --no-pager

echo ""
echo "--- Проверка порта 8000 ---"
netstat -tulpn | grep :8000 || echo "Django все еще не слушает порт 8000"

echo ""
echo "=== Диагностика завершена ==="
echo ""
echo "Если проблемы остались, проверьте:"
echo "1. Логи Django: sudo journalctl -u barlau -f"
echo "2. Логи Nginx: sudo tail -f /var/log/nginx/error.log"
echo "3. Тест Django вручную: sudo -u barlau bash -c 'cd /var/www/barlau && source venv/bin/activate && python manage.py runserver 0.0.0.0:8000'" 