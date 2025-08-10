#!/usr/bin/env python3
"""
Скрипт для создания демо заездов на основе данных из Flutter
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from core.models import Trip
from logistics.models import Vehicle
from accounts.models import User

def create_demo_trips():
    """Создаем демо заезды на основе данных из Flutter"""
    print("🔄 Создаем демо заезды...")
    
    # Очищаем существующие заезды
    Trip.objects.all().delete()
    print("🗑️ Удалены существующие заезды")
    
    # Создаем или получаем водителей
    drivers = {}
    driver_data = [
        {'first_name': 'Юнус', 'last_name': 'Алиев', 'phone': '+7 (777) 159 03 06'},
        {'first_name': 'Арман', 'last_name': 'Вадиев', 'phone': '+7 (777) 123 45 67'},
        {'first_name': 'Габит', 'last_name': 'Ахметов', 'phone': '+7 (701) 234 56 78'},
        {'first_name': 'Тест', 'last_name': 'Водитель', 'phone': '+7 (700) 123 45 67'},
    ]
    
    for driver_info in driver_data:
        driver, created = User.objects.get_or_create(
            first_name=driver_info['first_name'],
            last_name=driver_info['last_name'],
            defaults={
                'phone': driver_info['phone'],
                'role': 'DRIVER',
                'username': f"driver_{driver_info['first_name'].lower()}_{driver_info['last_name'].lower()}",
                'email': f"driver_{driver_info['first_name'].lower()}_{driver_info['last_name'].lower()}@barlau.kz"
            }
        )
        drivers[f"{driver_info['first_name']} {driver_info['last_name']}"] = driver
        if created:
            print(f"✅ Создан водитель: {driver.get_full_name()}")
    
    # Создаем или получаем грузовики
    vehicles = {}
    vehicle_data = [
        {'number': '290 ATL 01', 'brand': 'DAF', 'model': 'XF 106'},
        {'number': '484 ATL 01', 'brand': 'Volvo', 'model': 'FH'},
        {'number': '533 ATL 01', 'brand': 'Mercedes', 'model': 'Actros'},
        {'number': '290 ATL 02', 'brand': 'DAF', 'model': 'XF 106'},
    ]
    
    for vehicle_info in vehicle_data:
        vehicle, created = Vehicle.objects.get_or_create(
            number=vehicle_info['number'],
            defaults={
                'brand': vehicle_info['brand'],
                'model': vehicle_info['model'],
                'year': datetime.now().year
            }
        )
        vehicles[vehicle_info['number']] = vehicle
        if created:
            print(f"✅ Создан грузовик: {vehicle.number}")
    
    # Создаем заезды на основе данных из Flutter
    trips_data = [
        {
            'id': 1,
            'vehicle_number': '290 ATL 01',
            'driver_name': 'Юнус Алиев',
            'status': 'ACTIVE',
            'start_address': 'Алматы',
            'end_address': 'Астана',
            'cargo_description': 'Продукты питания',
            'cargo_weight': 12000,
            'planned_start_date': datetime.now() - timedelta(hours=2),
            'planned_end_date': datetime.now() + timedelta(hours=8)
        },
        {
            'id': 2,
            'vehicle_number': '484 ATL 01',
            'driver_name': 'Арман Вадиев',
            'status': 'ACTIVE',
            'start_address': 'Шымкент',
            'end_address': 'Алматы',
            'cargo_description': 'Строительные материалы',
            'cargo_weight': 18000,
            'planned_start_date': datetime.now() - timedelta(hours=1, minutes=30),
            'planned_end_date': datetime.now() + timedelta(hours=6, minutes=30)
        },
        {
            'id': 3,
            'vehicle_number': '533 ATL 01',
            'driver_name': 'Габит Ахметов',
            'status': 'COMPLETED',
            'start_address': 'Астана',
            'end_address': 'Караганда',
            'cargo_description': 'Электроника',
            'cargo_weight': 5000,
            'planned_start_date': datetime.now() - timedelta(days=1, hours=14),
            'planned_end_date': datetime.now() - timedelta(days=1, hours=8)
        },
        {
            'id': 4,
            'vehicle_number': '290 ATL 02',
            'driver_name': 'Тест Водитель',
            'status': 'PLANNED',
            'start_address': 'Алматы',
            'end_address': 'Тараз',
            'cargo_description': 'Текстиль',
            'cargo_weight': 8000,
            'planned_start_date': datetime.now() + timedelta(hours=1),
            'planned_end_date': datetime.now() + timedelta(hours=7)
        }
    ]
    
    created_count = 0
    for trip_info in trips_data:
        try:
            vehicle = vehicles.get(trip_info['vehicle_number'])
            driver = drivers.get(trip_info['driver_name'])
            
            trip = Trip.objects.create(
                id=trip_info['id'],
                vehicle=vehicle,
                driver=driver,
                status=trip_info['status'],
                start_address=trip_info['start_address'],
                end_address=trip_info['end_address'],
                start_latitude=43.238949,  # Координаты Алматы
                start_longitude=76.889709,
                end_latitude=51.1801,     # Координаты Астаны
                end_longitude=71.446,
                cargo_description=trip_info['cargo_description'],
                cargo_weight=trip_info['cargo_weight'],
                planned_start_date=trip_info['planned_start_date'],
                planned_end_date=trip_info['planned_end_date']
            )
            
            created_count += 1
            print(f"✅ Создан заезд ID {trip.id}: {trip.start_address} → {trip.end_address}")
            
        except Exception as e:
            print(f"❌ Ошибка создания заезда {trip_info['id']}: {e}")
    
    print(f"🎉 Создание завершено! Создано {created_count} заездов")
    
    # Выводим список активных заездов
    active_trips = Trip.objects.filter(status__in=['ACTIVE', 'PLANNED'])
    print(f"📊 Активных заездов: {active_trips.count()}")
    print("ID активных заездов:", ", ".join(str(t.id) for t in active_trips))

if __name__ == '__main__':
    create_demo_trips() 