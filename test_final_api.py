#!/usr/bin/env python3
import requests
import json

# Финальный тест с правильным форматом API
base_url = "https://hst-api.wialon.com"
access_token = "84582de9332f6d15227795a639a37d94DD3C6E56E170623AAC680089A097C9D1CBD30C52"

def test_final_auth():
    """Финальный тест авторизации"""
    print("🔐 Финальный тест авторизации...")
    
    try:
        auth_url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'token/login',
            'params': json.dumps({'token': access_token}),
            'sid': ''
        }
        
        response = requests.get(auth_url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'eid' in data:
                sid = data['eid']
                print(f"✅ Авторизация успешна! SID: {sid}")
                return sid
            else:
                print(f"❌ Ошибка авторизации: {data}")
                return None
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка авторизации: {e}")
        return None

def test_get_units_final(sid):
    """Финальный тест получения устройств"""
    print(f"\n📡 Финальный тест получения устройств...")
    
    # Используем точный формат из документации Wialon
    try:
        units_url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/search_items',
            'params': json.dumps({
                'spec': {
                    'itemsType': 'avl_unit',
                    'propName': 'sys_name',
                    'propValueMask': '*',
                    'sortType': 'sys_name'
                },
                'force': 1,
                'flags': 1,
                'from': 0,
                'to': 0
            }),
            'sid': sid
        }
        
        print(f"URL: {units_url}")
        print(f"Params: {json.dumps(params, indent=2)}")
        
        response = requests.get(units_url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, dict) and 'items' in data:
                units = data['items']
                print(f"✅ Получено {len(units)} устройств:")
                
                for i, unit in enumerate(units):
                    print(f"  {i+1}. {unit.get('nm', 'N/A')} (ID: {unit.get('id', 'N/A')})")
                    
                return units
            elif isinstance(data, dict) and 'error' in data:
                print(f"❌ Ошибка API: {data['error']}")
                if 'reason' in data:
                    print(f"Причина: {data['reason']}")
                return None
            else:
                print(f"❌ Неожиданная структура ответа: {data}")
                return None
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка получения устройств: {e}")
        return None

def test_get_unit_position_final(sid, unit_id):
    """Финальный тест получения позиции устройства"""
    print(f"\n📍 Финальный тест получения позиции устройства {unit_id}...")
    
    try:
        # Используем разные методы получения позиции
        methods = [
            {
                'name': 'core/get_position',
                'params': {'itemId': unit_id}
            },
            {
                'name': 'core/search_item',
                'params': {'id': unit_id, 'flags': 0x4}  # Флаг позиции
            },
            {
                'name': 'core/search_item', 
                'params': {'id': unit_id, 'flags': 0x1F}  # Все основные флаги
            }
        ]
        
        for method in methods:
            print(f"\n  🔍 Тестируем {method['name']} с параметрами {method['params']}")
            
            url = f"{base_url}/wialon/ajax.html"
            params = {
                'svc': method['name'],
                'params': json.dumps(method['params']),
                'sid': sid
            }
            
            response = requests.get(url, params=params, timeout=30)
            print(f"    Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"    Response: {json.dumps(data, indent=2)}")
                
                # Ищем позицию в ответе
                position_found = False
                if isinstance(data, dict):
                    if 'pos' in data:
                        pos = data['pos']
                        print(f"    ✅ Позиция найдена в корне: {pos}")
                        position_found = True
                    elif 'item' in data and isinstance(data['item'], dict) and 'pos' in data['item']:
                        pos = data['item']['pos']
                        print(f"    ✅ Позиция найдена в item: {pos}")
                        position_found = True
                
                if position_found:
                    return True
            else:
                print(f"    ❌ HTTP ошибка")
        
        return False
        
    except Exception as e:
        print(f"❌ Ошибка получения позиции: {e}")
        return False

def test_get_messages_final(sid, unit_id):
    """Финальный тест получения сообщений устройства"""
    print(f"\n📨 Финальный тест получения сообщений устройства {unit_id}...")
    
    try:
        # Получаем сообщения за последний час
        current_time = 1759067726  # Текущее время
        hour_ago = current_time - 3600
        
        url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/get_messages',
            'params': json.dumps({
                'itemId': unit_id,
                'timeFrom': hour_ago,
                'timeTo': current_time,
                'flags': 0x1
            }),
            'sid': sid
        }
        
        print(f"URL: {url}")
        print(f"Params: {json.dumps(params, indent=2)}")
        
        response = requests.get(url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, dict) and 'messages' in data:
                messages = data['messages']
                print(f"✅ Получено {len(messages)} сообщений")
                
                if messages:
                    last_msg = messages[-1]
                    if 'pos' in last_msg:
                        pos = last_msg['pos']
                        print(f"📍 Последняя позиция: {pos.get('y')}, {pos.get('x')}")
                        print(f"🚗 Скорость: {pos.get('s', 0) * 3.6:.1f} км/ч")
                        print(f"🕐 Время: {last_msg.get('t', 'N/A')}")
                        return True
                else:
                    print(f"⚠️ Нет сообщений за последний час")
                    return False
            elif isinstance(data, dict) and 'error' in data:
                print(f"❌ Ошибка API: {data['error']}")
                return False
            else:
                print(f"❌ Неожиданная структура ответа: {data}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка получения сообщений: {e}")
        return False

if __name__ == "__main__":
    print("🛰️ Финальное тестирование Wialon API")
    print("=" * 60)
    
    # Тестируем авторизацию
    sid = test_final_auth()
    
    if sid:
        # Получаем список устройств
        units = test_get_units_final(sid)
        
        if units:
            print(f"\n✅ Успешно получен список устройств!")
            print(f"📊 Найдено {len(units)} устройств")
            
            # Тестируем первое устройство
            if len(units) > 0:
                first_unit = units[0]
                unit_id = first_unit.get('id')
                unit_name = first_unit.get('nm')
                
                print(f"\n🎯 Тестируем устройство {unit_name} (ID: {unit_id})")
                
                # Тестируем получение позиции
                has_position = test_get_unit_position_final(sid, unit_id)
                
                # Тестируем получение сообщений
                has_messages = test_get_messages_final(sid, unit_id)
                
                print(f"\n📊 Результаты тестирования:")
                print(f"  📍 Позиция: {'✅ Есть' if has_position else '❌ Нет'}")
                print(f"  📨 Сообщения: {'✅ Есть' if has_messages else '❌ Нет'}")
                
                if has_position or has_messages:
                    print(f"\n✅ Устройство {unit_name} передает данные!")
                else:
                    print(f"\n⚠️ Устройство {unit_name} не передает данные")
                    print(f"💡 Обратитесь к поставщику GPS трекеров для активации")
        else:
            print(f"\n❌ Не удалось получить список устройств")
    else:
        print(f"\n❌ Не удалось авторизоваться")
