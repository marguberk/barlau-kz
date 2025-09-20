#!/usr/bin/env python
"""
Простой скрипт для проверки грузовиков
"""

import os
import sys
import django

# Настройка Django
sys.path.append('/Users/almaty/cursors/maro')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle, VehiclePhoto

def check_vehicles():
    """Показывает список грузовиков и их фотографии"""
    vehicles = Vehicle.objects.all()
    
    print("📋 Список грузовиков:")
    print("-" * 80)
    
    for vehicle in vehicles:
        has_main_photo = bool(vehicle.photo)
        has_photos = vehicle.photos.exists()
        main_photo_url = vehicle.main_photo_url
        
        status = "✅" if (has_main_photo or has_photos) else "❌"
        print(f"{status} {vehicle.number} - {vehicle.brand} {vehicle.model} ({vehicle.year})")
        print(f"   Основное фото: {'✅' if has_main_photo else '❌'}")
        print(f"   Дополнительные фото: {vehicle.photos.count()}")
        print(f"   main_photo_url: {main_photo_url}")
        print()
    
    print("-" * 80)
    print(f"Всего грузовиков: {vehicles.count()}")
    print(f"С основным фото: {vehicles.filter(photo__isnull=False).count()}")
    print(f"С дополнительными фото: {vehicles.filter(photos__isnull=False).distinct().count()}")

if __name__ == "__main__":
    check_vehicles() 
    if vehicles.count() > 0:
        print('Список транспорта:')
        for v in vehicles:
            driver_name = v.driver.get_full_name() if v.driver else 'Не назначен'
            print(f'- {v.number} ({v.brand} {v.model}), статус: {v.status}, водитель: {driver_name}')
    else:
        print('Транспорт не найден в базе данных')

if __name__ == '__main__':
    main() 