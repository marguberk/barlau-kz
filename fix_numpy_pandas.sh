#!/bin/bash

echo "🔧 Исправление конфликта numpy/pandas..."

# Переустанавливаем numpy и pandas с совместимыми версиями
echo "📦 Переустановка numpy и pandas..."
sudo -u barlau bash -c "
    cd /var/www/barlau
    source venv/bin/activate
    
    # Удаляем проблемные пакеты
    pip uninstall -y numpy pandas
    
    # Устанавливаем совместимые версии
    pip install numpy==1.24.3
    pip install pandas==2.0.3 --no-deps
    pip install pandas==2.0.3
"

echo "✅ numpy и pandas переустановлены"

# Проверяем Django
echo "🔍 Проверка Django..."
sudo -u barlau bash -c "
    cd /var/www/barlau
    source venv/bin/activate
    python manage.py check
"

if [ $? -eq 0 ]; then
    echo "✅ Django проверка прошла успешно"
    
    # Выполняем миграции
    echo "🗄️ Выполнение миграций..."
    sudo -u barlau bash -c "
        cd /var/www/barlau
        source venv/bin/activate
        python manage.py migrate
    "
    
    if [ $? -eq 0 ]; then
        echo "✅ Миграции выполнены успешно"
        
        # Создаем суперпользователя (если нужно)
        echo "👤 Создание суперпользователя..."
        sudo -u barlau bash -c "
            cd /var/www/barlau
            source venv/bin/activate
            echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@barlau.org', 'admin123')\" | python manage.py shell
        "
        
        # Собираем статические файлы
        echo "📁 Сбор статических файлов..."
        sudo -u barlau bash -c "
            cd /var/www/barlau
            source venv/bin/activate
            python manage.py collectstatic --noinput
        "
        
        # Перезапускаем сервис
        echo "🔄 Перезапуск сервиса barlau..."
        sudo systemctl restart barlau
        sudo systemctl enable barlau
        
        # Проверяем статус
        sleep 5
        echo "📊 Статус сервиса barlau:"
        sudo systemctl status barlau --no-pager -l
        
        # Проверяем порты
        echo "🌐 Проверка портов:"
        sudo netstat -tlnp | grep :8000
        
        if [ $? -eq 0 ]; then
            echo "🎉 Сайт успешно запущен!"
            echo "🌍 Проверьте: http://barlau.org"
            echo "🌍 Или по IP: http://85.202.192.33"
            echo "👤 Админ панель: http://barlau.org/admin (admin/admin123)"
        else
            echo "⚠️ Порт 8000 не слушается, проверяем логи..."
            sudo journalctl -u barlau --no-pager -l --since "5 minutes ago"
        fi
        
    else
        echo "❌ Ошибка при выполнении миграций"
        exit 1
    fi
else
    echo "❌ Ошибка при проверке Django"
    exit 1
fi 