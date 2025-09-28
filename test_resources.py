#!/usr/bin/env python3
import requests
import json

# Проверяем ресурсы и права доступа
base_url = "https://hst-api.wialon.com"
access_token = "84582de9332f6d15227795a639a37d94DD3C6E56E170623AAC680089A097C9D1CBD30C52"

def test_auth():
    """Авторизация"""
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
                return data['eid'], data
        return None, None
    except:
        return None, None

def check_resources(sid):
    """Проверяем доступные ресурсы"""
    print("📋 Проверяем доступные ресурсы...")
    
    try:
        # Получаем ресурсы
        url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/search_items',
            'params': json.dumps({
                'spec': {
                    'itemsType': 'avl_resource',
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
        
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"Resources Response: {json.dumps(data, indent=2)}")
            
            if isinstance(data, dict) and 'items' in data:
                resources = data['items']
                print(f"✅ Найдено {len(resources)} ресурсов:")
                
                for i, resource in enumerate(resources):
                    print(f"  {i+1}. {resource.get('nm', 'N/A')} (ID: {resource.get('id', 'N/A')})")
                    print(f"      Права: {resource.get('uacl', 'N/A')}")
                    
                return resources
            else:
                print(f"❌ Неожиданная структура ответа")
                return None
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def check_user_info(auth_data):
    """Проверяем информацию о пользователе"""
    print(f"\n👤 Информация о пользоватеle:")
    
    if 'user' in auth_data:
        user = auth_data['user']
        print(f"  Имя: {user.get('nm', 'N/A')}")
        print(f"  ID: {user.get('id', 'N/A')}")
        print(f"  Класс: {user.get('cls', 'N/A')}")
        
        if 'prp' in user:
            prp = user['prp']
            print(f"  Свойства пользователя:")
            for key, value in prp.items():
                print(f"    {key}: {value}")
        
        if 'uacl' in user:
            uacl = user['uacl']
            print(f"  Права доступа: {uacl}")
            
            # Расшифровываем права
            rights = {
                0x1: "Мониторинг",
                0x2: "Отчеты", 
                0x4: "Управление",
                0x8: "Администрирование",
                0x10: "Биллинг",
                0x20: "API",
                0x40: "Экспорт",
                0x80: "Импорт"
            }
            
            print(f"  Расшифровка прав:")
            for right, name in rights.items():
                if uacl & right:
                    print(f"    ✅ {name}")

def test_different_search(sid):
    """Тестируем разные способы поиска устройств"""
    print(f"\n🔍 Тестируем разные способы поиска устройств...")
    
    # Способ 1: Поиск по всем типам
    print(f"  📋 Способ 1: Поиск по всем типам")
    try:
        url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/search_items',
            'params': json.dumps({
                'spec': {
                    'itemsType': 'avl_unit',
                    'propName': 'sys_name',
                    'propValueMask': '484*',  # Ищем по номеру
                    'sortType': 'sys_name'
                },
                'force': 1,
                'flags': 1,
                'from': 0,
                'to': 0
            }),
            'sid': sid
        }
        
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"    Response: {json.dumps(data, indent=2)}")
            
            if isinstance(data, dict) and 'items' in data:
                units = data['items']
                print(f"    ✅ Найдено {len(units)} устройств с номером 484")
            else:
                print(f"    ⚠️ Не найдено устройств с номером 484")
        else:
            print(f"    ❌ HTTP ошибка: {response.status_code}")
    except Exception as e:
        print(f"    ❌ Ошибка: {e}")
    
    # Способ 2: Поиск без фильтра
    print(f"  📋 Способ 2: Поиск без фильтра")
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
        if response.status_code == 200:
            data = response.json()
            print(f"    Response: {json.dumps(data, indent=2)}")
            
            if isinstance(data, dict) and 'items' in data:
                units = data['items']
                print(f"    ✅ Найдено {len(units)} устройств")
            else:
                print(f"    ⚠️ Не найдено устройств")
        else:
            print(f"    ❌ HTTP ошибка: {response.status_code}")
    except Exception as e:
        print(f"    ❌ Ошибка: {e}")

def test_alternative_endpoints(sid):
    """Тестируем альтернативные API endpoints"""
    print(f"\n🔄 Тестируем альтернативные API endpoints...")
    
    # Тестируем разные endpoints
    endpoints = [
        'core/get_monitoring_data',
        'core/get_messages',
        'core/search_item',
        'core/get_position',
        'unit/get_messages',
        'unit/get_position'
    ]
    
    unit_id = 29603155  # 484 ATL 01
    
    for endpoint in endpoints:
        print(f"  🔍 Тестируем {endpoint}")
        try:
            url = f"{base_url}/wialon/ajax.html"
            
            # Разные параметры для разных endpoints
            if endpoint == 'core/get_monitoring_data':
                params_data = {
                    'spec': [unit_id],
                    'timeFrom': 1758000000,
                    'timeTo': 1759067726,
                    'flags': 0x1
                }
            elif endpoint in ['core/get_messages', 'unit/get_messages']:
                params_data = {
                    'itemId': unit_id,
                    'timeFrom': 1758000000,
                    'timeTo': 1759067726,
                    'flags': 0x1
                }
            elif endpoint in ['core/get_position', 'unit/get_position']:
                params_data = {
                    'itemId': unit_id
                }
            else:  # core/search_item
                params_data = {
                    'id': unit_id,
                    'flags': 0x1F
                }
            
            params = {
                'svc': endpoint,
                'params': json.dumps(params_data),
                'sid': sid
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                print(f"    Status: {response.status_code}")
                print(f"    Response: {json.dumps(data, indent=2)}")
                
                # Проверяем, есть ли позиция
                if isinstance(data, dict):
                    if 'pos' in data:
                        print(f"    ✅ Позиция найдена в корне!")
                    elif 'item' in data and isinstance(data['item'], dict) and 'pos' in data['item']:
                        print(f"    ✅ Позиция найдена в item!")
                    elif 'messages' in data and isinstance(data['messages'], list) and len(data['messages']) > 0:
                        last_msg = data['messages'][-1]
                        if 'pos' in last_msg:
                            print(f"    ✅ Позиция найдена в последнем сообщении!")
                    elif 'error' in data:
                        print(f"    ❌ Ошибка API: {data['error']}")
                    else:
                        print(f"    ⚠️ Позиция не найдена")
            else:
                print(f"    ❌ HTTP ошибка: {response.status_code}")
        except Exception as e:
            print(f"    ❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🛰️ Проверка ресурсов и альтернативных endpoints")
    print("=" * 60)
    
    sid, auth_data = test_auth()
    if sid and auth_data:
        print(f"✅ Авторизация успешна! SID: {sid}")
        
        # Проверяем информацию о пользователе
        check_user_info(auth_data)
        
        # Проверяем ресурсы
        resources = check_resources(sid)
        
        # Тестируем разные способы поиска
        test_different_search(sid)
        
        # Тестируем альтернативные endpoints
        test_alternative_endpoints(sid)
    else:
        print("❌ Ошибка авторизации")
