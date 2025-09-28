#!/usr/bin/env python3
"""
Скрипт для подключения GPS трекеров к четырем грузовикам
"""

import os
import sys
import django
from django.conf import settings

# Настройка Django
sys.path.append('/Users/almaty/cursors/maro')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from logistics.models import Vehicle
from datetime import datetime
from django.utils import timezone

def setup_gps_trackers():
    """
    Подключение GPS трекеров к четырем грузовикам
    """
    print("🛰️ Настройка GPS трекеров для четырех грузовиков")
    print("=" * 60)
    
    # Список грузовиков для подключения GPS трекеров
    vehicles_to_setup = [
        {
            'number': '484 ATL 01',
            'gps_device_id': '484001',
            'gps_imei': '861234567890001',
            'gps_phone': '+77001234501',
            'description': 'Основной грузовик Volvo FH'
        },
        {
            'number': '290 ATL 01', 
            'gps_device_id': '290001',
            'gps_imei': '861234567890002',
            'gps_phone': '+77001234502',
            'description': 'Грузовик DAF XF 106'
        },
        {
            'number': '533 ATL 01',
            'gps_device_id': '533001', 
            'gps_imei': '861234567890003',
            'gps_phone': '+77001234503',
            'description': 'Грузовик Mercedes Actros'
        },
        {
            'number': '290 ATL 02',
            'gps_device_id': '290002',
            'gps_imei': '861234567890004', 
            'gps_phone': '+77001234504',
            'description': 'Грузовик DAF XF 106 (второй)'
        }
    ]
    
    success_count = 0
    
    for vehicle_data in vehicles_to_setup:
        try:
            # Ищем грузовик по номеру
            vehicle = Vehicle.objects.get(number=vehicle_data['number'])
            
            print(f"\n🚛 Настройка GPS для {vehicle_data['number']} ({vehicle_data['description']})")
            print(f"   ID грузовика: {vehicle.id}")
            print(f"   Марка/Модель: {vehicle.brand} {vehicle.model}")
            
            # Обновляем GPS данные
            vehicle.gps_device_id = vehicle_data['gps_device_id']
            vehicle.gps_imei = vehicle_data['gps_imei']
            vehicle.gps_phone = vehicle_data['gps_phone']
            vehicle.gps_enabled = True
            vehicle.gps_last_update = timezone.now()
            
            # Устанавливаем начальные координаты (Алматы)
            vehicle.gps_latitude = 43.2220
            vehicle.gps_longitude = 76.8512
            vehicle.gps_speed = 0.0
            vehicle.gps_heading = 0.0
            vehicle.gps_altitude = 785.0
            vehicle.gps_satellites = 8
            vehicle.gps_signal_quality = 'good'
            vehicle.gps_fuel_level = 75.0
            vehicle.gps_engine_status = False
            vehicle.gps_ignition_status = False
            
            vehicle.save()
            
            print(f"   ✅ GPS трекер подключен:")
            print(f"      - Device ID: {vehicle_data['gps_device_id']}")
            print(f"      - IMEI: {vehicle_data['gps_imei']}")
            print(f"      - Phone: {vehicle_data['gps_phone']}")
            print(f"      - Координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
            
            success_count += 1
            
        except Vehicle.DoesNotExist:
            print(f"   ❌ Грузовик {vehicle_data['number']} не найден в базе данных")
        except Exception as e:
            print(f"   ❌ Ошибка настройки GPS для {vehicle_data['number']}: {e}")
    
    print(f"\n📊 Результат настройки:")
    print(f"   ✅ Успешно настроено: {success_count}/{len(vehicles_to_setup)} грузовиков")
    
    if success_count > 0:
        print(f"\n🛰️ GPS трекеры активны для {success_count} грузовиков")
        print("   Теперь можно отслеживать их местоположение через API")
        
        # Показываем обновленные данные
        print(f"\n📋 Список грузовиков с GPS:")
        gps_vehicles = Vehicle.objects.filter(gps_enabled=True)
        for vehicle in gps_vehicles:
            print(f"   🚛 {vehicle.number}: {vehicle.brand} {vehicle.model}")
            print(f"      GPS ID: {vehicle.gps_device_id}, IMEI: {vehicle.gps_imei}")
            print(f"      Координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
            print(f"      Последнее обновление: {vehicle.gps_last_update}")
    
    return success_count

def verify_gps_setup():
    """
    Проверка настроенных GPS трекеров
    """
    print(f"\n🔍 Проверка настроенных GPS трекеров:")
    print("=" * 60)
    
    gps_vehicles = Vehicle.objects.filter(gps_enabled=True)
    
    if not gps_vehicles.exists():
        print("   ❌ Нет грузовиков с активными GPS трекерами")
        return False
    
    print(f"   📊 Найдено {gps_vehicles.count()} грузовиков с GPS:")
    
    for vehicle in gps_vehicles:
        status_icon = "🟢" if vehicle.gps_last_update else "🔴"
        print(f"   {status_icon} {vehicle.number}: {vehicle.brand} {vehicle.model}")
        print(f"      Device ID: {vehicle.gps_device_id}")
        print(f"      IMEI: {vehicle.gps_imei}")
        print(f"      Phone: {vehicle.gps_phone}")
        if vehicle.gps_latitude and vehicle.gps_longitude:
            print(f"      Координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
        print(f"      Последнее обновление: {vehicle.gps_last_update}")
        print()
    
    return True

def main():
    """
    Основная функция
    """
    print("🚀 Запуск настройки GPS трекеров")
    print("=" * 60)
    
    # Настраиваем GPS трекеры
    success_count = setup_gps_trackers()
    
    if success_count > 0:
        # Проверяем результат
        verify_gps_setup()
        
        print(f"\n✅ Настройка GPS трекеров завершена успешно!")
        print(f"   Подключено трекеров: {success_count}")
        print(f"   Теперь можно использовать GPS мониторинг через API")
        
        # Показываем доступные API endpoints
        print(f"\n🌐 Доступные GPS API endpoints:")
        print(f"   - GET /api/gps/vehicles/with-gps/ - Список грузовиков с GPS")
        print(f"   - GET /api/gps/vehicles/<id>/status/ - Статус конкретного грузовика")
        print(f"   - POST /api/gps/vehicles/<id>/sync/ - Синхронизация GPS данных")
        print(f"   - GET /api/gps/devices/available/ - Доступные GPS устройства")
        
    else:
        print(f"\n❌ Не удалось настроить GPS трекеры")
        print(f"   Проверьте номера грузовиков в базе данных")

if __name__ == "__main__":
    main()
