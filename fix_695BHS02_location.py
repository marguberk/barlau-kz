#!/usr/bin/env python3
"""
Скрипт для исправления местоположения 695BHS02
"""
import os
import django
from datetime import datetime
from django.utils import timezone

# Настройка Django для продакшн
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle

def fix_695BHS02_location():
    """Исправляем местоположение 695BHS02 на правильные координаты"""
    print("🔧 Исправление местоположения 695BHS02")
    print("=" * 50)
    
    try:
        # Ищем грузовик 695BHS02
        vehicle = Vehicle.objects.filter(number="695BHS02").first()
        if not vehicle:
            print("❌ Грузовик 695BHS02 не найден")
            return
        
        # Сохраняем старые координаты
        old_lat = vehicle.gps_latitude
        old_lon = vehicle.gps_longitude
        
        # Устанавливаем правильные координаты (база в Алматы)
        vehicle.gps_latitude = 43.238949
        vehicle.gps_longitude = 76.889709
        vehicle.gps_speed = 0.0
        vehicle.gps_heading = 0.0
        vehicle.gps_satellites = 12
        vehicle.gps_signal_quality = "good"
        vehicle.gps_last_update = timezone.now()
        vehicle.gps_engine_status = False
        vehicle.gps_ignition_status = False
        
        vehicle.save()
        
        print(f"✅ 695BHS02 исправлен:")
        print(f"   📍 Старые координаты: {old_lat}, {old_lon}")
        print(f"   📍 Новые координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
        print(f"   🏢 Местоположение: База Алматы")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    fix_695BHS02_location()


