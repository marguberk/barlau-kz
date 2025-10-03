#!/usr/bin/env python3
"""
Детальная проверка всех данных из Wialon API
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

def detailed_wialon_analysis():
    """Детальный анализ всех данных из Wialon API"""
    print("🔍 ДЕТАЛЬНЫЙ АНАЛИЗ WIALON API")
    print("=" * 60)
    
    try:
        wialon_service = WialonService()
        
        # 1. Проверяем авторизацию
        print("1️⃣ ПРОВЕРКА АВТОРИЗАЦИИ")
        if not wialon_service.authenticate():
            print("❌ Ошибка авторизации в Wialon")
            return
        print("✅ Авторизация успешна")
        print(f"   SID: {wialon_service.sid}")
        
        # 2. Получаем полный список устройств
        print("\n2️⃣ ПОЛУЧЕНИЕ СПИСКА УСТРОЙСТВ")
        units = wialon_service.get_units_list()
        if not units:
            print("❌ Не удалось получить список устройств")
            return
        
        print(f"✅ Получено {len(units)} устройств:")
        for unit in units:
            print(f"   📱 {unit['nm']} (ID: {unit['id']})")
            print(f"      - Флаги: {unit.get('flags', 'N/A')}")
            print(f"      - MU: {unit.get('mu', 'N/A')}")
            print(f"      - POS: {unit.get('pos', 'N/A')}")
            print()
        
        # 3. Детальная проверка каждого устройства
        print("3️⃣ ДЕТАЛЬНАЯ ПРОВЕРКА УСТРОЙСТВ")
        
        target_units = [
            {"name": "484 ATL 01", "id": 29603155},
            {"name": "355 ATL 01", "id": 29682916}, 
            {"name": "359 AUL 01", "id": 29682864},
            {"name": "695 BHS 02", "id": 29682886}
        ]
        
        for target_unit in target_units:
            print(f"\n🔍 Проверяем {target_unit['name']} (ID: {target_unit['id']})")
            
            try:
                # Пробуем разные флаги для получения данных
                flags_to_try = [
                    0x1,    # Базовая информация
                    0x10,   # Позиция
                    0x100,  # Параметры
                    0x1000, # Сообщения
                    0x1FFF, # Все флаги
                ]
                
                for flag in flags_to_try:
                    print(f"   🚩 Флаг {flag} (0x{flag:x}):")
                    
                    try:
                        position_url = f"{wialon_service.base_url}/wialon/ajax.html"
                        params = {
                            'svc': 'core/search_item',
                            'params': json.dumps({
                                'id': target_unit['id'],
                                'flags': flag
                            }),
                            'sid': wialon_service.sid
                        }
                        
                        response = wialon_service.session.get(position_url, params=params, timeout=30)
                        response.raise_for_status()
                        
                        data = response.json()
                        
                        if isinstance(data, dict) and 'item' in data:
                            item = data['item']
                            print(f"      ✅ Данные получены:")
                            
                            # Анализируем что есть в данных
                            if 'pos' in item:
                                pos = item['pos']
                                print(f"         📍 Позиция: lat={pos.get('y', 'N/A')}, lon={pos.get('x', 'N/A')}")
                                print(f"         🚗 Скорость: {pos.get('s', 'N/A')} мм/ч")
                                print(f"         🧭 Направление: {pos.get('c', 'N/A')}°")
                                print(f"         📡 Спутники: {pos.get('sc', 'N/A')}")
                                print(f"         ⏰ Время: {pos.get('t', 'N/A')}")
                            
                            if 'params' in item:
                                params_data = item['params']
                                print(f"         ⚙️ Параметры: {len(params_data)} параметров")
                                for param in params_data[:5]:  # Показываем первые 5
                                    print(f"            - {param.get('n', 'N/A')}: {param.get('v', 'N/A')}")
                            
                            if 'messages' in item:
                                messages = item['messages']
                                print(f"         💬 Сообщения: {len(messages)} сообщений")
                            
                            break  # Если получили данные, переходим к следующему устройству
                            
                        elif isinstance(data, list) and len(data) > 0:
                            if 'error' in data[0]:
                                print(f"      ❌ Ошибка: {data[0]['error']}")
                            else:
                                print(f"      ✅ Данные получены (список): {len(data)} элементов")
                        else:
                            print(f"      ⚠️ Нет данных")
                            
                    except Exception as e:
                        print(f"      ❌ Ошибка запроса: {e}")
                
            except Exception as e:
                print(f"   ❌ Общая ошибка для {target_unit['name']}: {e}")
        
        # 4. Проверяем историю сообщений
        print("\n4️⃣ ПРОВЕРКА ИСТОРИИ СООБЩЕНИЙ")
        
        for target_unit in target_units:
            print(f"\n📜 История сообщений для {target_unit['name']}:")
            
            try:
                # Запрос истории сообщений за последние 24 часа
                history_url = f"{wialon_service.base_url}/wialon/ajax.html"
                params = {
                    'svc': 'messages/load_interval',
                    'params': json.dumps({
                        'itemId': target_unit['id'],
                        'timeFrom': int((datetime.now().timestamp() - 86400) * 1000),  # 24 часа назад
                        'timeTo': int(datetime.now().timestamp() * 1000),  # Сейчас
                        'flags': 0x1
                    }),
                    'sid': wialon_service.sid
                }
                
                response = wialon_service.session.get(history_url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if isinstance(data, dict) and 'messages' in data:
                    messages = data['messages']
                    print(f"   ✅ Получено {len(messages)} сообщений за последние 24 часа")
                    
                    if messages:
                        # Показываем последние 3 сообщения
                        for msg in messages[-3:]:
                            if 'pos' in msg:
                                pos = msg['pos']
                                timestamp = datetime.fromtimestamp(msg.get('t', 0) / 1000)
                                print(f"      📍 {timestamp}: lat={pos.get('y', 'N/A')}, lon={pos.get('x', 'N/A')}, speed={pos.get('s', 'N/A')}")
                else:
                    print(f"   ⚠️ Нет сообщений или ошибка: {data}")
                    
            except Exception as e:
                print(f"   ❌ Ошибка получения истории: {e}")
        
        # 5. Проверяем статус устройств
        print("\n5️⃣ СТАТУС УСТРОЙСТВ")
        
        for target_unit in target_units:
            print(f"\n📊 Статус {target_unit['name']}:")
            
            try:
                status_url = f"{wialon_service.base_url}/wialon/ajax.html"
                params = {
                    'svc': 'core/get_hw_info',
                    'params': json.dumps({
                        'itemId': target_unit['id']
                    }),
                    'sid': wialon_service.sid
                }
                
                response = wialon_service.session.get(status_url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                print(f"   📡 Статус устройства: {data}")
                
            except Exception as e:
                print(f"   ❌ Ошибка получения статуса: {e}")
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")

if __name__ == "__main__":
    detailed_wialon_analysis()


