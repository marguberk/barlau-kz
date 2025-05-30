#!/bin/bash

echo "🔄 Быстрое обновление barlau.org..."

# Создаем временный файл с командами
cat > /tmp/deploy_commands.sh << 'EOF'
cd /home/barlau/barlau-kz
systemctl stop barlau
sudo -u barlau git pull origin local-version
sudo -u barlau bash -c "source venv/bin/activate && python manage.py migrate && python manage.py collectstatic --noinput"
systemctl start barlau
systemctl restart nginx
echo "✅ Обновление завершено!"
EOF

echo "📋 Команды для выполнения на сервере созданы в /tmp/deploy_commands.sh"
echo "🔑 Подключитесь к серверу и выполните:"
echo "ssh root@barlau.org"
echo "bash -s < /tmp/deploy_commands.sh" 