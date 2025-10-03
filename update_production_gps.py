#!/usr/bin/env python3
"""
Скрипт для обновления GPS данных на продакшн сервере
"""
import os
import django
from datetime import datetime
from django.utils import timezone

# Настройка Django для продакшн
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle

def update_production_gps_data():
    """Обновляем GPS данные на продакшн сервере с реальными координатами из Wialon"""
    print("🛰️ Обновление GPS данных на продакшн сервере")
    print("=" * 60)
    
    # Реальные GPS координаты из Wialon API для правильных грузовиков
    real_gps_data = {
        "484ATL01": {
            "latitude": 41.186362,
            "longitude": 69.205233,
            "speed": 0.0,
            "heading": 94.0,
            "satellites": 19,
            "signal_quality": "good",
            "timestamp": 1759156947,  # Unix timestamp
            "engine_status": False,
            "ignition_status": False
        },
        "355ATL01": {
            "latitude": 44.148712,
            "longitude": 80.000000,
            "speed": 0.0,
            "heading": 310.0,
            "satellites": 11,
            "signal_quality": "good",
            "timestamp": 1759156921,
            "engine_status": False,
            "ignition_status": False
        },
        "359AUL01": {
            "latitude": 44.148209,
            "longitude": 79.999886,
            "speed": 0.0,
            "heading": 142.0,
            "satellites": 18,
            "signal_quality": "good",
            "timestamp": 1759156918,
            "engine_status": False,
            "ignition_status": False
        },
        "695BHS02": {
            "latitude": 44.184773,
            "longitude": 80.406952,
            "speed": 0.0,
            "heading": 177.0,
            "satellites": 12,
            "signal_quality": "good",
            "timestamp": 1759124234,
            "engine_status": False,
            "ignition_status": False
        }
    }
    
    updated_count = 0
    
    for vehicle_number, gps_data in real_gps_data.items():
        try:
            # Ищем грузовик по номеру (убираем пробелы для поиска)
            search_number = vehicle_number.replace(" ", "")
            vehicle = Vehicle.objects.filter(number__icontains=search_number).first()
            
            if not vehicle:
                print(f"❌ Грузовик {vehicle_number} не найден в базе данных")
                continue
            
            # Конвертируем Unix timestamp в Django datetime
            from datetime import timezone as dt_timezone
            timestamp_dt = datetime.fromtimestamp(gps_data['timestamp'], tz=dt_timezone.utc)
            
            # Сохраняем старые координаты для сравнения
            old_lat = vehicle.gps_latitude
            old_lon = vehicle.gps_longitude
            
            # Обновляем GPS данные
            vehicle.gps_enabled = True
            vehicle.gps_latitude = gps_data['latitude']
            vehicle.gps_longitude = gps_data['longitude']
            vehicle.gps_speed = gps_data['speed']
            vehicle.gps_heading = gps_data['heading']
            vehicle.gps_satellites = gps_data['satellites']
            vehicle.gps_signal_quality = gps_data['signal_quality']
            vehicle.gps_last_update = timestamp_dt
            vehicle.gps_engine_status = gps_data['engine_status']
            vehicle.gps_ignition_status = gps_data['ignition_status']
            
            vehicle.save()
            updated_count += 1
            
            print(f"\n🚛 Обновлен {vehicle.number}:")
            print(f"   📍 Старые координаты: {old_lat}, {old_lon}")
            print(f"   📍 Новые координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
            print(f"   🛰️ Спутники: {vehicle.gps_satellites}")
            print(f"   ⏰ Обновлено: {vehicle.gps_last_update}")
            
        except Exception as e:
            print(f"❌ Ошибка при обновлении грузовика {vehicle_number}: {e}")
    
    print(f"\n📊 ИТОГИ:")
    print(f"   ✅ Обновлено грузовиков: {updated_count}")
    print(f"   📱 Всего GPS устройств: {len(real_gps_data)}")
    
    # Проверяем обновленные данные
    print(f"\n🔍 ПРОВЕРКА ОБНОВЛЕННЫХ ДАННЫХ:")
    vehicles_with_gps = Vehicle.objects.filter(
        gps_enabled=True,
        gps_latitude__isnull=False,
        gps_longitude__isnull=False
    )
    
    for vehicle in vehicles_with_gps:
        print(f"🚛 {vehicle.number}: {vehicle.gps_latitude}, {vehicle.gps_longitude}")

if __name__ == "__main__":
    update_production_gps_data()
    print("\n✅ GPS данные на продакшн сервере обновлены!")
