#!/usr/bin/env python3
"""
Скрипт для синхронизации данных заездов с продакшн сервера
"""

import os
import sys
import django
import requests
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from core.models import Trip
from logistics.models import Vehicle
from accounts.models import User

def fetch_production_trips():
    """Получаем заезды с продакшн сервера"""
    try:
        # Используем тот же токен, что и в Flutter
        headers = {
            'Authorization': 'Bearer demo_token_for_web',
            'Content-Type': 'application/json'
        }
        
        response = requests.get('https://barlau.org/api/trips/', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Получено {len(data.get('data', []))} заездов с продакшн сервера")
            return data.get('data', [])
        else:
            print(f"❌ Ошибка получения данных: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка подключения к продакшн серверу: {e}")
        return []

def sync_trips_data():
    """Синхронизируем данные заездов"""
    print("🔄 Начинаем синхронизацию данных заездов...")
    
    # Получаем данные с продакшн сервера
    production_trips = fetch_production_trips()
    
    if not production_trips:
        print("❌ Не удалось получить данные с продакшн сервера")
        return
    
    # Очищаем существующие заезды
    Trip.objects.all().delete()
    print("🗑️ Удалены существующие заезды")
    
    # Создаем новые заезды
    created_count = 0
    
    for trip_data in production_trips:
        try:
            # Получаем или создаем водителя
            driver_details = trip_data.get('driver_details', {})
            if driver_details:
                driver, created = User.objects.get_or_create(
                    first_name=driver_details.get('first_name', ''),
                    last_name=driver_details.get('last_name', ''),
                    defaults={
                        'phone': driver_details.get('phone', ''),
                        'role': 'DRIVER',
                        'username': f"driver_{driver_details.get('first_name', '').lower()}_{driver_details.get('last_name', '').lower()}",
                        'email': f"driver_{driver_details.get('first_name', '').lower()}_{driver_details.get('last_name', '').lower()}@barlau.kz"
                    }
                )
            else:
                driver = None
            
            # Получаем или создаем грузовик
            vehicle_details = trip_data.get('vehicle_details', {})
            if vehicle_details:
                vehicle, created = Vehicle.objects.get_or_create(
                    number=vehicle_details.get('number', ''),
                    defaults={
                        'brand': vehicle_details.get('brand', ''),
                        'model': vehicle_details.get('model', ''),
                        'year': datetime.now().year
                    }
                )
            else:
                vehicle = None
            
            # Создаем заезд
            trip = Trip.objects.create(
                id=trip_data.get('id'),
                vehicle=vehicle,
                driver=driver,
                status=trip_data.get('status', 'PLANNED'),
                start_address=trip_data.get('start_address', ''),
                end_address=trip_data.get('end_address', ''),
                cargo_description=trip_data.get('cargo_description', ''),
                cargo_weight=trip_data.get('cargo_weight', 0),
                planned_start_date=trip_data.get('planned_start_date'),
                planned_end_date=trip_data.get('planned_end_date')
            )
            
            created_count += 1
            print(f"✅ Создан заезд ID {trip.id}: {trip.start_address} → {trip.end_address}")
            
        except Exception as e:
            print(f"❌ Ошибка создания заезда {trip_data.get('id')}: {e}")
    
    print(f"🎉 Синхронизация завершена! Создано {created_count} заездов")
    
    # Выводим список активных заездов
    active_trips = Trip.objects.filter(status__in=['ACTIVE', 'PLANNED'])
    print(f"📊 Активных заездов: {active_trips.count()}")
    print("ID активных заездов:", ", ".join(str(t.id) for t in active_trips))

if __name__ == '__main__':
    sync_trips_data() 