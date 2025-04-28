# BARLAU.KZ - Система управления логистикой

![BARLAU.KZ Logo](static/core/img/logo.png)

Веб-приложение для управления логистикой, сотрудниками и задачами компании. Разработано с использованием Django 5.1.6 и современного стека веб-технологий.

## Основные возможности

- Управление задачами и рабочими процессами
- Отслеживание местоположения транспорта на карте
- Управление сотрудниками и их ролями
- Финансовый учет и аналитика
- Полная мобильная поддержка (PWA)

## Требования

- Python 3.9+
- Django 5.1.6
- Другие зависимости в requirements.txt

## Локальная установка

```bash
# Клонирование репозитория
git clone https://github.com/marguberk/barlau-kz.git
cd barlau-kz

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# venv\Scripts\activate  # для Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
# Создайте файл .env в корневой директории проекта с содержимым:
SECRET_KEY=ваш_секретный_ключ
DEBUG=True

# Выполнение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера разработки
python manage.py runserver
```

## PWA (Progressive Web App)

Приложение поддерживает функциональность PWA, что позволяет:
- Устанавливать приложение на домашний экран
- Работать в оффлайн-режиме
- Получать push-уведомления

## Деплой на PythonAnywhere

### Шаг 1: Создание аккаунта и настройка окружения

1. Зарегистрируйтесь на [PythonAnywhere](https://www.pythonanywhere.com)
2. Создайте новое веб-приложение:
   - Выберите Django
   - Выберите Python 3.9 или выше
   - Укажите домен: yourusername.pythonanywhere.com

### Шаг 2: Загрузка кода

1. Откройте bash консоль на PythonAnywhere
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/marguberk/barlau-kz.git
   ```
3. Создайте и активируйте виртуальное окружение:
   ```bash
   cd barlau-kz
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Шаг 3: Настройка MySQL

1. Создайте базу данных MySQL через панель управления PythonAnywhere
2. Отредактируйте файл `barlau/pythonanywhere_settings.py`:
   - Укажите ваши учетные данные MySQL
   - Замените `yourusername` на ваше имя пользователя PythonAnywhere

### Шаг 4: Настройка WSGI

1. В файле `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
   ```python
   import os
   import sys

   path = '/home/yourusername/barlau-kz'
   if path not in sys.path:
       sys.path.append(path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'barlau.pythonanywhere_settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

### Шаг 5: Настройка статических файлов

1. В панели управления PythonAnywhere укажите пути:
   - URL: `/static/`
   - Directory: `/home/yourusername/barlau-kz/staticfiles`
   - URL: `/media/`
   - Directory: `/home/yourusername/barlau-kz/media`

### Шаг 6: Финальная настройка

1. Выполните сбор статических файлов и миграции:
   ```bash
   python manage.py collectstatic
   python manage.py migrate
   ```
2. Перезагрузите приложение через панель управления

## Лицензия

Проприетарное программное обеспечение, защищенное авторским правом.

© 2024 BARLAU.KZ. Все права защищены. 