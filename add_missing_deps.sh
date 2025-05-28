#!/bin/bash

echo "📦 Добавление недостающих зависимостей..."

# Добавляем недостающие пакеты в requirements.txt
sudo -u barlau bash -c "
    cd /var/www/barlau
    echo 'xhtml2pdf==0.2.16' >> requirements.txt
    echo 'setuptools>=68.0.0' >> requirements.txt
"

echo "✅ Зависимости добавлены в requirements.txt"

# Устанавливаем недостающие пакеты
echo "🔧 Установка недостающих пакетов..."
sudo -u barlau bash -c "
    cd /var/www/barlau
    source venv/bin/activate
    pip install xhtml2pdf==0.2.16
    pip install setuptools>=68.0.0
"

echo "✅ Пакеты установлены"

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
        sleep 3
        echo "📊 Статус сервиса barlau:"
        sudo systemctl status barlau --no-pager -l
        
        # Проверяем порты
        echo "🌐 Проверка портов:"
        sudo netstat -tlnp | grep :8000
        
        if [ $? -eq 0 ]; then
            echo "🎉 Сайт успешно запущен!"
            echo "🌍 Проверьте: http://barlau.org"
            echo "🌍 Или по IP: http://85.202.192.33"
        else
            echo "⚠️ Порт 8000 не слушается, проверьте логи"
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