# 🚀 Руководство по деплою Barlau.kz на Plesk хостинг

## 📋 Предварительные требования

- Plesk хостинг с поддержкой Python/Django
- Домен barlau.org настроен в Plesk
- SSH доступ к серверу
- Git установлен на сервере

## 🔧 Пошаговая инструкция

### 1. Настройка Git деплоя в Plesk

1. Войдите в панель Plesk
2. Выберите домен `barlau.org`
3. Нажмите **"Развернуть с помощью Git"**
4. Укажите репозиторий: `https://github.com/marguberk/barlau-kz.git`
5. Выберите ветку: `mobile-menu-refactor`
6. Путь деплоя: `/httpdocs/`

### 2. Создание базы данных MySQL

1. В Plesk перейдите в **"Базы данных"**
2. Создайте новую базу данных:
   - Имя: `barlau_db`
   - Пользователь: `barlau_user`
   - Пароль: (сгенерируйте надежный пароль)

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта на сервере:

```bash
# Скопируйте содержимое из env.production.example
cp env.production.example .env
```

Отредактируйте `.env` файл с реальными значениями:

```env
SECRET_KEY=ваш-секретный-ключ-django
DEBUG=False
DJANGO_SETTINGS_MODULE=barlau.settings_production

DB_NAME=barlau_db
DB_USER=barlau_user
DB_PASSWORD=ваш-пароль-от-бд
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST_USER=ваш-email@gmail.com
EMAIL_HOST_PASSWORD=пароль-приложения-gmail
```

### 4. Установка зависимостей

```bash
# Перейдите в директорию проекта
cd /var/www/vhosts/barlau.org/httpdocs/

# Установите зависимости
pip install -r requirements.txt
```

### 5. Настройка Django

```bash
# Установите переменную окружения
export DJANGO_SETTINGS_MODULE=barlau.settings_production

# Выполните миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Соберите статические файлы
python manage.py collectstatic --noinput

# Создайте таблицу кэша
python manage.py createcachetable
```

### 6. Настройка веб-сервера в Plesk

1. Перейдите в **"Настройки Apache и nginx"**
2. Добавьте в конфигурацию nginx:

```nginx
location /static/ {
    alias /var/www/vhosts/barlau.org/httpdocs/static/;
    expires 30d;
}

location /media/ {
    alias /var/www/vhosts/barlau.org/httpdocs/media/;
    expires 30d;
}
```

### 7. Настройка SSL сертификата

1. В Plesk перейдите в **"SSL/TLS сертификаты"**
2. Выберите **"Let's Encrypt"**
3. Включите сертификат для домена и www поддомена

### 8. Настройка автоматического деплоя

В настройках Git репозитория в Plesk:

1. Включите **"Автоматическое развертывание"**
2. Добавьте post-deployment скрипт:

```bash
#!/bin/bash
cd /var/www/vhosts/barlau.org/httpdocs/
./deploy.sh
```

## 🔄 Обновление проекта

После внесения изменений в код:

1. Сделайте commit и push в GitHub
2. В Plesk нажмите **"Обновить из репозитория"**
3. Или выполните на сервере:

```bash
cd /var/www/vhosts/barlau.org/httpdocs/
git pull origin mobile-menu-refactor
./deploy.sh
```

## 📊 Мониторинг

### Логи Django
```bash
tail -f /var/www/vhosts/barlau.org/logs/django.log
```

### Логи веб-сервера
```bash
tail -f /var/www/vhosts/barlau.org/logs/access_log
tail -f /var/www/vhosts/barlau.org/logs/error_log
```

## 🛠️ Устранение неполадок

### Проблема: 500 Internal Server Error
1. Проверьте логи Django
2. Убедитесь, что DEBUG=False в продакшн
3. Проверьте права доступа к файлам

### Проблема: Статические файлы не загружаются
1. Выполните `python manage.py collectstatic --noinput`
2. Проверьте настройки nginx для /static/

### Проблема: База данных недоступна
1. Проверьте настройки подключения в .env
2. Убедитесь, что пользователь БД имеет все права

## 📱 Подготовка к мобильным приложениям

После успешного деплоя веб-версии:

1. Настройте CORS для мобильных приложений
2. Создайте API ключи для Firebase
3. Настройте push-уведомления
4. Протестируйте API endpoints

## 🎉 Готово!

Ваш сайт должен быть доступен по адресу: https://barlau.org

Для доступа к админ-панели: https://barlau.org/admin/ 