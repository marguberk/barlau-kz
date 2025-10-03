#!/usr/bin/env python3
"""
Скрипт для автоматической синхронизации GPS данных из Wialon API каждые 5-10 секунд
"""
import os
import django
import time
import requests
import json
from datetime import datetime
from django.utils import timezone

# Настройка Django для продакшн
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle
from logistics.services.wialon_service import WialonService

def sync_gps_from_wialon():
    """Синхронизация GPS данных из Wialon API"""
    print(f"\n🛰️ Синхронизация GPS данных из Wialon - {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        # Используем существующий Wialon сервис
        wialon_service = WialonService()
        
        # Получаем все грузовики с GPS трекерами
        gps_vehicles = Vehicle.objects.filter(gps_enabled=True)
        
        if not gps_vehicles.exists():
            print("❌ Нет грузовиков с включенным GPS")
            return False
        
        print(f"📡 Найдено {gps_vehicles.count()} грузовиков с GPS")
        
        updated_count = 0
        
        for vehicle in gps_vehicles:
            try:
                print(f"🔄 Обновляем GPS данные для {vehicle.number}...")
                
                # Используем существующий метод для обновления GPS данных
                success = wialon_service.update_vehicle_gps_data(vehicle)
                
                if success:
                    # Получаем обновленные данные
                    vehicle.refresh_from_db()
                    print(f"✅ {vehicle.number}: {vehicle.gps_latitude}, {vehicle.gps_longitude} (скорость: {vehicle.gps_speed} км/ч)")
                    updated_count += 1
                else:
                    print(f"⚠️ Не удалось обновить GPS данные для {vehicle.number}")
                
                # Небольшая пауза между запросами
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Ошибка обновления {vehicle.number}: {e}")
        
        print(f"📊 Результат: обновлено {updated_count} из {gps_vehicles.count()} грузовиков")
        return updated_count > 0
        
    except Exception as e:
        print(f"❌ Общая ошибка синхронизации: {e}")
        return False

def run_continuous_sync():
    """Запуск непрерывной синхронизации GPS данных"""
    print("🛰️ Запуск непрерывной синхронизации GPS данных из Wialon")
    print("=" * 70)
    
    update_count = 0
    
    while True:
        try:
            success = sync_gps_from_wialon()
            
            if success:
                update_count += 1
                print(f"🔄 Синхронизация #{update_count} завершена успешно")
            else:
                print("⚠️ Синхронизация не удалась, повторяем через 30 секунд")
                time.sleep(30)
                continue
            
            # Ждем 5-10 секунд до следующей синхронизации
            sleep_time = 5 + (update_count % 5)  # 5-10 секунд
            print(f"⏰ Следующая синхронизация через {sleep_time} секунд...")
            time.sleep(sleep_time)
            
        except KeyboardInterrupt:
            print(f"\n🛑 Остановлено пользователем после {update_count} синхронизаций")
            break
        except Exception as e:
            print(f"❌ Общая ошибка: {e}")
            time.sleep(30)  # Ждем 30 секунд перед повтором

if __name__ == "__main__":
    run_continuous_sync()

