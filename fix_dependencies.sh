#!/bin/bash

echo "🔧 Исправление зависимостей Django проекта..."

# Переходим в директорию проекта
cd /var/www/barlau

# Активируем виртуальное окружение и устанавливаем критические зависимости
echo "📦 Установка критических зависимостей..."
sudo -u barlau bash -c "
    cd /var/www/barlau
    source venv/bin/activate
    
    # Обновляем pip
    pip install --upgrade pip
    
    # Устанавливаем setuptools (содержит pkg_resources)
    pip install setuptools
    
    # Устанавливаем wheel для лучшей совместимости
    pip install wheel
    
    # Переустанавливаем все зависимости из requirements.txt
    pip install -r requirements.txt --force-reinstall
"

echo "✅ Зависимости установлены"

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
        echo "📊 Статус сервисов:"
        sudo systemctl status barlau --no-pager -l
        
        # Проверяем порты
        echo "🌐 Проверка портов:"
        sudo netstat -tlnp | grep :8000
        
        echo "🎉 Исправление завершено!"
        echo "🌍 Проверьте сайт: http://barlau.org"
        
    else
        echo "❌ Ошибка при выполнении миграций"
        exit 1
    fi
else
    echo "❌ Ошибка при проверке Django"
    exit 1
fi 