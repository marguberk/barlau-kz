#!/bin/bash

echo "🔧 Финальное исправление зависимостей..."

# Удаляем старое виртуальное окружение
echo "🗑️ Удаление старого виртуального окружения..."
sudo -u barlau bash -c "
    cd /var/www/barlau
    rm -rf venv
"

# Создаем новое виртуальное окружение
echo "🆕 Создание нового виртуального окружения..."
sudo -u barlau bash -c "
    cd /var/www/barlau
    python3 -m venv venv
    source venv/bin/activate
    
    # Обновляем pip
    pip install --upgrade pip
    
    # Устанавливаем базовые пакеты
    pip install setuptools wheel
"

# Создаем requirements.txt с совместимыми версиями для Python 3.12
echo "📝 Создание requirements.txt с совместимыми версиями..."
sudo -u barlau bash -c "
    cd /var/www/barlau
    cat > requirements.txt << 'EOF'
django==4.2.9
djangorestframework==3.14.0
django-cors-headers==4.3.1
python-dotenv==1.0.0
firebase-admin==6.3.0
pillow==10.2.0
django-phonenumber-field==7.2.0
phonenumbers==8.13.24
djangorestframework-simplejwt==5.3.0
django-filter==23.5
drf-yasg==1.21.7
python-decouple==3.8
whitenoise==6.6.0
gunicorn==21.2.0
django-model-utils==4.3.1
weasyprint==60.1
XlsxWriter==3.1.2
reportlab==4.4.1
numpy>=1.25.0
pandas>=2.1.0
mysqlclient==2.2.0
xhtml2pdf==0.2.16
EOF
"

# Устанавливаем зависимости поэтапно
echo "📦 Установка зависимостей поэтапно..."
sudo -u barlau bash -c "
    cd /var/www/barlau
    source venv/bin/activate
    
    # Сначала устанавливаем numpy
    pip install 'numpy>=1.25.0'
    
    # Затем pandas
    pip install 'pandas>=2.1.0'
    
    # Остальные зависимости
    pip install django==4.2.9
    pip install djangorestframework==3.14.0
    pip install django-cors-headers==4.3.1
    pip install python-dotenv==1.0.0
    pip install firebase-admin==6.3.0
    pip install pillow==10.2.0
    pip install django-phonenumber-field==7.2.0
    pip install phonenumbers==8.13.24
    pip install djangorestframework-simplejwt==5.3.0
    pip install django-filter==23.5
    pip install drf-yasg==1.21.7
    pip install python-decouple==3.8
    pip install whitenoise==6.6.0
    pip install gunicorn==21.2.0
    pip install django-model-utils==4.3.1
    pip install weasyprint==60.1
    pip install XlsxWriter==3.1.2
    pip install reportlab==4.4.1
    pip install mysqlclient==2.2.0
    pip install xhtml2pdf==0.2.16
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
        
        # Создаем суперпользователя
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
            echo ""
            echo "🎉🎉🎉 УСПЕХ! Сайт Barlau.kz запущен! 🎉🎉🎉"
            echo ""
            echo "🌍 Основной сайт: http://barlau.org"
            echo "🌍 По IP адресу: http://85.202.192.33"
            echo "👤 Админ панель: http://barlau.org/admin"
            echo "   Логин: admin"
            echo "   Пароль: admin123"
            echo ""
            echo "📋 Следующие шаги:"
            echo "   1. Проверьте работу сайта в браузере"
            echo "   2. Войдите в админ панель и настройте данные"
            echo "   3. Добавьте SSL сертификат (если нужно)"
            echo "   4. Настройте домен barlau.kz (если планируется)"
            echo ""
            echo "🔧 Техническая информация:"
            echo "   - VPS IP: 85.202.192.33"
            echo "   - Django порт: 8000"
            echo "   - Nginx порт: 80/443"
            echo "   - База данных: MySQL (barlau_db)"
            echo ""
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