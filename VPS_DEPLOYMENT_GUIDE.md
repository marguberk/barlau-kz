# Руководство по деплою Django проекта Barlau.kz на VPS Ubuntu 24.04.2 LTS

## Обзор

Это руководство поможет развернуть Django проект Barlau.kz на VPS сервере с Ubuntu 24.04.2 LTS, используя:
- **Django 4.2.9** - веб-фреймворк
- **MySQL 8.0** - база данных
- **Nginx** - веб-сервер
- **Gunicorn** - WSGI сервер
- **Let's Encrypt** - SSL сертификаты

## Предварительные требования

1. ✅ VPS с Ubuntu 24.04.2 LTS (заказан у ps.kz)
2. ✅ Доступ к консоли VNC или SSH
3. ✅ Домены barlau.org и barlau.kz настроены на IP VPS
4. ✅ Репозиторий GitHub: https://github.com/marguberk/barlau-kz.git

## Пошаговая инструкция

### Шаг 1: Базовая настройка системы

```bash
# Войдите в VPS через VNC консоль или SSH
# Скачайте скрипты настройки
wget https://raw.githubusercontent.com/marguberk/barlau-kz/main/vps_setup_commands.sh
chmod +x vps_setup_commands.sh
sudo ./vps_setup_commands.sh
```

**Что делает скрипт:**
- Обновляет систему
- Устанавливает Python 3, pip, venv
- Устанавливает MySQL сервер
- Устанавливает Nginx
- Устанавливает Git и дополнительные инструменты
- Создает пользователя `barlau` для приложения
- Создает необходимые директории

### Шаг 2: Настройка MySQL

```bash
# Запустите скрипт настройки MySQL
wget https://raw.githubusercontent.com/marguberk/barlau-kz/main/mysql_setup.sh
chmod +x mysql_setup.sh
sudo ./mysql_setup.sh
```

**Важно:** Запомните root пароль MySQL и данные созданной базы:
- База данных: `barlau_db`
- Пользователь: `barlau_user`
- Пароль: `BarlauSecure2024!`

### Шаг 3: Деплой Django проекта

```bash
# Запустите скрипт деплоя Django
wget https://raw.githubusercontent.com/marguberk/barlau-kz/main/django_deploy.sh
chmod +x django_deploy.sh
sudo ./django_deploy.sh
```

**Что делает скрипт:**
- Клонирует репозиторий в `/var/www/barlau`
- Создает виртуальное окружение Python
- Устанавливает зависимости из `requirements.txt`
- Создает файл `.env` с настройками
- Выполняет миграции Django
- Собирает статические файлы
- Создает таблицу кэша
- Запрашивает создание суперпользователя

### Шаг 4: Настройка сервисов

```bash
# Скачайте конфигурационные файлы
wget https://raw.githubusercontent.com/marguberk/barlau-kz/main/gunicorn_config.py
wget https://raw.githubusercontent.com/marguberk/barlau-kz/main/nginx_barlau.conf
wget https://raw.githubusercontent.com/marguberk/barlau-kz/main/barlau.service
wget https://raw.githubusercontent.com/marguberk/barlau-kz/main/setup_services.sh

# Запустите настройку сервисов
chmod +x setup_services.sh
sudo ./setup_services.sh
```

**Что делает скрипт:**
- Настраивает Gunicorn с автозапуском
- Настраивает Nginx
- Устанавливает Certbot для SSL
- Запускает все сервисы

### Шаг 5: Настройка DNS и SSL

1. **Настройте DNS записи** для ваших доменов:
   ```
   barlau.org     A    [IP_ВАШЕГО_VPS]
   www.barlau.org A    [IP_ВАШЕГО_VPS]
   barlau.kz      A    [IP_ВАШЕГО_VPS]
   www.barlau.kz  A    [IP_ВАШЕГО_VPS]
   ```

2. **Получите SSL сертификат:**
   ```bash
   sudo certbot --nginx -d barlau.org -d www.barlau.org -d barlau.kz -d www.barlau.kz
   ```

3. **Активируйте полную конфигурацию Nginx:**
   ```bash
   sudo ln -sf /etc/nginx/sites-available/barlau /etc/nginx/sites-enabled/barlau
   sudo systemctl reload nginx
   ```

## Проверка работы

### Проверка сервисов
```bash
# Статус Django приложения
sudo systemctl status barlau

# Статус Nginx
sudo systemctl status nginx

# Статус MySQL
sudo systemctl status mysql

# Логи Django
sudo journalctl -u barlau -f

# Логи Nginx
sudo tail -f /var/log/nginx/barlau_access.log
sudo tail -f /var/log/nginx/barlau_error.log
```

### Проверка сайта
- Откройте браузер и перейдите на https://barlau.org
- Проверьте админ панель: https://barlau.org/admin/
- Проверьте API: https://barlau.org/api/

## Управление проектом

### Обновление кода
```bash
# Переключитесь на пользователя barlau
sudo su - barlau
cd /var/www/barlau

# Обновите код
git pull origin main

# Активируйте виртуальное окружение
source venv/bin/activate

# Установите новые зависимости (если есть)
pip install -r requirements.txt

# Выполните миграции
python manage.py migrate

# Соберите статические файлы
python manage.py collectstatic --noinput

# Перезапустите приложение
sudo systemctl restart barlau
```

### Резервное копирование
```bash
# Создание бэкапа базы данных
mysqldump -u barlau_user -p barlau_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Создание бэкапа медиа файлов
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz /var/www/barlau/media/
```

## Мониторинг и логи

### Основные логи
- Django приложение: `sudo journalctl -u barlau`
- Gunicorn: `/var/log/barlau/gunicorn_error.log`
- Nginx доступ: `/var/log/nginx/barlau_access.log`
- Nginx ошибки: `/var/log/nginx/barlau_error.log`
- MySQL: `/var/log/mysql/error.log`

### Мониторинг ресурсов
```bash
# Использование CPU и памяти
htop

# Использование диска
df -h

# Сетевые подключения
netstat -tulpn | grep :80
netstat -tulpn | grep :443
netstat -tulpn | grep :8000
```

## Безопасность

### Настройка файрвола
```bash
# Установка UFW
sudo apt install ufw

# Базовые правила
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### Обновления безопасности
```bash
# Автоматические обновления безопасности
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Решение проблем

### Проблема: Django не запускается
```bash
# Проверьте логи
sudo journalctl -u barlau -n 50

# Проверьте конфигурацию
sudo -u barlau bash -c "cd /var/www/barlau && source venv/bin/activate && python manage.py check"
```

### Проблема: Nginx показывает 502 Bad Gateway
```bash
# Проверьте что Gunicorn запущен
sudo systemctl status barlau

# Проверьте что порт 8000 слушается
netstat -tulpn | grep :8000
```

### Проблема: SSL сертификат не работает
```bash
# Обновите сертификат
sudo certbot renew

# Проверьте конфигурацию Nginx
sudo nginx -t
```

## Контакты и поддержка

- **Репозиторий:** https://github.com/marguberk/barlau-kz
- **Документация Django:** https://docs.djangoproject.com/
- **Документация Nginx:** https://nginx.org/en/docs/
- **Документация Let's Encrypt:** https://letsencrypt.org/docs/

---

**Успешного деплоя! 🚀** 