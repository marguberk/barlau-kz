#!/usr/bin/env python3
import requests
import json

# Тестируем Wialon API напрямую
base_url = "https://hst-api.wialon.com"
access_token = "84582de9332f6d15227795a639a37d94DD3C6E56E170623AAC680089A097C9D1CBD30C52"

def test_wialon_auth():
    """Тестируем авторизацию в Wialon API"""
    try:
        auth_url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'token/login',
            'params': json.dumps({
                'token': access_token
            }),
            'sid': ''
        }
        
        print(f"🔐 Тестируем авторизацию в Wialon API...")
        print(f"URL: {auth_url}")
        print(f"Params: {params}")
        
        response = requests.get(auth_url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Parsed JSON: {type(data)}")
            if isinstance(data, dict) and 'eid' in data:
                print(f"✅ Авторизация успешна! SID: {data.get('eid', 'N/A')}")
                return data.get('eid')
            elif isinstance(data, list) and len(data) > 0 and 'error' not in data[0]:
                print(f"✅ Авторизация успешна! SID: {data[0].get('eid', 'N/A')}")
                return data[0].get('eid')
            else:
                error_msg = data.get('error', 'Неизвестная ошибка') if isinstance(data, dict) else (data[0].get('error', 'Неизвестная ошибка') if isinstance(data, list) and len(data) > 0 else 'Ошибка авторизации')
                print(f"❌ Ошибка авторизации: {error_msg}")
                return None
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return None

def test_get_units(sid):
    """Тестируем получение списка GPS устройств"""
    try:
        units_url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/search_items',
            'params': json.dumps({
                'spec': {
                    'itemsType': 'avl_unit',
                    'propName': 'sys_name,phone,relay_state',
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
        
        print(f"\n📡 Получаем список GPS устройств...")
        print(f"URL: {units_url}")
        print(f"SID: {sid}")
        
        response = requests.get(units_url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'items' in data:
                units = data['items']
                print(f"✅ Получено {len(units)} GPS устройств:")
                for i, unit in enumerate(units[:5]):  # Показываем первые 5
                    print(f"  {i+1}. {unit.get('nm', 'N/A')} (ID: {unit.get('id', 'N/A')})")
                return units
            elif isinstance(data, list) and len(data) > 0 and 'error' not in data[0]:
                units = data[0].get('items', [])
                print(f"✅ Получено {len(units)} GPS устройств:")
                for i, unit in enumerate(units[:5]):  # Показываем первые 5
                    print(f"  {i+1}. {unit.get('nm', 'N/A')} (ID: {unit.get('id', 'N/A')})")
                return units
            else:
                error_msg = data.get('error', 'Неизвестная ошибка') if isinstance(data, dict) else (data[0].get('error', 'Неизвестная ошибка') if isinstance(data, list) and len(data) > 0 else 'Ошибка получения списка')
                print(f"❌ Ошибка получения списка: {error_msg}")
                return None
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка получения списка: {e}")
        return None

def test_get_unit_position(sid, unit_id):
    """Тестируем получение позиции GPS устройства"""
    try:
        position_url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/search_item',
            'params': json.dumps({
                'id': unit_id,
                'flags': 0x1  # Флаг для получения позиции
            }),
            'sid': sid
        }
        
        print(f"\n📍 Получаем позицию устройства {unit_id}...")
        print(f"URL: {position_url}")
        print(f"Params: {params}")
        
        response = requests.get(position_url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Parsed JSON: {type(data)}")
            if isinstance(data, dict) and 'item' in data:
                unit_data = data['item']
                if 'pos' in unit_data:
                    pos = unit_data['pos']
                    print(f"✅ Позиция найдена: {pos.get('y', 0)}, {pos.get('x', 0)}")
                    return pos
                else:
                    print(f"⚠️ Нет данных о позиции в ответе")
                    return None
            else:
                print(f"⚠️ Неожиданная структура ответа")
                return None
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка получения позиции: {e}")
        return None

if __name__ == "__main__":
    print("🛰️ Тестирование Wialon API")
    print("=" * 50)
    
    # Тестируем авторизацию
    sid = test_wialon_auth()
    
    if sid:
        # Тестируем получение списка устройств
        units = test_get_units(sid)
        
        if units:
            print(f"\n✅ Wialon API работает корректно!")
            print(f"📊 Найдено {len(units)} GPS устройств")
            
            # Тестируем получение позиции для первого устройства
            if len(units) > 0:
                first_unit = units[0]
                unit_id = first_unit.get('id')
                unit_name = first_unit.get('nm')
                print(f"\n📍 Тестируем получение позиции для {unit_name} (ID: {unit_id})")
                position = test_get_unit_position(sid, unit_id)
                if position:
                    print(f"✅ Позиция получена успешно!")
                else:
                    print(f"⚠️ Не удалось получить позицию")
        else:
            print(f"\n❌ Не удалось получить список устройств")
    else:
        print(f"\n❌ Не удалось авторизоваться в Wialon API")
