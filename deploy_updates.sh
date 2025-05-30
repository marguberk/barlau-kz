#!/bin/bash

echo "🔄 Обновление системы уведомлений на barlau.org..."

# Выполняем команды на продакшн сервере
ssh root@barlau.org << 'EOF'
# Переходим в директорию проекта
cd /home/barlau/barlau-kz

# Останавливаем сервис
systemctl stop barlau

# Обновляем код из Git
sudo -u barlau git pull origin local-version

# Активируем виртуальное окружение и выполняем миграции
sudo -u barlau bash << 'INNER_EOF'
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
INNER_EOF

# Перезапускаем сервисы
systemctl start barlau
systemctl restart nginx

echo "✅ Обновление завершено!"
EOF

echo "🎉 Система уведомлений обновлена на barlau.org" 