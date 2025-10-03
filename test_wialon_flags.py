#!/usr/bin/env python3
"""
Тестирование разных флагов Wialon API для получения максимальных данных
"""
import os
import django
import json
from datetime import datetime
from django.utils import timezone

# Настройка Django для продакшн
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle
from logistics.services.wialon_service import WialonService

def test_wialon_flags():
    """Тестируем разные флаги для получения данных"""
    print("🧪 ТЕСТИРОВАНИЕ ФЛАГОВ WIALON API")
    print("=" * 60)
    
    try:
        wialon_service = WialonService()
        
        if not wialon_service.authenticate():
            print("❌ Ошибка авторизации в Wialon")
            return
        print("✅ Авторизация успешна")
        
        # Тестируем на 484 ATL 01 (который работает)
        test_unit_id = 29603155
        test_unit_name = "484 ATL 01"
        
        print(f"\n🔬 Тестируем флаги для {test_unit_name} (ID: {test_unit_id})")
        
        # Разные комбинации флагов
        flag_combinations = [
            (0x1, "Базовая информация"),
            (0x10, "Позиция"),
            (0x100, "Параметры"),
            (0x1000, "Сообщения"),
            (0x1111, "Все основные флаги"),
            (0x1FFF, "Все возможные флаги"),
            (0xFFFF, "Максимальные флаги"),
        ]
        
        for flag, description in flag_combinations:
            print(f"\n🚩 Тестируем флаг {flag} (0x{flag:x}) - {description}")
            
            try:
                position_url = f"{wialon_service.base_url}/wialon/ajax.html"
                params = {
                    'svc': 'core/search_item',
                    'params': json.dumps({
                        'id': test_unit_id,
                        'flags': flag
                    }),
                    'sid': wialon_service.sid
                }
                
                response = wialon_service.session.get(position_url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if isinstance(data, dict) and 'item' in data:
                    item = data['item']
                    print(f"   ✅ Успешно получены данные")
                    
                    # Анализируем структуру данных
                    print(f"   📊 Структура данных:")
                    for key in item.keys():
                        value = item[key]
                        if isinstance(value, dict):
                            print(f"      - {key}: dict с {len(value)} полями")
                            if key == 'pos' and value:
                                print(f"        📍 Позиция: lat={value.get('y', 'N/A')}, lon={value.get('x', 'N/A')}")
                                print(f"        🚗 Скорость: {value.get('s', 'N/A')} мм/ч")
                                print(f"        🧭 Направление: {value.get('c', 'N/A')}°")
                                print(f"        📡 Спутники: {value.get('sc', 'N/A')}")
                                print(f"        ⏰ Время: {value.get('t', 'N/A')}")
                        elif isinstance(value, list):
                            print(f"      - {key}: list с {len(value)} элементами")
                        else:
                            print(f"      - {key}: {type(value).__name__} = {value}")
                
                elif isinstance(data, list) and len(data) > 0:
                    if 'error' in data[0]:
                        print(f"   ❌ Ошибка: {data[0]['error']} - {data[0].get('reason', 'N/A')}")
                    else:
                        print(f"   ✅ Получен список с {len(data)} элементами")
                else:
                    print(f"   ⚠️ Неожиданный формат данных: {type(data)}")
                    
            except Exception as e:
                print(f"   ❌ Ошибка запроса: {e}")
        
        # Теперь попробуем получить данные для всех устройств с лучшим флагом
        print(f"\n🔄 ПРИМЕНЯЕМ ЛУЧШИЙ ФЛАГ КО ВСЕМ УСТРОЙСТВАМ")
        
        target_units = [
            {"name": "484 ATL 01", "id": 29603155},
            {"name": "355 ATL 01", "id": 29682916}, 
            {"name": "359 AUL 01", "id": 29682864},
            {"name": "695 BHS 02", "id": 29682886}
        ]
        
        best_flag = 0x1111  # Все основные флаги
        
        for target_unit in target_units:
            print(f"\n📱 {target_unit['name']} (ID: {target_unit['id']}):")
            
            try:
                position_url = f"{wialon_service.base_url}/wialon/ajax.html"
                params = {
                    'svc': 'core/search_item',
                    'params': json.dumps({
                        'id': target_unit['id'],
                        'flags': best_flag
                    }),
                    'sid': wialon_service.sid
                }
                
                response = wialon_service.session.get(position_url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if isinstance(data, dict) and 'item' in data:
                    item = data['item']
                    
                    if 'pos' in item and item['pos']:
                        pos = item['pos']
                        print(f"   ✅ GPS данные найдены:")
                        print(f"      📍 Координаты: {pos.get('y', 'N/A')}, {pos.get('x', 'N/A')}")
                        print(f"      🚗 Скорость: {pos.get('s', 'N/A')} мм/ч")
                        print(f"      🧭 Направление: {pos.get('c', 'N/A')}°")
                        print(f"      📡 Спутники: {pos.get('sc', 'N/A')}")
                        print(f"      ⏰ Время: {pos.get('t', 'N/A')}")
                        
                        # Обновляем данные в базе
                        try:
                            vehicle = Vehicle.objects.filter(number=target_unit['name'].replace(' ', '')).first()
                            if vehicle:
                                vehicle.gps_latitude = pos.get('y', 0)
                                vehicle.gps_longitude = pos.get('x', 0)
                                vehicle.gps_speed = pos.get('s', 0) * 3.6 / 1000  # мм/ч в км/ч
                                vehicle.gps_heading = pos.get('c', 0)
                                vehicle.gps_satellites = pos.get('sc', 0)
                                vehicle.gps_last_update = timezone.now()
                                vehicle.save()
                                print(f"   💾 Данные сохранены в базу")
                        except Exception as e:
                            print(f"   ❌ Ошибка сохранения: {e}")
                    else:
                        print(f"   ⚠️ Нет GPS данных в позиции")
                else:
                    print(f"   ❌ Не удалось получить данные")
                    
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")

if __name__ == "__main__":
    test_wialon_flags()


