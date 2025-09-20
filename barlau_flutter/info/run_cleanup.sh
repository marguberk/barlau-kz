#!/bin/bash

# Скрипт для выполнения очистки продакшн базы данных
# Выполняется на продакшн сервере

echo "🚀 Начинаем очистку продакшн базы данных BARLAU.KZ"
echo "📅 Дата: $(date)"
echo "🖥️  Сервер: $(hostname)"
echo ""

# Переходим в директорию проекта
cd /home/ubuntu/barlau_project

# Активируем виртуальное окружение
echo "🔧 Активируем виртуальное окружение..."
source venv/bin/activate

# Проверяем подключение к базе данных
echo "🔍 Проверяем подключение к базе данных..."
python manage.py check --database default

if [ $? -ne 0 ]; then
    echo "❌ Ошибка подключения к базе данных!"
    exit 1
fi

echo "✅ Подключение к базе данных успешно"
echo ""

# Создаем резервную копию базы данных
echo "💾 Создаем резервную копию базы данных..."
BACKUP_FILE="backup_before_cleanup_$(date +%Y%m%d_%H%M%S).sql"
pg_dump -h localhost -U barlau_user -d barlau_db > "/home/ubuntu/backups/$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Резервная копия создана: $BACKUP_FILE"
else
    echo "⚠️  Не удалось создать резервную копию, продолжаем..."
fi

echo ""

# Выполняем очистку
echo "🧹 Выполняем очистку данных..."
python /home/ubuntu/barlau_project/cleanup_production_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Очистка завершена успешно!"
    echo "📊 Проверяем результаты..."
    
    # Показываем статистику
    echo ""
    echo "📈 Статистика после очистки:"
    python manage.py shell -c "
from django.contrib.auth.models import User
from core.models import Employee, Vehicle, Trip, Expense
print(f'👤 Пользователей: {User.objects.count()}')
print(f'👥 Сотрудников: {Employee.objects.count()}')
print(f'🚛 Транспортных средств: {Vehicle.objects.count()}')
print(f'🗺️  Поездок: {Trip.objects.count()}')
print(f'💰 Расходов: {Expense.objects.count()}')
"
    
else
    echo "❌ Ошибка при выполнении очистки!"
    exit 1
fi

echo ""
echo "✅ Скрипт завершен успешно!"
echo "📅 Время завершения: $(date)"
