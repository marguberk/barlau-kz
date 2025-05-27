#!/bin/bash

# Скрипт деплоя Django проекта Barlau.kz на VPS

echo "=== Деплой Django проекта Barlau.kz ==="

# 1. Переходим в директорию проекта
cd /var/www/barlau

# 2. Клонируем репозиторий
echo "1. Клонируем репозиторий..."
sudo -u barlau git clone https://github.com/marguberk/barlau-kz.git .

# 3. Создаем виртуальное окружение
echo "2. Создаем виртуальное окружение..."
sudo -u barlau python3 -m venv venv

# 4. Активируем виртуальное окружение и устанавливаем зависимости
echo "3. Устанавливаем зависимости Python..."
sudo -u barlau bash -c "source venv/bin/activate && pip install --upgrade pip"
sudo -u barlau bash -c "source venv/bin/activate && pip install -r requirements.txt"

# 5. Создаем файл .env
echo "4. Создаем файл .env..."
sudo -u barlau cat > .env << EOF
# Django settings
SECRET_KEY=your-very-secret-key-here-change-this-in-production
DEBUG=False
DJANGO_SETTINGS_MODULE=barlau.settings_production

# Database settings
DB_NAME=barlau_db
DB_USER=barlau_user
DB_PASSWORD=BarlauSecure2024!
DB_HOST=localhost
DB_PORT=3306

# Email settings (настройте по необходимости)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@barlau.org

# Firebase settings (добавьте ваши ключи)
FIREBASE_CREDENTIALS_PATH=/var/www/barlau/firebase-credentials.json
EOF

# 6. Создаем директории для статических файлов и медиа
echo "5. Создаем директории для статических файлов..."
sudo -u barlau mkdir -p static media logs

# 7. Выполняем миграции Django
echo "6. Выполняем миграции Django..."
sudo -u barlau bash -c "source venv/bin/activate && python manage.py migrate"

# 8. Собираем статические файлы
echo "7. Собираем статические файлы..."
sudo -u barlau bash -c "source venv/bin/activate && python manage.py collectstatic --noinput"

# 9. Создаем таблицу кэша
echo "8. Создаем таблицу кэша..."
sudo -u barlau bash -c "source venv/bin/activate && python manage.py createcachetable"

# 10. Создаем суперпользователя (интерактивно)
echo "9. Создание суперпользователя..."
echo "Сейчас будет запрошено создание суперпользователя Django:"
sudo -u barlau bash -c "source venv/bin/activate && python manage.py createsuperuser"

echo "=== Django проект развернут! ==="
echo "Следующие шаги:"
echo "1. Настроить Gunicorn"
echo "2. Настроить Nginx"
echo "3. Настроить SSL сертификат"
echo "4. Настроить автозапуск сервисов" 