#!/usr/bin/env python3
"""
Тестовый скрипт для проверки отображения местоположения водителей
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import DriverLocation, Trip

User = get_user_model()

def test_driver_locations():
    """Тестируем местоположения водителей"""
    print("🧪 Тестирование местоположений водителей")
    print("=" * 50)
    
    # Получаем всех водителей
    drivers = User.objects.filter(role='DRIVER')
    print(f"📊 Найдено {len(drivers)} водителей:")
    
    for driver in drivers:
        print(f"  👤 {driver.get_full_name()} (ID: {driver.id})")
        
        # Получаем последнее местоположение
        last_location = DriverLocation.objects.filter(driver=driver).order_by('-timestamp').first()
        
        if last_location:
            print(f"    📍 Последнее местоположение: {last_location.latitude}, {last_location.longitude}")
            print(f"    🕐 Время: {last_location.timestamp}")
            print(f"    🚛 Заезд: {last_location.trip.id if last_location.trip else 'Не указан'}")
        else:
            print(f"    ❌ Нет данных о местоположении")
        print()
    
    # Получаем заезды с водителями
    trips_with_drivers = Trip.objects.filter(driver__isnull=False).select_related('driver')
    print(f"🚛 Найдено {len(trips_with_drivers)} заездов с водителями:")
    
    for trip in trips_with_drivers[:5]:  # Показываем первые 5
        print(f"  🚛 Заезд #{trip.id}: {trip.driver.get_full_name()}")
        
        # Проверяем местоположение водителя для этого заезда
        driver_location = DriverLocation.objects.filter(
            driver=trip.driver,
            trip=trip
        ).order_by('-timestamp').first()
        
        if driver_location:
            print(f"    📍 Местоположение: {driver_location.latitude}, {driver_location.longitude}")
            print(f"    🕐 Время: {driver_location.timestamp}")
        else:
            # Проверяем общее местоположение водителя
            general_location = DriverLocation.objects.filter(
                driver=trip.driver
            ).order_by('-timestamp').first()
            
            if general_location:
                print(f"    📍 Общее местоположение: {general_location.latitude}, {general_location.longitude}")
                print(f"    🕐 Время: {general_location.timestamp}")
            else:
                print(f"    ❌ Нет данных о местоположении")
        print()

def create_test_driver_location():
    """Создаем тестовое местоположение водителя"""
    print("🔧 Создание тестового местоположения водителя")
    print("=" * 50)
    
    # Получаем первого водителя
    driver = User.objects.filter(role='DRIVER').first()
    
    if not driver:
        print("❌ Водители не найдены")
        return
    
    # Получаем первый заезд этого водителя
    trip = Trip.objects.filter(driver=driver).first()
    
    if not trip:
        print(f"❌ Заезды для водителя {driver.get_full_name()} не найдены")
        return
    
    # Создаем тестовое местоположение (Алматы)
    test_location = DriverLocation.objects.create(
        driver=driver,
        trip=trip,
        latitude=43.222000,
        longitude=76.851200
    )
    
    print(f"✅ Создано тестовое местоположение:")
    print(f"  👤 Водитель: {driver.get_full_name()}")
    print(f"  🚛 Заезд: #{trip.id}")
    print(f"  📍 Координаты: {test_location.latitude}, {test_location.longitude}")
    print(f"  🕐 Время: {test_location.timestamp}")

if __name__ == "__main__":
    print("🚀 Запуск тестирования местоположений водителей")
    print()
    
    # Тестируем существующие данные
    test_driver_locations()
    
    # Создаем тестовое местоположение
    create_test_driver_location()
    
    print("✅ Тестирование завершено!")
