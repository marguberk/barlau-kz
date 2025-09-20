#!/bin/bash

# Скрипт для выполнения очистки на продакшн сервере через SSH
# Автоматически подключается к серверу и выполняет очистку

echo "🚀 Выполняем очистку продакшн базы данных BARLAU.KZ"
echo "📅 Дата: $(date)"
echo ""

# Параметры подключения
SERVER="85.202.192.33"
USER="ubuntu"
PASSWORD="33q97KKRfmnHTY6dCiyuA3g="

echo "🔌 Подключаемся к серверу $SERVER..."

# Создаем временный скрипт на сервере
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USER@$SERVER" << 'EOF'
# Создаем директорию для скриптов
mkdir -p /home/ubuntu/cleanup_scripts

# Создаем Python скрипт очистки
cat > /home/ubuntu/cleanup_scripts/cleanup_production_data.py << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Скрипт для очистки продакшн базы данных от тестовых данных
Удаляет обычных сотрудников, водителей и транспортные средства
Оставляет только администраторов и директоров
"""

import os
import sys
import django

# Настройка Django
sys.path.append('/home/ubuntu/barlau_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Employee, Vehicle, Trip, Expense
from django.db import transaction

def cleanup_production_data():
    """
    Очистка продакшн базы данных от тестовых данных
    """
    
    print("🧹 Начинаем очистку продакшн базы данных...")
    
    # Список сотрудников для удаления (обычные сотрудники)
    employees_to_remove = [
        "Айдарбеков Серік Шайдолдаұлы",
        "Сопашев Алмасжан Сематжанович", 
        "Құсайын Мақсат Ермекұлы",
        "Кудайбергенов Ерболат Чингизович",
        "Садвакасова Назерке Касымхановна",
        "Ахметов Ғабит Сәбитұлы",
        "Илямов Азиз Алымжанұлы",
        "Ұзақ Айдана Ербосынқызы",
        "Мұрат Асель Мұратқызы"
    ]
    
    # Список водителей для удаления
    drivers_to_remove = [
        "Касимов Сухрат Алимжанович",
        "Қасенов Хезиз Ибраимұлы",
        "Сабит Ғабит Нұрғалиұлы",
        "Садыров Рустем Шаукетович",
        "Пида Хамражан Магаметжанович",
        "Камердинов Азизжан Якупжанович",
        "Рузиев Сраилжан Смаилович",
        "Саит Абдулжан Адилович",
        "Абдуллаев Хамит Рахемжанович",
        "Муталипов Марат Хасанович",
        "Исмаилов Розахун Рахимжанович",
        "Касымов Шахмурат Дильмуратович",
        "Кудайбергенов Жасулан Берикович",
        "Умурбеков Елдос Болатханович"
    ]
    
    # Список транспортных средств для удаления
    vehicles_to_remove = [
        "484ATL01", "057AUC01", "456AUC01", "956AUN01", "533ATL01",
        "290ATL01", "355ATL01", "474ATL01", "257ASC01", "108AGR19",
        "481ACA19", "523BMT02", "213AUL01", "208AUL01", "203AUL01",
        "359AUL01", "355AUL01", "287AUL01", "917AQM01", "913AQM01",
        "105AGR19", "042BJK02", "695BHS02", "494AVW01"
    ]
    
    with transaction.atomic():
        # Удаляем обычных сотрудников
        print("\n👥 Удаляем обычных сотрудников...")
        removed_employees = 0
        for employee_name in employees_to_remove:
            try:
                # Ищем сотрудника по имени
                employee = Employee.objects.filter(
                    first_name__icontains=employee_name.split()[0],
                    last_name__icontains=employee_name.split()[1]
                ).first()
                
                if employee:
                    print(f"  ❌ Удаляем: {employee_name}")
                    employee.delete()
                    removed_employees += 1
                else:
                    print(f"  ⚠️  Не найден: {employee_name}")
            except Exception as e:
                print(f"  🔴 Ошибка при удалении {employee_name}: {e}")
        
        # Удаляем водителей
        print(f"\n🚗 Удаляем водителей...")
        removed_drivers = 0
        for driver_name in drivers_to_remove:
            try:
                # Ищем водителя по имени
                driver = Employee.objects.filter(
                    first_name__icontains=driver_name.split()[0],
                    last_name__icontains=driver_name.split()[1],
                    role='DRIVER'
                ).first()
                
                if driver:
                    print(f"  ❌ Удаляем водителя: {driver_name}")
                    driver.delete()
                    removed_drivers += 1
                else:
                    print(f"  ⚠️  Водитель не найден: {driver_name}")
            except Exception as e:
                print(f"  🔴 Ошибка при удалении водителя {driver_name}: {e}")
        
        # Удаляем транспортные средства
        print(f"\n🚛 Удаляем транспортные средства...")
        removed_vehicles = 0
        for vehicle_number in vehicles_to_remove:
            try:
                vehicle = Vehicle.objects.filter(license_plate=vehicle_number).first()
                if vehicle:
                    print(f"  ❌ Удаляем ТС: {vehicle_number}")
                    vehicle.delete()
                    removed_vehicles += 1
                else:
                    print(f"  ⚠️  ТС не найдено: {vehicle_number}")
            except Exception as e:
                print(f"  🔴 Ошибка при удалении ТС {vehicle_number}: {e}")
        
        # Удаляем связанные данные (поездки и расходы)
        print(f"\n🧹 Очищаем связанные данные...")
        
        # Удаляем поездки без водителей
        trips_deleted = Trip.objects.filter(driver__isnull=True).count()
        Trip.objects.filter(driver__isnull=True).delete()
        print(f"  ❌ Удалено поездок без водителей: {trips_deleted}")
        
        # Удаляем расходы без сотрудников
        expenses_deleted = Expense.objects.filter(employee__isnull=True).count()
        Expense.objects.filter(employee__isnull=True).delete()
        print(f"  ❌ Удалено расходов без сотрудников: {expenses_deleted}")
        
        print(f"\n✅ Очистка завершена!")
        print(f"📊 Статистика удаления:")
        print(f"  👥 Сотрудников: {removed_employees}")
        print(f"  🚗 Водителей: {removed_drivers}")
        print(f"  🚛 Транспортных средств: {removed_vehicles}")
        print(f"  🗺️  Поездок: {trips_deleted}")
        print(f"  💰 Расходов: {expenses_deleted}")
        
        # Показываем оставшихся пользователей
        print(f"\n👑 Оставшиеся пользователи:")
        remaining_users = User.objects.all()
        for user in remaining_users:
            print(f"  ✅ {user.username} - {user.first_name} {user.last_name}")
        
        # Показываем оставшихся сотрудников
        print(f"\n👥 Оставшиеся сотрудники:")
        remaining_employees = Employee.objects.all()
        for employee in remaining_employees:
            print(f"  ✅ {employee.first_name} {employee.last_name} - {employee.role}")

if __name__ == "__main__":
    cleanup_production_data()
PYTHON_EOF

# Переходим в директорию проекта
cd /home/ubuntu/barlau_project

# Активируем виртуальное окружение
source venv/bin/activate

# Создаем резервную копию
echo "💾 Создаем резервную копию базы данных..."
BACKUP_FILE="backup_before_cleanup_$(date +%Y%m%d_%H%M%S).sql"
mkdir -p /home/ubuntu/backups
pg_dump -h localhost -U barlau_user -d barlau_db > "/home/ubuntu/backups/$BACKUP_FILE"
echo "✅ Резервная копия создана: $BACKUP_FILE"

# Выполняем очистку
echo "🧹 Выполняем очистку данных..."
python /home/ubuntu/cleanup_scripts/cleanup_production_data.py

echo "✅ Очистка завершена!"
EOF

echo ""
echo "🎉 Очистка продакшн базы данных завершена!"
echo "📅 Время завершения: $(date)"
