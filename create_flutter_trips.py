#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from core.models import Trip
from logistics.models import Vehicle
from django.contrib.auth.models import User

def create_flutter_trips():
    """Создает заезды, соответствующие данным из Flutter приложения"""
    
    print("Создание заездов, соответствующих Flutter приложению...")
    
    # Получаем или создаем водителей
    drivers = {}
    driver_data = [
        {'username': 'yunus', 'first_name': 'Юнус', 'last_name': 'Алиев', 'phone': '+7 (777) 159 03 06'},
        {'username': 'arman', 'first_name': 'Арман', 'last_name': 'Вадиев', 'phone': '+7 (777) 123 45 67'},
        {'username': 'gabit', 'first_name': 'Габит', 'last_name': 'Ахметов', 'phone': '+7 (701) 234 56 78'},
        {'username': 'test_driver', 'first_name': 'Тест', 'last_name': 'Водитель', 'phone': '+7 (700) 123 45 67'},
    ]
    
    for driver_info in driver_data:
        user, created = User.objects.get_or_create(
            username=driver_info['username'],
            defaults={
                'first_name': driver_info['first_name'],
                'last_name': driver_info['last_name'],
                'email': f"{driver_info['username']}@barlau.org",
                'is_active': True,
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Создан пользователь: {user.get_full_name()}")
        
        # Устанавливаем роль водителя
        user.profile.role = 'DRIVER'
        user.profile.phone = driver_info['phone']
        user.profile.save()
        drivers[driver_info['first_name']] = user
        print(f"Водитель: {user.get_full_name()}")
    
    # Получаем или создаем грузовики
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
                'year': 2020,
                'status': 'ACTIVE',
            }
        )
        vehicles[vehicle_info['number']] = vehicle
        print(f"Грузовик: {vehicle.number} ({vehicle.brand} {vehicle.model})")
    
    # Данные заездов из Flutter приложения
    trips_data = [
        {
            'vehicle_number': '290 ATL 01',
            'driver_name': 'Юнус',
            'start_location': 'Алматы',
            'end_location': 'Астана',
            'cargo_type': 'Продукты питания',
            'cargo_volume': 15.5,
            'cargo_weight': 12000,
            'trailer_number': 'П 125 ATL 01',
            'border_crossing': 'Нур Жолы',
            'status': 'ACTIVE',
            'start_date': datetime.now() - timedelta(hours=2),
            'estimated_arrival': datetime.now() + timedelta(hours=10),
            'progress': 0.6,
        },
        {
            'vehicle_number': '484 ATL 01',
            'driver_name': 'Арман',
            'start_location': 'Шымкент',
            'end_location': 'Алматы',
            'cargo_type': 'Строительные материалы',
            'cargo_volume': 22.0,
            'cargo_weight': 18000,
            'trailer_number': 'П 347 ATL 01',
            'border_crossing': 'Достык',
            'status': 'ACTIVE',
            'start_date': datetime.now() - timedelta(hours=1, minutes=30),
            'estimated_arrival': datetime.now() + timedelta(hours=7),
            'progress': 0.8,
        },
        {
            'vehicle_number': '533 ATL 01',
            'driver_name': 'Габит',
            'start_location': 'Астана',
            'end_location': 'Караганда',
            'cargo_type': 'Электроника',
            'cargo_volume': 8.5,
            'cargo_weight': 5000,
            'trailer_number': 'П 892 ATL 01',
            'border_crossing': 'Хоргос',
            'status': 'COMPLETED',
            'start_date': datetime.now() - timedelta(days=1),
            'estimated_arrival': datetime.now() - timedelta(hours=3),
            'progress': 1.0,
        },
        {
            'vehicle_number': '290 ATL 02',
            'driver_name': 'Тест',
            'start_location': 'Алматы',
            'end_location': 'Тараз',
            'cargo_type': 'Текстиль',
            'cargo_volume': 12.0,
            'cargo_weight': 8000,
            'trailer_number': 'П 456 ATL 02',
            'border_crossing': 'Кордай',
            'status': 'PLANNED',
            'start_date': datetime.now() + timedelta(hours=1),
            'estimated_arrival': datetime.now() + timedelta(hours=7),
            'progress': 0.0,
        },
    ]
    
    # Создаем заезды
    created_trips = []
    for trip_info in trips_data:
        vehicle = vehicles[trip_info['vehicle_number']]
        driver = drivers[trip_info['driver_name']]
        
        # Координаты для маршрутов (примерные)
        coordinates = {
            'Алматы': {'lat': 43.238949, 'lng': 76.889709},
            'Астана': {'lat': 51.169392, 'lng': 71.449074},
            'Шымкент': {'lat': 42.317442, 'lng': 69.590263},
            'Караганда': {'lat': 49.804705, 'lng': 73.103084},
            'Тараз': {'lat': 42.902834, 'lng': 71.365219},
        }
        
        start_coords = coordinates.get(trip_info['start_location'], {'lat': 43.238949, 'lng': 76.889709})
        end_coords = coordinates.get(trip_info['end_location'], {'lat': 51.169392, 'lng': 71.449074})
        
        trip, created = Trip.objects.get_or_create(
            title=f"Рейс {trip_info['vehicle_number']}",
            vehicle=vehicle,
            driver=driver,
            defaults={
                'status': trip_info['status'],
                'start_latitude': start_coords['lat'],
                'start_longitude': start_coords['lng'],
                'end_latitude': end_coords['lat'],
                'end_longitude': end_coords['lng'],
                'start_address': trip_info['start_location'],
                'end_address': trip_info['end_location'],
                'cargo_description': trip_info['cargo_type'],
                'cargo_type': 'OTHER',
                'cargo_weight': trip_info['cargo_weight'],
                'planned_start_date': trip_info['start_date'],
                'planned_end_date': trip_info['estimated_arrival'],
                'notes': f"Прицеп: {trip_info['trailer_number']}, Пункт пропуска: {trip_info['border_crossing']}",
                'date': trip_info['start_date'].date(),
            }
        )
        
        if created:
            created_trips.append(trip)
            print(f"Создан заезд: {trip.title} ({trip.start_address} → {trip.end_address})")
        else:
            print(f"Заезд уже существует: {trip.title}")
    
    print(f"\nВсего создано заездов: {len(created_trips)}")
    return created_trips

if __name__ == '__main__':
    create_flutter_trips() 
import os
import sys
import django
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from core.models import Trip
from logistics.models import Vehicle
from django.contrib.auth.models import User

def create_flutter_trips():
    """Создает заезды, соответствующие данным из Flutter приложения"""
    
    print("Создание заездов, соответствующих Flutter приложению...")
    
    # Получаем или создаем водителей
    drivers = {}
    driver_data = [
        {'username': 'yunus', 'first_name': 'Юнус', 'last_name': 'Алиев', 'phone': '+7 (777) 159 03 06'},
        {'username': 'arman', 'first_name': 'Арман', 'last_name': 'Вадиев', 'phone': '+7 (777) 123 45 67'},
        {'username': 'gabit', 'first_name': 'Габит', 'last_name': 'Ахметов', 'phone': '+7 (701) 234 56 78'},
        {'username': 'test_driver', 'first_name': 'Тест', 'last_name': 'Водитель', 'phone': '+7 (700) 123 45 67'},
    ]
    
    for driver_info in driver_data:
        user, created = User.objects.get_or_create(
            username=driver_info['username'],
            defaults={
                'first_name': driver_info['first_name'],
                'last_name': driver_info['last_name'],
                'email': f"{driver_info['username']}@barlau.org",
                'is_active': True,
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Создан пользователь: {user.get_full_name()}")
        
        # Устанавливаем роль водителя
        user.profile.role = 'DRIVER'
        user.profile.phone = driver_info['phone']
        user.profile.save()
        drivers[driver_info['first_name']] = user
        print(f"Водитель: {user.get_full_name()}")
    
    # Получаем или создаем грузовики
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
                'year': 2020,
                'status': 'ACTIVE',
            }
        )
        vehicles[vehicle_info['number']] = vehicle
        print(f"Грузовик: {vehicle.number} ({vehicle.brand} {vehicle.model})")
    
    # Данные заездов из Flutter приложения
    trips_data = [
        {
            'vehicle_number': '290 ATL 01',
            'driver_name': 'Юнус',
            'start_location': 'Алматы',
            'end_location': 'Астана',
            'cargo_type': 'Продукты питания',
            'cargo_volume': 15.5,
            'cargo_weight': 12000,
            'trailer_number': 'П 125 ATL 01',
            'border_crossing': 'Нур Жолы',
            'status': 'ACTIVE',
            'start_date': datetime.now() - timedelta(hours=2),
            'estimated_arrival': datetime.now() + timedelta(hours=10),
            'progress': 0.6,
        },
        {
            'vehicle_number': '484 ATL 01',
            'driver_name': 'Арман',
            'start_location': 'Шымкент',
            'end_location': 'Алматы',
            'cargo_type': 'Строительные материалы',
            'cargo_volume': 22.0,
            'cargo_weight': 18000,
            'trailer_number': 'П 347 ATL 01',
            'border_crossing': 'Достык',
            'status': 'ACTIVE',
            'start_date': datetime.now() - timedelta(hours=1, minutes=30),
            'estimated_arrival': datetime.now() + timedelta(hours=7),
            'progress': 0.8,
        },
        {
            'vehicle_number': '533 ATL 01',
            'driver_name': 'Габит',
            'start_location': 'Астана',
            'end_location': 'Караганда',
            'cargo_type': 'Электроника',
            'cargo_volume': 8.5,
            'cargo_weight': 5000,
            'trailer_number': 'П 892 ATL 01',
            'border_crossing': 'Хоргос',
            'status': 'COMPLETED',
            'start_date': datetime.now() - timedelta(days=1),
            'estimated_arrival': datetime.now() - timedelta(hours=3),
            'progress': 1.0,
        },
        {
            'vehicle_number': '290 ATL 02',
            'driver_name': 'Тест',
            'start_location': 'Алматы',
            'end_location': 'Тараз',
            'cargo_type': 'Текстиль',
            'cargo_volume': 12.0,
            'cargo_weight': 8000,
            'trailer_number': 'П 456 ATL 02',
            'border_crossing': 'Кордай',
            'status': 'PLANNED',
            'start_date': datetime.now() + timedelta(hours=1),
            'estimated_arrival': datetime.now() + timedelta(hours=7),
            'progress': 0.0,
        },
    ]
    
    # Создаем заезды
    created_trips = []
    for trip_info in trips_data:
        vehicle = vehicles[trip_info['vehicle_number']]
        driver = drivers[trip_info['driver_name']]
        
        # Координаты для маршрутов (примерные)
        coordinates = {
            'Алматы': {'lat': 43.238949, 'lng': 76.889709},
            'Астана': {'lat': 51.169392, 'lng': 71.449074},
            'Шымкент': {'lat': 42.317442, 'lng': 69.590263},
            'Караганда': {'lat': 49.804705, 'lng': 73.103084},
            'Тараз': {'lat': 42.902834, 'lng': 71.365219},
        }
        
        start_coords = coordinates.get(trip_info['start_location'], {'lat': 43.238949, 'lng': 76.889709})
        end_coords = coordinates.get(trip_info['end_location'], {'lat': 51.169392, 'lng': 71.449074})
        
        trip, created = Trip.objects.get_or_create(
            title=f"Рейс {trip_info['vehicle_number']}",
            vehicle=vehicle,
            driver=driver,
            defaults={
                'status': trip_info['status'],
                'start_latitude': start_coords['lat'],
                'start_longitude': start_coords['lng'],
                'end_latitude': end_coords['lat'],
                'end_longitude': end_coords['lng'],
                'start_address': trip_info['start_location'],
                'end_address': trip_info['end_location'],
                'cargo_description': trip_info['cargo_type'],
                'cargo_type': 'OTHER',
                'cargo_weight': trip_info['cargo_weight'],
                'planned_start_date': trip_info['start_date'],
                'planned_end_date': trip_info['estimated_arrival'],
                'notes': f"Прицеп: {trip_info['trailer_number']}, Пункт пропуска: {trip_info['border_crossing']}",
                'date': trip_info['start_date'].date(),
            }
        )
        
        if created:
            created_trips.append(trip)
            print(f"Создан заезд: {trip.title} ({trip.start_address} → {trip.end_address})")
        else:
            print(f"Заезд уже существует: {trip.title}")
    
    print(f"\nВсего создано заездов: {len(created_trips)}")
    return created_trips

if __name__ == '__main__':
    create_flutter_trips() 
 
 