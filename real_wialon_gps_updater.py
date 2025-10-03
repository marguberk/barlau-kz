#!/usr/bin/env python3
"""
Скрипт для автоматического получения GPS данных из Wialon API каждые 5-10 секунд
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

class WialonGPSUpdater:
    def __init__(self):
        self.wialon_token = "a4e2f8e4c9c7f8e4c9c7f8e4c9c7f8e4"  # Ваш токен Wialon
        self.base_url = "https://hst-api.wialon.com/wialon/ajax.html"
        
    def get_wialon_data(self):
        """Получаем GPS данные из Wialon API"""
        try:
            # Параметры для запроса к Wialon API
            params = {
                'svc': 'core/search_items',
                'params': json.dumps({
                    "spec": {
                        "itemsType": "avl_unit",
                        "propName": "sys_name",
                        "propValueMask": "*",
                        "sortType": "sys_name"
                    },
                    "force": 1,
                    "flags": 1,
                    "from": 0,
                    "to": 0
                }),
                'sid': self.wialon_token
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'items' in data:
                    return data['items']
            
            return []
            
        except Exception as e:
            print(f"❌ Ошибка получения данных из Wialon: {e}")
            return []
    
    def get_vehicle_positions(self, item_ids):
        """Получаем позиции транспортных средств"""
        try:
            if not item_ids:
                return []
                
            params = {
                'svc': 'core/search_items',
                'params': json.dumps({
                    "spec": {
                        "itemsType": "avl_unit",
                        "items": item_ids,
                        "propName": "sys_name",
                        "propValueMask": "*",
                        "sortType": "sys_name"
                    },
                    "force": 1,
                    "flags": 8193,  # Флаги для получения позиций
                    "from": 0,
                    "to": 0
                }),
                'sid': self.wialon_token
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('items', [])
            
            return []
            
        except Exception as e:
            print(f"❌ Ошибка получения позиций: {e}")
            return []
    
    def update_vehicles_from_wialon(self):
        """Обновляем GPS данные транспортных средств из Wialon"""
        print(f"\n🛰️ Получение GPS данных из Wialon - {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            # Получаем список всех транспортных средств из Wialon
            wialon_vehicles = self.get_wialon_data()
            
            if not wialon_vehicles:
                print("❌ Не удалось получить данные из Wialon")
                return False
            
            print(f"📡 Получено {len(wialon_vehicles)} транспортных средств из Wialon")
            
            # Маппинг номеров Wialon на номера в нашей базе
            wialon_to_django_map = {
                "484 ATL 01": "484ATL01",
                "355 ATL 01": "355ATL01", 
                "359 AUL 01": "359AUL01",
                "695 BHS 02": "695BHS02"
            }
            
            updated_count = 0
            
            for wialon_vehicle in wialon_vehicles:
                wialon_name = wialon_vehicle.get('nm', '')
                django_number = wialon_to_django_map.get(wialon_name)
                
                if not django_number:
                    continue
                
                # Получаем позицию транспортного средства
                positions = self.get_vehicle_positions([wialon_vehicle['id']])
                
                if positions and len(positions) > 0:
                    position = positions[0]
                    
                    # Извлекаем GPS данные
                    pos = position.get('pos', {})
                    if pos:
                        latitude = pos.get('y', 0)
                        longitude = pos.get('x', 0)
                        speed = pos.get('s', 0) / 1000  # Конвертируем из мм/ч в км/ч
                        course = pos.get('c', 0)
                        
                        # Находим транспортное средство в нашей базе
                        vehicle = Vehicle.objects.filter(number=django_number).first()
                        if vehicle:
                            # Обновляем GPS данные
                            vehicle.gps_latitude = latitude
                            vehicle.gps_longitude = longitude
                            vehicle.gps_speed = speed
                            vehicle.gps_heading = course
                            vehicle.gps_satellites = 12  # Примерное значение
                            vehicle.gps_signal_quality = "good"
                            vehicle.gps_last_update = timezone.now()
                            vehicle.gps_engine_status = speed > 0
                            vehicle.gps_ignition_status = speed > 0
                            
                            vehicle.save()
                            
                            print(f"✅ {django_number}: {latitude:.6f}, {longitude:.6f} (скорость: {speed:.1f} км/ч)")
                            updated_count += 1
            
            print(f"📊 Обновлено {updated_count} транспортных средств")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка обновления из Wialon: {e}")
            return False
    
    def run_continuous_update(self):
        """Запускаем непрерывное обновление GPS данных"""
        print("🛰️ Запуск непрерывного обновления GPS данных из Wialon")
        print("=" * 70)
        
        update_count = 0
        
        while True:
            try:
                success = self.update_vehicles_from_wialon()
                
                if success:
                    update_count += 1
                    print(f"🔄 Обновление #{update_count} завершено успешно")
                else:
                    print("⚠️ Обновление не удалось, повторяем через 30 секунд")
                    time.sleep(30)
                    continue
                
                # Ждем 5-10 секунд до следующего обновления
                sleep_time = 5 + (update_count % 5)  # 5-10 секунд
                print(f"⏰ Следующее обновление через {sleep_time} секунд...")
                time.sleep(sleep_time)
                
            except KeyboardInterrupt:
                print(f"\n🛑 Остановлено пользователем после {update_count} обновлений")
                break
            except Exception as e:
                print(f"❌ Общая ошибка: {e}")
                time.sleep(30)  # Ждем 30 секунд перед повтором

def main():
    updater = WialonGPSUpdater()
    updater.run_continuous_update()

if __name__ == "__main__":
    main()


