#!/usr/bin/env python3
"""
Автоматическая синхронизация GPS данных из StavTrack API с продакшн базой
Обновляет данные каждые 5-10 секунд
"""
import os
import django
import time
import requests
import json
import logging
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Настройка Django для продакшн
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle
from logistics.services.wialon_service import WialonService

logger = logging.getLogger(__name__)

def auto_sync_stavtrack():
    """
    Автоматическая синхронизация GPS данных из StavTrack
    """
    print("🚀 ЗАПУСК АВТОМАТИЧЕСКОЙ СИНХРОНИЗАЦИИ STAVTRACK")
    print("=" * 60)
    
    wialon_service = WialonService()
    
    sync_count = 0
    
    while True:
        try:
            sync_count += 1
            print(f"\n🔄 СИНХРОНИЗАЦИЯ #{sync_count} - {datetime.now().strftime('%H:%M:%S')}")
            print("-" * 40)
            
            # Авторизация в StavTrack API
            if not wialon_service._authenticated:
                print("🔐 Авторизация в StavTrack API...")
                if not wialon_service.authenticate():
                    print("❌ Ошибка авторизации в StavTrack API. Повтор через 60 сек.")
                    time.sleep(60)
                    continue
            
            # Получаем устройства из StavTrack
            stavtrack_units = wialon_service.get_units_list()
            if not stavtrack_units:
                print("❌ Не удалось получить список устройств из StavTrack")
                time.sleep(30)
                continue
            
            # Синхронизируем GPS данные для каждого устройства
            updated_count = 0
            for stavtrack_unit in stavtrack_units:
                stavtrack_name = stavtrack_unit.get('nm')
                stavtrack_id = stavtrack_unit.get('id')
                
                # Ищем грузовик в нашей базе
                stavtrack_number_clean = stavtrack_name.replace(' ', '')
                matching_vehicle = None
                
                for vehicle in Vehicle.objects.all():
                    vehicle_number_clean = vehicle.number.replace(' ', '')
                    if vehicle_number_clean == stavtrack_number_clean:
                        matching_vehicle = vehicle
                        break
                
                if matching_vehicle:
                    # Получаем GPS данные из StavTrack
                    position = wialon_service.get_unit_position(stavtrack_id)
                    if position:
                        # Обновляем GPS данные
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
                        print(f"✅ {matching_vehicle.number}: {position['latitude']:.6f}, {position['longitude']:.6f}")
            
            print(f"📊 Обновлено {updated_count} грузовиков из {len(stavtrack_units)} устройств")
            
        except Exception as e:
            print(f"❌ Ошибка в цикле синхронизации: {e}")
            time.sleep(30)
            continue
        
        # Ждем 5-10 секунд перед следующей синхронизацией
        wait_time = random.randint(5, 10)
        print(f"⏳ Следующая синхронизация через {wait_time} секунд...")
        time.sleep(wait_time)

if __name__ == "__main__":
    auto_sync_stavtrack()


