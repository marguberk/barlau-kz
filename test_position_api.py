#!/usr/bin/env python3
import requests
import json

# Тестируем разные API endpoints для получения позиции
base_url = "https://hst-api.wialon.com"
access_token = "84582de9332f6d15227795a639a37d94DD3C6E56E170623AAC680089A097C9D1CBD30C52"
device_id = "29603155"  # ID устройства для 484ATL01

def test_position_endpoints(sid):
    """Тестируем разные endpoints для получения позиции"""
    
    endpoints_to_test = [
        {
            'name': 'core/get_position',
            'params': {'itemId': device_id}
        },
        {
            'name': 'core/search_item',
            'params': {'id': device_id, 'flags': 0x3}  # Позиция + параметры
        },
        {
            'name': 'core/search_item',
            'params': {'id': device_id, 'flags': 0x7}  # Позиция + параметры + датчики
        },
        {
            'name': 'core/search_item',
            'params': {'id': device_id, 'flags': 0xF}  # Все основные флаги
        },
        {
            'name': 'core/search_item',
            'params': {'id': device_id, 'flags': 0x1F}  # Все флаги
        },
        {
            'name': 'core/search_item',
            'params': {'id': device_id, 'flags': 0x3F}  # Расширенные флаги
        },
    ]
    
    for endpoint in endpoints_to_test:
        print(f"\n🔍 Тестируем {endpoint['name']} с параметрами {endpoint['params']}")
        
        try:
            url = f"{base_url}/wialon/ajax.html"
            params = {
                'svc': endpoint['name'],
                'params': json.dumps(endpoint['params']),
                'sid': sid
            }
            
            response = requests.get(url, params=params, timeout=30)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                # Ищем позицию в разных местах ответа
                if isinstance(data, dict):
                    if 'pos' in data:
                        pos = data['pos']
                        print(f"✅ Позиция найдена в корне: {pos}")
                    elif 'item' in data and isinstance(data['item'], dict) and 'pos' in data['item']:
                        pos = data['item']['pos']
                        print(f"✅ Позиция найдена в item: {pos}")
                    elif 'items' in data and isinstance(data['items'], list):
                        for item in data['items']:
                            if isinstance(item, dict) and 'pos' in item:
                                pos = item['pos']
                                print(f"✅ Позиция найдена в items: {pos}")
                                break
                    else:
                        print(f"⚠️ Позиция не найдена в ответе")
                        
                        # Проверяем, есть ли поле с координатами в других местах
                        def find_coordinates(obj, path=""):
                            if isinstance(obj, dict):
                                for key, value in obj.items():
                                    if key in ['y', 'lat', 'latitude', 'x', 'lon', 'longitude']:
                                        print(f"  Найдены координаты в {path}.{key}: {value}")
                                    find_coordinates(value, f"{path}.{key}" if path else key)
                            elif isinstance(obj, list):
                                for i, item in enumerate(obj):
                                    find_coordinates(item, f"{path}[{i}]")
                        
                        find_coordinates(data)
            else:
                print(f"❌ HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")

def test_monitoring_data(sid):
    """Тестируем получение данных мониторинга"""
    try:
        print(f"\n📊 Тестируем получение данных мониторинга...")
        
        url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/get_monitoring_data',
            'params': json.dumps({
                'spec': [device_id],
                'timeFrom': 1759000000,  # Недавнее время
                'timeTo': 1759067329,    # Текущее время
                'flags': 0x1
            }),
            'sid': sid
        }
        
        response = requests.get(url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Monitoring Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка получения данных мониторинга: {e}")

if __name__ == "__main__":
    print("🛰️ Тестирование API endpoints для получения позиции 484ATL01")
    print("=" * 70)
    
    # Сначала авторизуемся
    try:
        auth_url = f"{base_url}/wialon/ajax.html"
        auth_params = {
            'svc': 'token/login',
            'params': json.dumps({'token': access_token}),
            'sid': ''
        }
        
        response = requests.get(auth_url, params=auth_params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'eid' in data:
                sid = data['eid']
                print(f"✅ Авторизация успешна! SID: {sid}")
                
                # Тестируем endpoints
                test_position_endpoints(sid)
                test_monitoring_data(sid)
            else:
                print(f"❌ Ошибка авторизации")
        else:
            print(f"❌ HTTP ошибка авторизации: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка авторизации: {e}")
