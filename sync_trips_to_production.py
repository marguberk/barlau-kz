#!/usr/bin/env python3
"""
Скрипт для синхронизации заездов с продакшеном
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from core.models import Trip
from logistics.models import Vehicle
from accounts.models import User

# Настройки продакшн сервера
PROD_API_BASE = 'https://barlau.org/api'
PROD_TOKEN = 'demo_token_for_web'

def sync_trips_to_production():
    """Синхронизация заездов с продакшеном"""
    print("🚛 Синхронизация заездов с продакшеном...")
    
    # Получаем последние 3 заезда (которые мы создали)
    local_trips = Trip.objects.all().order_by('-created_at')[:3]
    print(f"📊 Найдено заездов для синхронизации: {local_trips.count()}")
    
    for trip in local_trips:
        print(f"\n📦 Синхронизация заезда: {trip.title}")
        
        # Подготавливаем данные заезда
        trip_data = {
            'title': trip.title,
            'status': trip.status,
            'vehicle': trip.vehicle.id if trip.vehicle else None,
            'driver': trip.driver.id if trip.driver else None,
            'start_address': trip.start_address,
            'end_address': trip.end_address,
            'start_latitude': float(trip.start_latitude) if trip.start_latitude else None,
            'start_longitude': float(trip.start_longitude) if trip.start_longitude else None,
            'end_latitude': float(trip.end_latitude) if trip.end_latitude else None,
            'end_longitude': float(trip.end_longitude) if trip.end_longitude else None,
            'cargo_description': trip.cargo_description,
            'cargo_type': trip.cargo_type,
            'cargo_weight': float(trip.cargo_weight) if trip.cargo_weight else None,
            'freight_amount': float(trip.freight_amount) if trip.freight_amount else None,
            'freight_payment_type': trip.freight_payment_type,
            'planned_start_date': trip.planned_start_date.isoformat() if trip.planned_start_date else None,
            'planned_end_date': trip.planned_end_date.isoformat() if trip.planned_end_date else None,
            'actual_start_date': trip.actual_start_date.isoformat() if trip.actual_start_date else None,
            'actual_end_date': trip.actual_end_date.isoformat() if trip.actual_end_date else None,
            'notes': trip.notes,
            'date': trip.date.isoformat() if trip.date else None,
            'created_by': trip.created_by.id if trip.created_by else None,
        }
        
        try:
            # Отправляем на продакшн
            response = requests.post(
                f'{PROD_API_BASE}/trips/',
                headers={
                    'Authorization': f'Bearer {PROD_TOKEN}',
                    'Content-Type': 'application/json'
                },
                json=trip_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Заезд '{trip.title}' успешно синхронизирован")
                print(f"   Статус: {trip.get_status_display()}")
                print(f"   Грузовик: {trip.vehicle}")
                print(f"   Водитель: {trip.driver}")
            else:
                print(f"❌ Ошибка синхронизации заезда '{trip.title}': {response.status_code}")
                print(f"   Ответ: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка сети при синхронизации заезда '{trip.title}': {e}")
        except Exception as e:
            print(f"❌ Общая ошибка при синхронизации заезда '{trip.title}': {e}")
    
    print("\n🎉 Синхронизация завершена!")

if __name__ == '__main__':
    try:
        sync_trips_to_production()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)








































