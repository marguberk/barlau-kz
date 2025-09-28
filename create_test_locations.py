#!/usr/bin/env python3
"""
Создание тестовых местоположений водителей для демонстрации
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import DriverLocation, Trip
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def create_test_locations():
    """Создаем тестовые местоположения для разных водителей"""
    print("🔧 Создание тестовых местоположений водителей")
    print("=" * 50)
    
    # Координаты разных мест в Казахстане
    locations = [
        {"name": "Алматы", "lat": 43.222000, "lng": 76.851200},
        {"name": "Астана", "lat": 51.169400, "lng": 71.449100},
        {"name": "Шымкент", "lat": 42.300000, "lng": 69.600000},
        {"name": "Актау", "lat": 43.650000, "lng": 51.200000},
        {"name": "Актобе", "lat": 50.283300, "lng": 57.216700},
    ]
    
    # Получаем всех водителей
    drivers = User.objects.filter(role='DRIVER')
    
    if not drivers.exists():
        print("❌ Водители не найдены")
        return
    
    created_count = 0
    
    for i, driver in enumerate(drivers[:5]):  # Берем первых 5 водителей
        # Получаем последний заезд этого водителя
        trip = Trip.objects.filter(driver=driver).order_by('-created_at').first()
        
        if not trip:
            print(f"⚠️ Нет заездов для водителя {driver.get_full_name()}")
            continue
        
        # Выбираем координаты для этого водителя
        location = locations[i % len(locations)]
        
        # Создаем местоположение с разным временем (от 1 до 5 часов назад)
        hours_ago = i + 1
        timestamp = timezone.now() - timedelta(hours=hours_ago)
        
        driver_location = DriverLocation.objects.create(
            driver=driver,
            trip=trip,
            latitude=location["lat"],
            longitude=location["lng"],
            timestamp=timestamp
        )
        
        print(f"✅ Создано местоположение:")
        print(f"  👤 Водитель: {driver.get_full_name()}")
        print(f"  🚛 Заезд: #{trip.id}")
        print(f"  📍 Место: {location['name']} ({driver_location.latitude}, {driver_location.longitude})")
        print(f"  🕐 Время: {driver_location.timestamp}")
        print()
        
        created_count += 1
    
    print(f"🎯 Создано {created_count} тестовых местоположений")

if __name__ == "__main__":
    create_test_locations()
