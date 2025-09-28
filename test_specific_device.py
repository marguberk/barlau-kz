#!/usr/bin/env python3
import requests
import json

# Тестируем конкретное GPS устройство 484ATL01
base_url = "https://hst-api.wialon.com"
access_token = "84582de9332f6d15227795a639a37d94DD3C6E56E170623AAC680089A097C9D1CBD30C52"
device_id = "29603155"  # ID устройства для 484ATL01

def test_device_details(sid):
    """Тестируем получение детальной информации об устройстве"""
    try:
        # Пробуем разные флаги для получения данных
        flags_to_test = [
            0x1,    # Базовая информация
            0x2,    # Позиция
            0x4,    # Параметры
            0x8,    # Датчики
            0x10,   # Состояние
            0x1F,   # Все флаги
        ]
        
        for flags in flags_to_test:
            print(f"\n🔍 Тестируем флаги: {flags} (0x{flags:02X})")
            
            url = f"{base_url}/wialon/ajax.html"
            params = {
                'svc': 'core/search_item',
                'params': json.dumps({
                    'id': device_id,
                    'flags': flags
                }),
                'sid': sid
            }
            
            response = requests.get(url, params=params, timeout=30)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                if isinstance(data, dict) and 'item' in data:
                    item = data['item']
                    if 'pos' in item:
                        pos = item['pos']
                        print(f"✅ Позиция найдена: lat={pos.get('y')}, lon={pos.get('x')}, speed={pos.get('s')}")
                    else:
                        print(f"⚠️ Позиция не найдена в ответе")
                        
                    # Проверяем другие поля
                    for key in ['nm', 'cls', 'id', 'mu', 'uacl']:
                        if key in item:
                            print(f"  {key}: {item[key]}")
            else:
                print(f"❌ HTTP ошибка: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_device_messages(sid):
    """Тестируем получение сообщений устройства"""
    try:
        print(f"\n📨 Тестируем получение сообщений устройства...")
        
        url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/get_messages',
            'params': json.dumps({
                'itemId': device_id,
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
            print(f"Messages Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка получения сообщений: {e}")

if __name__ == "__main__":
    print("🛰️ Тестирование конкретного GPS устройства 484ATL01")
    print("=" * 60)
    
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
                
                # Тестируем устройство
                test_device_details(sid)
                test_device_messages(sid)
            else:
                print(f"❌ Ошибка авторизации")
        else:
            print(f"❌ HTTP ошибка авторизации: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка авторизации: {e}")
