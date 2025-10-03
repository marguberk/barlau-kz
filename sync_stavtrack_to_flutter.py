#!/usr/bin/env python3
"""
Синхронизация GPS данных из StavTrack API с грузовиками во Flutter приложении
"""
import os
import django
import time
import requests
import json
import logging
from datetime import datetime, timedelta
from django.utils import timezone

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle
from logistics.services.wialon_service import WialonService

logger = logging.getLogger(__name__)

def sync_stavtrack_to_flutter():
    """
    Синхронизируем GPS данные из StavTrack с грузовиками во Flutter
    """
    print("🔄 СИНХРОНИЗАЦИЯ STAVTRACK → FLUTTER")
    print("=" * 60)
    
    wialon_service = WialonService()
    if not wialon_service.authenticate():
        print("❌ Не удалось авторизоваться в StavTrack API")
        return
    
    print("✅ Авторизация в StavTrack API успешна")
    
    # Получаем все устройства из StavTrack
    stavtrack_units = wialon_service.get_units_list()
    if not stavtrack_units:
        print("❌ Не удалось получить список устройств из StavTrack")
        return
    
    print(f"📡 Найдено {len(stavtrack_units)} устройств в StavTrack:")
    for unit in stavtrack_units:
        print(f"   - {unit.get('nm')} (ID: {unit.get('id')})")
    
    # Получаем все грузовики из нашей базы (те что показывает Flutter)
    all_vehicles = Vehicle.objects.all().order_by('number')
    print(f"\n🚛 Найдено {all_vehicles.count()} грузовиков в нашей базе:")
    for vehicle in all_vehicles:
        print(f"   - {vehicle.number} (ID: {vehicle.id})")
    
    # Синхронизируем GPS данные
    updated_count = 0
    for stavtrack_unit in stavtrack_units:
        stavtrack_name = stavtrack_unit.get('nm')  # Например: "355 ATL 01"
        stavtrack_id = stavtrack_unit.get('id')
        
        print(f"\n🔍 Ищем грузовик {stavtrack_name} в нашей базе...")
        
        # Ищем грузовик в нашей базе по номеру (убираем пробелы для сравнения)
        stavtrack_number_clean = stavtrack_name.replace(' ', '')  # "355ATL01"
        
        matching_vehicle = None
        for vehicle in all_vehicles:
            vehicle_number_clean = vehicle.number.replace(' ', '')  # "355ATL01"
            if vehicle_number_clean == stavtrack_number_clean:
                matching_vehicle = vehicle
                break
        
        if matching_vehicle:
            print(f"✅ Найден грузовик: {matching_vehicle.number}")
            
            # Получаем GPS данные из StavTrack
            position = wialon_service.get_unit_position(stavtrack_id)
            if position:
                print(f"   📍 GPS данные из StavTrack: {position['latitude']}, {position['longitude']}")
                
                # Обновляем GPS данные в нашей базе
                matching_vehicle.gps_latitude = str(position['latitude'])
                matching_vehicle.gps_longitude = str(position['longitude'])
                matching_vehicle.gps_speed = str(position.get('speed', 0))
                matching_vehicle.gps_heading = str(position.get('heading', 0))
                matching_vehicle.gps_satellites = position.get('satellites', 0)
                matching_vehicle.gps_signal_quality = position.get('signal_quality', 'unknown')
                matching_vehicle.gps_last_update = timezone.now()
                matching_vehicle.gps_enabled = True
                matching_vehicle.gps_device_id = str(stavtrack_id)
                matching_vehicle.gps_engine_status = position.get('engine_status', False)
                matching_vehicle.gps_ignition_status = position.get('ignition_status', False)
                
                matching_vehicle.save()
                updated_count += 1
                print(f"   ✅ Обновлены GPS данные для {matching_vehicle.number}")
            else:
                print(f"   ⚠️ Не удалось получить GPS данные для {stavtrack_name}")
        else:
            print(f"   ❌ Грузовик {stavtrack_name} не найден в нашей базе")
    
    print(f"\n📊 ИТОГИ СИНХРОНИЗАЦИИ:")
    print(f"   ✅ Обновлено грузовиков: {updated_count}")
    print(f"   📡 Устройств в StavTrack: {len(stavtrack_units)}")
    print(f"   🚛 Грузовиков в нашей базе: {all_vehicles.count()}")
    
    # Показываем обновленные GPS данные
    print(f"\n🛰️ ОБНОВЛЕННЫЕ GPS ДАННЫЕ:")
    gps_vehicles = Vehicle.objects.filter(
        gps_enabled=True,
        gps_latitude__isnull=False,
        gps_longitude__isnull=False
    ).order_by('number')
    
    for vehicle in gps_vehicles:
        print(f"   {vehicle.number}: {vehicle.gps_latitude}, {vehicle.gps_longitude} (обновлено: {vehicle.gps_last_update.strftime('%H:%M:%S')})")

if __name__ == "__main__":
    sync_stavtrack_to_flutter()
    print("\n✅ Синхронизация StavTrack → Flutter завершена!")


