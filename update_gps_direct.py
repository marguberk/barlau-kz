#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime

# Настройка Django
sys.path.append('/Users/almaty/cursors/maro')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle
from django.utils import timezone

def update_gps_direct():
    """Обновляем GPS данные напрямую с реальными координатами"""
    print("🛰️ Прямое обновление GPS данных")
    print("=" * 60)
    
    # Реальные GPS данные из Wialon (получены из детального анализа)
    gps_data = {
        "484 ATL 01": {
            "latitude": 41.1863623935,
            "longitude": 69.2052327118,
            "speed": 0,
            "heading": 94,
            "altitude": 0,
            "satellites": 19,
            "device_id": "29603155"
        },
        "290 ATL 01": {
            "latitude": 44.1487121941,
            "longitude": 80.0000004051,
            "speed": 0,
            "heading": 310,
            "altitude": 0,
            "satellites": 11,
            "device_id": "29682916"
        },
        "533 ATL 01": {
            "latitude": 44.1482092589,
            "longitude": 79.9998858664,
            "speed": 0,
            "heading": 142,
            "altitude": 0,
            "satellites": 18,
            "device_id": "29682864"
        },
        "290 ATL 02": {
            "latitude": 44.1847730065,
            "longitude": 80.4069515272,
            "speed": 0,
            "heading": 177,
            "altitude": 0,
            "satellites": 12,
            "device_id": "29682886"
        }
    }
    
    updated_count = 0
    
    for vehicle_number, gps_info in gps_data.items():
        try:
            # Находим грузовик в базе
            vehicle = Vehicle.objects.get(number=vehicle_number)
            print(f"\n🚛 Обновляем {vehicle_number}...")
            
            # Обновляем GPS данные
            vehicle.gps_enabled = True
            vehicle.gps_device_id = gps_info["device_id"]
            vehicle.gps_latitude = gps_info["latitude"]
            vehicle.gps_longitude = gps_info["longitude"]
            vehicle.gps_speed = gps_info["speed"]
            vehicle.gps_heading = gps_info["heading"]
            vehicle.gps_altitude = gps_info["altitude"]
            vehicle.gps_satellites = gps_info["satellites"]
            vehicle.gps_signal_quality = 'good' if gps_info["satellites"] > 4 else 'poor'
            vehicle.gps_last_update = timezone.now()
            
            # Статус двигателя и зажигания
            speed = float(vehicle.gps_speed) if vehicle.gps_speed else 0
            vehicle.gps_engine_status = speed > 1.0
            vehicle.gps_ignition_status = speed > 0.5
            
            vehicle.save()
            
            print(f"   ✅ Обновлено:")
            print(f"      📍 Координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
            print(f"      🚗 Скорость: {vehicle.gps_speed} км/ч")
            print(f"      🧭 Направление: {vehicle.gps_heading}°")
            print(f"      🛰️ Спутники: {vehicle.gps_satellites}")
            print(f"      🔋 Двигатель: {'Включен' if vehicle.gps_engine_status else 'Выключен'}")
            print(f"      📡 Качество сигнала: {vehicle.gps_signal_quality}")
            
            updated_count += 1
            
        except Vehicle.DoesNotExist:
            print(f"   ❌ Грузовик {vehicle_number} не найден в базе данных")
        except Exception as e:
            print(f"   ❌ Ошибка обновления {vehicle_number}: {e}")
    
    print(f"\n📊 ИТОГИ:")
    print(f"   ✅ Обновлено грузовиков: {updated_count}")
    print(f"   📱 Всего GPS устройств: {len(gps_data)}")
    
    return updated_count > 0

def verify_gps_data():
    """Проверяем обновленные GPS данные"""
    print(f"\n🔍 ПРОВЕРКА ОБНОВЛЕННЫХ GPS ДАННЫХ")
    print("=" * 60)
    
    vehicles_with_gps = Vehicle.objects.filter(gps_enabled=True)
    print(f"📱 Грузовиков с GPS: {vehicles_with_gps.count()}")
    
    for vehicle in vehicles_with_gps:
        print(f"\n🚛 {vehicle.number}:")
        print(f"   Device ID: {vehicle.gps_device_id}")
        print(f"   Последнее обновление: {vehicle.gps_last_update}")
        if vehicle.gps_latitude and vehicle.gps_longitude:
            print(f"   📍 Координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
            print(f"   🚗 Скорость: {vehicle.gps_speed} км/ч")
            print(f"   🧭 Направление: {vehicle.gps_heading}°")
            print(f"   🛰️ Спутники: {vehicle.gps_satellites}")
            print(f"   🔋 Двигатель: {'Включен' if vehicle.gps_engine_status else 'Выключен'}")
            print(f"   📡 Качество сигнала: {vehicle.gps_signal_quality}")
        else:
            print(f"   ⚠️ Нет GPS координат")

def test_map_integration():
    """Тестируем интеграцию с картой"""
    print(f"\n🗺️ ТЕСТИРОВАНИЕ ИНТЕГРАЦИИ С КАРТОЙ")
    print("=" * 60)
    
    vehicles_with_gps = Vehicle.objects.filter(gps_enabled=True, gps_latitude__isnull=False, gps_longitude__isnull=False)
    
    print(f"📱 Грузовиков с координатами: {vehicles_with_gps.count()}")
    
    for vehicle in vehicles_with_gps:
        print(f"\n🚛 {vehicle.number}:")
        print(f"   📍 Координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
        print(f"   🗺️ Google Maps: https://maps.google.com/?q={vehicle.gps_latitude},{vehicle.gps_longitude}")
        print(f"   🗺️ Yandex Maps: https://yandex.ru/maps/?pt={vehicle.gps_longitude},{vehicle.gps_latitude}&z=16&l=map")

if __name__ == "__main__":
    print("🛰️ ПРЯМАЯ ИНТЕГРАЦИЯ GPS ДАННЫХ")
    print("=" * 80)
    
    # Обновляем GPS данные
    success = update_gps_direct()
    
    if success:
        # Проверяем результат
        verify_gps_data()
        
        # Тестируем интеграцию с картой
        test_map_integration()
        
        print(f"\n✅ GPS данные успешно интегрированы в систему!")
        print(f"🗺️ Теперь грузовики можно отслеживать на карте!")
    else:
        print(f"\n❌ Не удалось интегрировать GPS данные")

