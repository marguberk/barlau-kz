#!/usr/bin/env python3
"""
Скрипт для исправления местоположения 695BHS02 ближе к Китаю
"""
import os
import django
from datetime import datetime
from django.utils import timezone

# Настройка Django для продакшн
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle

def fix_695BHS02_china_location():
    """Исправляем местоположение 695BHS02 ближе к китайской границе"""
    print("🔧 Исправление местоположения 695BHS02 ближе к Китаю")
    print("=" * 60)
    
    try:
        # Ищем грузовик 695BHS02
        vehicle = Vehicle.objects.filter(number="695BHS02").first()
        if not vehicle:
            print("❌ Грузовик 695BHS02 не найден")
            return
        
        # Сохраняем старые координаты
        old_lat = vehicle.gps_latitude
        old_lon = vehicle.gps_longitude
        
        # Координаты ближе к китайской границе (район Хоргоса)
        # Хоргос - это пограничный пункт между Казахстаном и Китаем
        vehicle.gps_latitude = 44.217500  # Севернее Хоргоса
        vehicle.gps_longitude = 80.405000  # Ближе к китайской границе
        vehicle.gps_speed = 0.0
        vehicle.gps_heading = 180.0  # Направление на юг (к Китаю)
        vehicle.gps_satellites = 12
        vehicle.gps_signal_quality = "good"
        vehicle.gps_last_update = timezone.now()
        vehicle.gps_engine_status = False
        vehicle.gps_ignition_status = False
        
        vehicle.save()
        
        print(f"✅ 695BHS02 исправлен:")
        print(f"   📍 Старые координаты: {old_lat}, {old_lon} (Алматы)")
        print(f"   📍 Новые координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
        print(f"   🇨🇳 Местоположение: Ближе к китайской границе (район Хоргоса)")
        print(f"   📏 Расстояние до Китая: ~50 км")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    fix_695BHS02_china_location()


