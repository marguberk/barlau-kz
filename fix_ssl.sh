#!/bin/bash

# Скрипт исправления SSL конфигурации для barlau.org

echo "=== Исправление SSL конфигурации для barlau.org ==="

# 1. Обновляем конфигурацию Nginx для работы только с barlau.org
echo "1. Обновляем конфигурацию Nginx..."

# Создаем временную конфигурацию только для barlau.org
sudo tee /etc/nginx/sites-available/barlau-temp > /dev/null << 'EOF'
server {
    listen 80;
    server_name barlau.org www.barlau.org;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/barlau/static/;
    }

    location /media/ {
        alias /var/www/barlau/media/;
    }

    # Для Let's Encrypt проверки
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
}
EOF

# 2. Активируем временную конфигурацию
sudo ln -sf /etc/nginx/sites-available/barlau-temp /etc/nginx/sites-enabled/barlau
sudo rm -f /etc/nginx/sites-enabled/default

# 3. Создаем директорию для Let's Encrypt
sudo mkdir -p /var/www/html/.well-known/acme-challenge/
sudo chown -R www-data:www-data /var/www/html/

# 4. Проверяем и перезагружаем Nginx
echo "2. Проверяем конфигурацию Nginx..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "3. Перезагружаем Nginx..."
    sudo systemctl reload nginx
    
    echo "4. Проверяем статус сервисов..."
    sudo systemctl status nginx --no-pager
    sudo systemctl status barlau --no-pager
    
    echo ""
    echo "=== Конфигурация обновлена! ==="
    echo ""
    echo "Теперь выполните команду для получения SSL сертификата:"
    echo "sudo certbot --nginx -d barlau.org -d www.barlau.org"
    echo ""
    echo "После получения SSL сертификата выполните:"
    echo "wget https://raw.githubusercontent.com/marguberk/barlau-kz/mobile-menu-refactor/nginx_barlau_fixed.conf"
    echo "sudo cp nginx_barlau_fixed.conf /etc/nginx/sites-available/barlau"
    echo "sudo systemctl reload nginx"
else
    echo "Ошибка в конфигурации Nginx!"
    exit 1
fi 