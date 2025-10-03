#!/usr/bin/env python3
"""
Скрипт для настройки GPS устройств и получения данных из Wialon
"""
import os
import django
from datetime import datetime
from django.utils import timezone

# Настройка Django для продакшн
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle
from logistics.services.wialon_service import WialonService

def setup_gps_devices():
    """Настройка GPS устройств для грузовиков"""
    print("🔧 Настройка GPS устройств")
    print("=" * 50)
    
    try:
        # Инициализируем Wialon сервис
        wialon_service = WialonService()
        
        # Получаем список устройств из Wialon
        units = wialon_service.get_units_list()
        if not units:
            print("❌ Не удалось получить список устройств из Wialon")
            return
        
        print(f"📡 Найдено {len(units)} устройств в Wialon:")
        for unit in units:
            print(f"  - {unit['nm']} (ID: {unit['id']})")
        
        # Маппинг грузовиков на GPS устройства
        vehicle_mapping = {
            "484ATL01": "484 ATL 01",
            "355ATL01": "355 ATL 01", 
            "359AUL01": "359 AUL 01",
            "695BHS02": "695 BHS 02"
        }
        
        print(f"\n🔗 Настройка маппинга грузовиков:")
        
        for vehicle_number, wialon_name in vehicle_mapping.items():
            try:
                # Находим грузовик в базе
                vehicle = Vehicle.objects.filter(number=vehicle_number).first()
                if not vehicle:
                    print(f"❌ Грузовик {vehicle_number} не найден в базе")
                    continue
                
                # Находим GPS устройство в Wialon
                gps_unit = None
                for unit in units:
                    if unit['nm'] == wialon_name:
                        gps_unit = unit
                        break
                
                if not gps_unit:
                    print(f"❌ GPS устройство {wialon_name} не найдено в Wialon")
                    continue
                
                # Настраиваем грузовик
                vehicle.gps_enabled = True
                vehicle.gps_device_id = str(gps_unit['id'])
                vehicle.save()
                
                print(f"✅ {vehicle_number} → {wialon_name} (ID: {gps_unit['id']})")
                
            except Exception as e:
                print(f"❌ Ошибка настройки {vehicle_number}: {e}")
        
        print(f"\n🛰️ Получение GPS данных:")
        
        # Получаем GPS данные для настроенных грузовиков
        for vehicle_number in vehicle_mapping.keys():
            try:
                vehicle = Vehicle.objects.filter(number=vehicle_number).first()
                if not vehicle or not vehicle.gps_enabled:
                    continue
                
                print(f"🔄 Обновляем GPS данные для {vehicle.number}...")
                success = wialon_service.update_vehicle_gps_data(vehicle)
                
                if success:
                    vehicle.refresh_from_db()
                    print(f"✅ {vehicle.number}: {vehicle.gps_latitude}, {vehicle.gps_longitude} (скорость: {vehicle.gps_speed} км/ч)")
                else:
                    print(f"⚠️ Не удалось получить GPS данные для {vehicle.number}")
                
            except Exception as e:
                print(f"❌ Ошибка получения GPS данных для {vehicle_number}: {e}")
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")

if __name__ == "__main__":
    setup_gps_devices()


