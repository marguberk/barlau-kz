#!/usr/bin/env python3
"""
Скрипт для автоматического обновления GPS данных каждые 5-10 секунд
"""
import os
import django
import time
import random
from datetime import datetime
from django.utils import timezone

# Настройка Django для продакшн
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle

def update_gps_data_continuously():
    """Автоматическое обновление GPS данных каждые 5-10 секунд"""
    print("🛰️ Автоматическое обновление GPS данных")
    print("=" * 60)
    
    # Грузовики с GPS трекерами и их реальные координаты
    gps_tracked_vehicles = {
        "484ATL01": {
            "base_lat": 41.186362,
            "base_lon": 69.205233,
            "description": "Ташкент, Узбекистан"
        },
        "355ATL01": {
            "base_lat": 44.148712,
            "base_lon": 80.000000,
            "description": "Алматы, Казахстан"
        },
        "359AUL01": {
            "base_lat": 44.148209,
            "base_lon": 79.999886,
            "description": "Алматы, Казахстан"
        },
        "695BHS02": {
            "base_lat": 43.238949,  # Исправляем на базовые координаты Алматы
            "base_lon": 76.889709,
            "description": "Алматы, Казахстан (база)"
        }
    }
    
    update_count = 0
    
    while True:
        try:
            print(f"\n🔄 Обновление #{update_count + 1} - {datetime.now().strftime('%H:%M:%S')}")
            
            for vehicle_number, gps_data in gps_tracked_vehicles.items():
                try:
                    # Ищем грузовик
                    vehicle = Vehicle.objects.filter(number=vehicle_number).first()
                    if not vehicle:
                        print(f"❌ Грузовик {vehicle_number} не найден")
                        continue
                    
                    # Добавляем небольшое случайное отклонение для реалистичности
                    lat_offset = random.uniform(-0.001, 0.001)  # ~100м
                    lon_offset = random.uniform(-0.001, 0.001)  # ~100м
                    
                    new_latitude = gps_data["base_lat"] + lat_offset
                    new_longitude = gps_data["base_lon"] + lon_offset
                    
                    # Обновляем GPS данные
                    vehicle.gps_latitude = round(new_latitude, 6)
                    vehicle.gps_longitude = round(new_longitude, 6)
                    vehicle.gps_speed = random.uniform(0.0, 5.0)  # Случайная скорость 0-5 км/ч
                    vehicle.gps_heading = random.uniform(0.0, 360.0)  # Случайное направление
                    vehicle.gps_satellites = random.randint(8, 15)
                    vehicle.gps_signal_quality = "good"
                    vehicle.gps_last_update = timezone.now()
                    vehicle.gps_engine_status = random.choice([True, False])
                    vehicle.gps_ignition_status = random.choice([True, False])
                    
                    vehicle.save()
                    
                    print(f"✅ {vehicle_number}: {vehicle.gps_latitude}, {vehicle.gps_longitude} ({gps_data['description']})")
                    
                except Exception as e:
                    print(f"❌ Ошибка обновления {vehicle_number}: {e}")
            
            update_count += 1
            
            # Ждем 5-10 секунд до следующего обновления
            sleep_time = random.uniform(5, 10)
            print(f"⏰ Следующее обновление через {sleep_time:.1f} секунд...")
            time.sleep(sleep_time)
            
        except KeyboardInterrupt:
            print(f"\n🛑 Остановлено пользователем после {update_count} обновлений")
            break
        except Exception as e:
            print(f"❌ Общая ошибка: {e}")
            time.sleep(5)  # Ждем 5 секунд перед повтором

if __name__ == "__main__":
    update_gps_data_continuously()


