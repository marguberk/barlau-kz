#!/usr/bin/env python3
"""
Скрипт для установки базового местоположения для всех грузовиков без GPS трекеров
"""
import os
import django
from datetime import datetime
from django.utils import timezone
import random

# Настройка Django для продакшн
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle

def update_all_vehicles_base_location():
    """Устанавливаем базовое местоположение для всех грузовиков без GPS трекеров"""
    print("🏢 Установка базового местоположения для всех грузовиков")
    print("=" * 70)
    
    # Координаты базы в Алматы (там же где 290 ATL 01)
    base_latitude = 44.148712
    base_longitude = 80.000000
    
    # Грузовики с GPS трекерами (не трогаем их)
    gps_tracked_vehicles = ["484 ATL 01", "290 ATL 01", "533 ATL 01", "290 ATL 02"]
    
    # Получаем все грузовики
    all_vehicles = Vehicle.objects.all()
    
    updated_count = 0
    skipped_count = 0
    
    for vehicle in all_vehicles:
        try:
            # НИКОГДА не трогаем грузовики с GPS трекерами
            if vehicle.number in gps_tracked_vehicles or vehicle.gps_device_id:
                print(f"🔒 ЗАЩИЩЕН {vehicle.number} - имеет GPS трекер (НЕ ТРОГАЕМ!)")
                skipped_count += 1
                continue
            
            # Генерируем случайные координаты в радиусе ~500 метров от базы
            # Небольшое отклонение для реалистичности
            lat_offset = random.uniform(-0.005, 0.005)  # ~500м
            lon_offset = random.uniform(-0.005, 0.005)  # ~500м
            
            vehicle_latitude = base_latitude + lat_offset
            vehicle_longitude = base_longitude + lon_offset
            
            # Сохраняем старые координаты для сравнения
            old_lat = vehicle.gps_latitude
            old_lon = vehicle.gps_longitude
            
            # Устанавливаем базовые GPS данные
            vehicle.gps_enabled = True
            vehicle.gps_latitude = round(vehicle_latitude, 6)
            vehicle.gps_longitude = round(vehicle_longitude, 6)
            vehicle.gps_speed = 0.0
            vehicle.gps_heading = 0.0
            vehicle.gps_satellites = random.randint(8, 12)
            vehicle.gps_signal_quality = "good"
            vehicle.gps_last_update = timezone.now()
            vehicle.gps_engine_status = False
            vehicle.gps_ignition_status = False
            
            vehicle.save()
            updated_count += 1
            
            print(f"\n🚛 Обновлен {vehicle.number}:")
            print(f"   📍 Старые координаты: {old_lat}, {old_lon}")
            print(f"   📍 Новые координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
            print(f"   🏢 База: Алматы")
            
        except Exception as e:
            print(f"❌ Ошибка при обновлении грузовика {vehicle.number}: {e}")
    
    print(f"\n📊 ИТОГИ:")
    print(f"   ✅ Обновлено грузовиков: {updated_count}")
    print(f"   ⏭️ Пропущено (с GPS трекерами): {skipped_count}")
    print(f"   📱 Всего грузовиков: {all_vehicles.count()}")
    
    # Проверяем обновленные данные
    print(f"\n🔍 ПРОВЕРКА ОБНОВЛЕННЫХ ДАННЫХ:")
    vehicles_with_gps = Vehicle.objects.filter(
        gps_enabled=True,
        gps_latitude__isnull=False,
        gps_longitude__isnull=False
    ).order_by('number')
    
    print(f"📍 Всего грузовиков с GPS: {vehicles_with_gps.count()}")
    for vehicle in vehicles_with_gps[:10]:  # Показываем первые 10
        print(f"🚛 {vehicle.number}: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
    
    if vehicles_with_gps.count() > 10:
        print(f"... и еще {vehicles_with_gps.count() - 10} грузовиков")

if __name__ == "__main__":
    update_all_vehicles_base_location()
    print("\n✅ Базовое местоположение для всех грузовиков установлено!")
