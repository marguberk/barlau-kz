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

## Установка на PythonAnywhere

1. Клонировать репозиторий:
```bash
git clone https://github.com/marguberk/barlau-kz.git
cd barlau-kz
```

2. Создать виртуальное окружение Python 3.10:
```bash
mkvirtualenv --python=python3.10 barlau
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Настроить базу данных:
```bash
python manage.py migrate
```

5. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

6. Собрать статические файлы:
```bash
python manage.py collectstatic --noinput
```

7. Настроить WSGI файл в панели PythonAnywhere, указав путь к файлу wsgi.py

## Основные компоненты системы

- Система учета транспорта и мониторинга
- Управление сотрудниками и задачами
- Путевые листы и документооборот
- Финансовый учет и отчетность

## Технологии

- Backend: Django 4.2 с Django REST Framework
- Frontend: TailwindCSS с использованием компонентов ShadcnUI
- База данных: MySQL
- Деплой: PythonAnywhere

## Лицензия

Проприетарное программное обеспечение, защищенное авторским правом.

© 2024 BARLAU.KZ. Все права защищены. 