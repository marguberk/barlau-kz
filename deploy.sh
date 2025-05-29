#!/bin/bash

# Деплой скрипт для barlau.org
echo "🚀 Начинаем деплой на barlau.org..."

# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Python 3.11 и pip
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip git nginx postgresql postgresql-contrib

# Создаем пользователя для приложения
sudo useradd -m -s /bin/bash barlau || echo "Пользователь barlau уже существует"

# Переходим в домашний каталог пользователя barlau
sudo su - barlau << 'EOF'
# Клонируем репозиторий
git clone https://github.com/marguberk/barlau-kz.git
cd barlau-kz
git checkout local-version

# Создаем виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Создаем файл настроек для продакшена
cat > local_settings.py << 'SETTINGS_EOF'
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here-change-this'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['barlau.org', 'www.barlau.org', '85.202.192.33', 'localhost']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'barlau_db',
        'USER': 'barlau_user',
        'PASSWORD': 'barlau_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Отключаем некоторые middleware для продакшена
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://barlau.org",
    "https://www.barlau.org",
]
SETTINGS_EOF

# Импортируем локальные настройки в основной файл настроек
cat >> barlau/settings.py << 'IMPORT_EOF'

# Импорт локальных настроек для продакшена
try:
    from .local_settings import *
except ImportError:
    pass
IMPORT_EOF

EOF

echo "✅ Репозиторий склонирован и настроен"

# Настраиваем PostgreSQL
sudo -u postgres psql << 'PSQL_EOF'
CREATE DATABASE barlau_db;
CREATE USER barlau_user WITH PASSWORD 'barlau_password';
ALTER ROLE barlau_user SET client_encoding TO 'utf8';
ALTER ROLE barlau_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE barlau_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE barlau_db TO barlau_user;
\q
PSQL_EOF

echo "✅ База данных PostgreSQL настроена"

# Выполняем миграции и собираем статику
sudo su - barlau << 'EOF'
cd barlau-kz
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput

# Создаем суперпользователя (опционально)
echo "from accounts.models import User; User.objects.create_superuser('admin', 'admin@barlau.org', 'admin123', role='SUPERADMIN') if not User.objects.filter(username='admin').exists() else print('Admin уже существует')" | python manage.py shell
EOF

echo "✅ Миграции выполнены, статика собрана"

# Создаем systemd сервис для Gunicorn
sudo tee /etc/systemd/system/barlau.service > /dev/null << 'SERVICE_EOF'
[Unit]
Description=Barlau Django Application
After=network.target

[Service]
User=barlau
Group=www-data
WorkingDirectory=/home/barlau/barlau-kz
Environment="PATH=/home/barlau/barlau-kz/venv/bin"
ExecStart=/home/barlau/barlau-kz/venv/bin/gunicorn --workers 3 --bind unix:/home/barlau/barlau-kz/barlau.sock barlau.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Запускаем и включаем сервис
sudo systemctl daemon-reload
sudo systemctl start barlau
sudo systemctl enable barlau

echo "✅ Gunicorn сервис настроен и запущен"

# Настраиваем Nginx
sudo tee /etc/nginx/sites-available/barlau.org > /dev/null << 'NGINX_EOF'
server {
    listen 80;
    server_name barlau.org www.barlau.org;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/barlau/barlau-kz;
    }
    
    location /media/ {
        root /home/barlau/barlau-kz;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/barlau/barlau-kz/barlau.sock;
    }
}
NGINX_EOF

# Активируем сайт
sudo ln -sf /etc/nginx/sites-available/barlau.org /etc/nginx/sites-enabled
sudo rm -f /etc/nginx/sites-enabled/default

# Тестируем и перезапускаем Nginx
sudo nginx -t
sudo systemctl restart nginx

echo "✅ Nginx настроен и перезапущен"

# Настраиваем права доступа
sudo chown -R barlau:www-data /home/barlau/barlau-kz
sudo chmod -R 755 /home/barlau/barlau-kz

echo "🎉 Деплой завершен!"
echo ""
echo "📋 Полезные команды:"
echo "sudo systemctl status barlau    # Статус приложения"
echo "sudo systemctl restart barlau   # Перезапуск приложения"
echo "sudo systemctl status nginx     # Статус веб-сервера"
echo "sudo tail -f /var/log/nginx/error.log  # Логи Nginx"
echo ""
echo "🌐 Сайт должен быть доступен по адресу: http://barlau.org"
echo "👤 Админ: admin / admin123" 