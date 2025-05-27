#!/bin/bash

# Скрипт настройки сервисов для Django проекта Barlau.kz

echo "=== Настройка сервисов для Barlau.kz ==="

# 1. Копируем конфигурационные файлы
echo "1. Копируем конфигурационные файлы..."

# Копируем конфигурацию Gunicorn
sudo cp gunicorn_config.py /var/www/barlau/
sudo chown barlau:barlau /var/www/barlau/gunicorn_config.py

# Копируем systemd сервис
sudo cp barlau.service /etc/systemd/system/
sudo systemctl daemon-reload

# Копируем конфигурацию Nginx
sudo cp nginx_barlau.conf /etc/nginx/sites-available/barlau
sudo ln -sf /etc/nginx/sites-available/barlau /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 2. Создаем необходимые директории
echo "2. Создаем необходимые директории..."
sudo mkdir -p /var/run/barlau
sudo chown barlau:barlau /var/run/barlau

# 3. Устанавливаем Certbot для SSL сертификатов
echo "3. Устанавливаем Certbot для SSL..."
sudo apt install -y certbot python3-certbot-nginx

# 4. Временно настраиваем Nginx без SSL для получения сертификата
echo "4. Создаем временную конфигурацию Nginx..."
sudo tee /etc/nginx/sites-available/barlau-temp > /dev/null << EOF
server {
    listen 80;
    server_name barlau.org www.barlau.org barlau.kz www.barlau.kz;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /var/www/barlau/static/;
    }

    location /media/ {
        alias /var/www/barlau/media/;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/barlau-temp /etc/nginx/sites-enabled/barlau
sudo rm -f /etc/nginx/sites-enabled/default

# 5. Проверяем конфигурацию Nginx
echo "5. Проверяем конфигурацию Nginx..."
sudo nginx -t

# 6. Запускаем сервисы
echo "6. Запускаем сервисы..."
sudo systemctl enable barlau
sudo systemctl start barlau
sudo systemctl enable nginx
sudo systemctl restart nginx

# 7. Проверяем статус сервисов
echo "7. Проверяем статус сервисов..."
sudo systemctl status barlau --no-pager
sudo systemctl status nginx --no-pager

echo "=== Сервисы настроены! ==="
echo ""
echo "Следующие шаги:"
echo "1. Убедитесь что домены barlau.org и barlau.kz указывают на IP вашего VPS"
echo "2. Получите SSL сертификат: sudo certbot --nginx -d barlau.org -d www.barlau.org -d barlau.kz -d www.barlau.kz"
echo "3. После получения SSL замените временную конфигурацию на полную:"
echo "   sudo ln -sf /etc/nginx/sites-available/barlau /etc/nginx/sites-enabled/barlau"
echo "   sudo systemctl reload nginx"
echo ""
echo "Проверить работу сайта можно по адресу: http://$(curl -s ifconfig.me)" 