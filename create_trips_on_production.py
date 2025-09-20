#!/usr/bin/env python3
"""
Скрипт для создания заездов напрямую на продакшн сервере
"""

import paramiko
import json
from datetime import datetime, timedelta
from decimal import Decimal

# Данные продакшн сервера
PROD_HOST = '85.202.192.33'
PROD_USER = 'ubuntu'
PROD_PASSWORD = '33q97KKRfmnHTY6dCiyuA3g='
PROD_PORT = 22

def create_trips_on_production():
    """Создание заездов на продакшн сервере"""
    print("🚛 Подключение к продакшн серверу...")
    
    try:
        # Создаем SSH клиент
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Подключаемся к серверу
        ssh.connect(
            hostname=PROD_HOST,
            username=PROD_USER,
            password=PROD_PASSWORD,
            port=PROD_PORT,
            timeout=30
        )
        
        print("✅ Подключение к серверу успешно!")
        
        # Переходим в директорию проекта
        ssh.exec_command('cd /var/www/barlau')
        
        # Активируем виртуальное окружение
        ssh.exec_command('source venv/bin/activate')
        
        # Создаем Python скрипт для создания заездов
        trip_script = '''
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from core.models import Trip
from logistics.models import Vehicle
from accounts.models import User
from django.utils import timezone

def create_production_trips():
    """Создание 3 заездов в продакшене"""
    
    print("🚛 Создание заездов в продакшене...")
    
    # Получаем активные грузовики
    trucks = Vehicle.objects.filter(vehicle_type='TRUCK', status='ACTIVE')
    if not trucks.exists():
        print("❌ Нет активных грузовиков!")
        return
    
    # Получаем водителей
    drivers = User.objects.filter(role='DRIVER', is_active=True)
    if not drivers.exists():
        print("❌ Нет активных водителей!")
        return
    
    # Получаем администратора для создания заездов
    admin_user = User.objects.filter(role__in=['ADMIN', 'SUPERADMIN', 'DIRECTOR'], is_active=True).first()
    if not admin_user:
        print("❌ Нет администратора для создания заездов!")
        return
    
    print(f"✅ Найдено грузовиков: {trucks.count()}")
    print(f"✅ Найдено водителей: {drivers.count()}")
    print(f"✅ Администратор: {admin_user.first_name} {admin_user.last_name}")
    
    # Текущее время
    now = timezone.now()
    
    # 1. АКТИВНЫЙ ЗАЕЗД (в пути)
    print("\\n📦 Создание АКТИВНОГО заезда...")
    active_trip = Trip.objects.create(
        title="Алматы → Астана - Электроника",
        status='ACTIVE',
        vehicle=trucks.first(),
        driver=drivers.first(),
        start_address="Алматы, ул. Достык, 123",
        end_address="Астана, ул. Республики, 456",
        start_latitude=Decimal('43.238949'),
        start_longitude=Decimal('76.889709'),
        end_latitude=Decimal('51.1801'),
        end_longitude=Decimal('71.446'),
        cargo_description="Электроника и бытовая техника. Хрупкий груз, требует бережной перевозки.",
        cargo_type='DIRECT',
        cargo_weight=Decimal('2500.00'),
        freight_amount=Decimal('150000.00'),
        freight_payment_type='TRANSFER',
        planned_start_date=now - timedelta(hours=2),
        planned_end_date=now + timedelta(hours=8),
        actual_start_date=now - timedelta(hours=2),
        actual_end_date=None,
        notes="Срочная доставка. Водитель в пути. Ожидается прибытие в 18:00.",
        date=now.date(),
        created_by=admin_user
    )
    print(f"✅ Создан активный заезд ID: {active_trip.id}")
    
    # 2. ЗАЕЗД В ПЛАНЕ
    print("\\n📋 Создание заезда В ПЛАНЕ...")
    planned_trip = Trip.objects.create(
        title="Астана → Шымкент - Продукты питания",
        status='PLANNED',
        vehicle=trucks[1] if trucks.count() > 1 else trucks.first(),
        driver=drivers[1] if drivers.count() > 1 else drivers.first(),
        start_address="Астана, ул. Республики, 789",
        end_address="Шымкент, ул. Тауке хана, 321",
        start_latitude=Decimal('51.1801'),
        start_longitude=Decimal('71.446'),
        end_latitude=Decimal('42.3000'),
        end_longitude=Decimal('69.6000'),
        cargo_description="Продукты питания, молочная продукция. Требуется рефрижератор.",
        cargo_type='DIRECT',
        cargo_weight=Decimal('5000.00'),
        freight_amount=Decimal('200000.00'),
        freight_payment_type='CASH',
        planned_start_date=now + timedelta(days=1, hours=8),
        planned_end_date=now + timedelta(days=1, hours=20),
        actual_start_date=None,
        actual_end_date=None,
        notes="Планируется на завтра. Нужно подготовить документы и чек-лист.",
        date=(now + timedelta(days=1)).date(),
        created_by=admin_user
    )
    print(f"✅ Создан заезд в плане ID: {planned_trip.id}")
    
    # 3. ЗАВЕРШЕННЫЙ ЗАЕЗД
    print("\\n✅ Создание ЗАВЕРШЕННОГО заезда...")
    completed_trip = Trip.objects.create(
        title="Алматы → Караганда - Строительные материалы",
        status='COMPLETED',
        vehicle=trucks[2] if trucks.count() > 2 else trucks.first(),
        driver=drivers[2] if drivers.count() > 2 else drivers.first(),
        start_address="Алматы, ул. Абая, 456",
        end_address="Караганда, ул. Академическая, 789",
        start_latitude=Decimal('43.238949'),
        start_longitude=Decimal('76.889709'),
        end_latitude=Decimal('49.8000'),
        end_longitude=Decimal('73.1000'),
        cargo_description="Строительные материалы, цемент, кирпич. Тяжелый груз.",
        cargo_type='OTHER',
        cargo_weight=Decimal('15000.00'),
        freight_amount=Decimal('180000.00'),
        freight_payment_type='TRANSFER',
        planned_start_date=now - timedelta(days=2, hours=8),
        planned_end_date=now - timedelta(days=1, hours=16),
        actual_start_date=now - timedelta(days=2, hours=8),
        actual_end_date=now - timedelta(days=1, hours=18),
        notes="Заезд успешно завершен. Груз доставлен в срок. Документы подписаны.",
        date=(now - timedelta(days=2)).date(),
        created_by=admin_user
    )
    print(f"✅ Создан завершенный заезд ID: {completed_trip.id}")
    
    print("\\n🎉 Все заезды успешно созданы!")
    print(f"📊 Статистика:")
    print(f"   • Активных заездов: {Trip.objects.filter(status='ACTIVE').count()}")
    print(f"   • Заездов в плане: {Trip.objects.filter(status='PLANNED').count()}")
    print(f"   • Завершенных заездов: {Trip.objects.filter(status='COMPLETED').count()}")
    
    return [active_trip, planned_trip, completed_trip]

if __name__ == '__main__':
    try:
        trips = create_production_trips()
        print("\\n✅ Скрипт выполнен успешно!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)
'''
        
        # Сохраняем скрипт на сервере
        stdin, stdout, stderr = ssh.exec_command(f'cat > /var/www/barlau/create_trips_script.py << "EOF"\n{trip_script}\nEOF')
        
        # Запускаем скрипт
        print("🚀 Запуск скрипта создания заездов...")
        stdin, stdout, stderr = ssh.exec_command('cd /var/www/barlau && source venv/bin/activate && python create_trips_script.py')
        
        # Получаем результат
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if output:
            print("📤 Вывод скрипта:")
            print(output)
        
        if error:
            print("❌ Ошибки:")
            print(error)
        
        # Проверяем созданные заезды
        print("\n🔍 Проверка созданных заездов...")
        stdin, stdout, stderr = ssh.exec_command('cd /var/www/barlau && source venv/bin/activate && python manage.py shell -c "from core.models import Trip; trips = Trip.objects.all().order_by(\'-created_at\')[:3]; print(\'Последние 3 заезда:\'); [print(f\'ID: {t.id}, Статус: {t.get_status_display()}, Название: {t.title}\') for t in trips]"')
        
        output = stdout.read().decode('utf-8')
        if output:
            print("📊 Результат:")
            print(output)
        
        ssh.close()
        print("✅ Работа с сервером завершена!")
        
    except Exception as e:
        print(f"❌ Ошибка подключения к серверу: {e}")

if __name__ == '__main__':
    create_trips_on_production()








































