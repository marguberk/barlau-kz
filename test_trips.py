#!/usr/bin/env python3
"""
Скрипт для проверки данных заездов
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from core.models import Trip

def check_trips():
    """Проверяем данные заездов"""
    print("🔍 Проверяем данные заездов...")
    
    # Получаем все заезды
    trips = Trip.objects.all()
    print(f"📊 Всего заездов в базе: {trips.count()}")
    
    # Получаем активные заезды
    active_trips = Trip.objects.filter(status__in=['ACTIVE', 'PLANNED'])
    print(f"📊 Активных заездов: {active_trips.count()}")
    
    if active_trips.exists():
        print("ID активных заездов:", ", ".join(str(t.id) for t in active_trips))
        
        # Показываем детали каждого заезда
        for trip in active_trips:
            print(f"\n🚛 Заезд ID {trip.id}:")
            print(f"   Статус: {trip.status}")
            print(f"   Маршрут: {trip.start_address} → {trip.end_address}")
            print(f"   Грузовик: {trip.vehicle.number if trip.vehicle else 'Не указан'}")
            print(f"   Водитель: {trip.driver.get_full_name() if trip.driver else 'Не указан'}")
            print(f"   Дата: {trip.planned_start_date}")
    else:
        print("❌ Активных заездов не найдено")

if __name__ == '__main__':
    check_trips() 