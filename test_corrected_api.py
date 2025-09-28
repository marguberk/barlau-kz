#!/usr/bin/env python3
import requests
import json

# Тестируем с исправленным форматом запроса
base_url = "https://hst-api.wialon.com"
access_token = "84582de9332f6d15227795a639a37d94DD3C6E56E170623AAC680089A097C9D1CBD30C52"

def test_corrected_auth():
    """Тестируем авторизацию с исправленным форматом"""
    print("🔐 Тестируем авторизацию...")
    
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

def test_search_items_corrected(sid):
    """Тестируем получение устройств с исправленным форматом"""
    print(f"\n📡 Получаем список устройств с исправленным форматом...")
    
    try:
        # Исправляем формат согласно документации
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
        
        print(f"URL: {units_url}")
        print(f"Params: {params}")
        
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

def test_different_search_methods(sid):
    """Тестируем разные методы поиска устройств"""
    print(f"\n🔍 Тестируем разные методы поиска...")
    
    # Метод 1: Без spec
    print(f"\n  📋 Метод 1: Без spec")
    try:
        url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/search_items',
            'params': json.dumps({
                'force': 1,
                'flags': 1,
                'from': 0,
                'to': 0
            }),
            'sid': sid
        }
        
        response = requests.get(url, params=params, timeout=30)
        print(f"    Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"    Response: {json.dumps(data, indent=2)}")
            
            if isinstance(data, dict) and 'items' in data:
                units = data['items']
                print(f"    ✅ Получено {len(units)} устройств")
                return units
        else:
            print(f"    ❌ HTTP ошибка")
            
    except Exception as e:
        print(f"    ❌ Ошибка: {e}")
    
    # Метод 2: С упрощенным spec
    print(f"\n  📋 Метод 2: С упрощенным spec")
    try:
        url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/search_items',
            'params': json.dumps({
                'spec': {
                    'itemsType': 'avl_unit'
                },
                'force': 1,
                'flags': 1,
                'from': 0,
                'to': 0
            }),
            'sid': sid
        }
        
        response = requests.get(url, params=params, timeout=30)
        print(f"    Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"    Response: {json.dumps(data, indent=2)}")
            
            if isinstance(data, dict) and 'items' in data:
                units = data['items']
                print(f"    ✅ Получено {len(units)} устройств")
                return units
        else:
            print(f"    ❌ HTTP ошибка")
            
    except Exception as e:
        print(f"    ❌ Ошибка: {e}")
    
    # Метод 3: Получить все ресурсы
    print(f"\n  📋 Метод 3: Получить все ресурсы")
    try:
        url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/search_items',
            'params': json.dumps({
                'spec': {
                    'itemsType': 'avl_resource'
                },
                'force': 1,
                'flags': 1,
                'from': 0,
                'to': 0
            }),
            'sid': sid
        }
        
        response = requests.get(url, params=params, timeout=30)
        print(f"    Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"    Response: {json.dumps(data, indent=2)}")
            
            if isinstance(data, dict) and 'items' in data:
                resources = data['items']
                print(f"    ✅ Получено {len(resources)} ресурсов")
                
                # Теперь получаем устройства из ресурса
                if len(resources) > 0:
                    resource_id = resources[0]['id']
                    print(f"    🔍 Получаем устройства из ресурса {resource_id}")
                    
                    url2 = f"{base_url}/wialon/ajax.html"
                    params2 = {
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
                    
                    response2 = requests.get(url2, params=params2, timeout=30)
                    if response2.status_code == 200:
                        data2 = response2.json()
                        print(f"    Units Response: {json.dumps(data2, indent=2)}")
                        
                        if isinstance(data2, dict) and 'items' in data2:
                            units = data2['items']
                            print(f"    ✅ Получено {len(units)} устройств")
                            return units
        else:
            print(f"    ❌ HTTP ошибка")
            
    except Exception as e:
        print(f"    ❌ Ошибка: {e}")
    
    return None

if __name__ == "__main__":
    print("🛰️ Тестирование с исправленным форматом API")
    print("=" * 60)
    
    # Тестируем авторизацию
    sid = test_corrected_auth()
    
    if sid:
        # Тестируем разные методы поиска
        units = test_different_search_methods(sid)
        
        if units:
            print(f"\n✅ Успешно получен список устройств!")
            print(f"📊 Найдено {len(units)} устройств")
        else:
            print(f"\n❌ Не удалось получить список устройств")
    else:
        print(f"\n❌ Не удалось авторизоваться")
