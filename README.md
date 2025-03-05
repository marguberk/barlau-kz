# Barlau.kz - Система управления логистической компанией

## Описание
Barlau.kz - это веб-приложение для автоматизации процессов в логистической компании. Система включает в себя управление задачами, контроль грузовиков, составление КАТов, отчеты о расходах и информацию о сотрудниках.

## Основные функции
- Управление пользователями с разными ролями (Директор, Бухгалтер, Водитель, Снабженец, Техотдел)
- Отслеживание местоположения грузовиков в реальном времени
- Управление финансами и отчетностью
- Управление персоналом и резюме сотрудников
- Система аутентификации через телефон (SMS/WhatsApp)

## Технологии
- Backend: Python Django + Django REST Framework
- Frontend: React.js + Tailwind CSS + Shards UI Kit
- База данных: PostgreSQL
- Аутентификация: Firebase Authentication
- Геолокация: Google Maps API

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/barlau.git
cd barlau
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

3. Настройте переменные окружения:
Создайте файл .env в корневой директории и добавьте необходимые переменные:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
FIREBASE_CREDENTIALS=path-to-firebase-credentials.json
```

4. Выполните миграции:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Запустите сервер:
```bash
python manage.py runserver
```

## Документация API
API документация доступна по адресу: `http://localhost:8000/api/docs/`

## Лицензия
MIT License 