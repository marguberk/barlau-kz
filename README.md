# BARLAU.KZ - Система управления логистикой и сотрудниками

## О проекте

BARLAU.KZ - это веб-приложение для управления логистической компанией. Система позволяет отслеживать транспорт, управлять задачами и путевыми листами, вести учет сотрудников и контролировать финансы.

## Технологии

- Backend: Django, Django REST Framework
- Frontend: TailwindCSS, JavaScript
- База данных: SQLite (разработка), MySQL (продакшен)
- Безопасность: JWT-аутентификация
- Дополнительно: PWA (Progressive Web App)

## Установка и запуск (локальная разработка)

### Предварительные требования

- Python 3.8+
- pip
- virtualenv (опционально)

### Настройка проекта

1. Клонировать репозиторий:
```
git clone https://github.com/your-username/barlau-kz.git
cd barlau-kz
```

2. Создать и активировать виртуальное окружение:
```
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установить зависимости:
```
pip install -r requirements.txt
```

4. Создать файл `.env` в корне проекта:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

5. Выполнить миграции:
```
python manage.py migrate
```

6. Создать суперпользователя:
```
python manage.py createsuperuser
```

7. Запустить сервер разработки:
```
python manage.py runserver
```

8. Открыть в браузере http://127.0.0.1:8000/

## Развертывание на PythonAnywhere

### Настройка проекта на PythonAnywhere

1. Создать аккаунт на [PythonAnywhere](https://www.pythonanywhere.com/).

2. Открыть Bash консоль и клонировать репозиторий:
```
git clone https://github.com/marguberk/barlau-kz.git
```

3. Создать виртуальное окружение и установить зависимости:
```
cd barlau-kz
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Создать файл `barlau/pythonanywhere_settings.py`:
```python
PYTHONANYWHERE = True
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Настройки базы данных для MySQL на PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourusername$barlau',
        'USER': 'yourusername',
        'PASSWORD': 'your-database-password',
        'HOST': 'yourusername.mysql.pythonanywhere-services.com',
        'PORT': '',
    }
}

# Настройки для обслуживания медиа-файлов
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yourusername/barlau-kz/media'
STATIC_URL = '/static/'
STATIC_ROOT = '/home/yourusername/barlau-kz/static'

# Дополнительные настройки безопасности
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

5. Создать и настроить базу данных MySQL:
   - Перейти в раздел Databases
   - Создать новую базу данных (например, `yourusername$barlau`)
   - Запомнить пароль

6. Отредактировать файл `barlau/wsgi.py`:
```python
import os
import sys

# Добавить путь к проекту
path = '/home/yourusername/barlau-kz'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

7. Выполнить миграции и создать суперпользователя:
```
python manage.py migrate
python manage.py createsuperuser
```

8. Собрать статические файлы:
```
python manage.py collectstatic
```

### Настройка веб-приложения на PythonAnywhere

1. Перейти в раздел "Web" и добавить новое веб-приложение.
2. Выбрать "Manual configuration" и версию Python, соответствующую вашему проекту.
3. Настроить путь к виртуальному окружению: `/home/yourusername/barlau-kz/venv`
4. Настроить путь к файлу WSGI: `/home/yourusername/barlau-kz/barlau/wsgi.py`
5. Настроить статические файлы:
   - URL: `/static/`
   - Directory: `/home/yourusername/barlau-kz/static`
6. Настроить медиа-файлы:
   - URL: `/media/`
   - Directory: `/home/yourusername/barlau-kz/media`
7. Перезапустить веб-приложение.

## Обновление проекта на PythonAnywhere

Для обновления проекта на PythonAnywhere выполните следующие команды:

```bash
cd ~/barlau-kz
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Затем перезапустите веб-приложение из раздела "Web".

## Дополнительная информация

- Для роботы с API используйте Swagger: `/swagger/`
- Документация API: `/redoc/`
- Админ-панель: `/admin/`

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