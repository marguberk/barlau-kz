#!/usr/bin/env python3
import requests
import json

# Проверяем, возможно устройства активны, но мы неправильно запрашиваем данные
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
                return data['eid']
        return None
    except:
        return None

def test_monitoring_data(sid):
    """Проверяем данные мониторинга - возможно устройства активны"""
    print("📊 Проверяем данные мониторинга...")
    
    try:
        # Получаем все устройства
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
        
        response = requests.get(units_url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'items' in data:
                units = data['items']
                print(f"✅ Получено {len(units)} устройств")
                
                # Проверяем каждое устройство разными способами
                for unit in units:
                    unit_id = unit['id']
                    unit_name = unit['nm']
                    print(f"\n🚛 Проверяем {unit_name} (ID: {unit_id})")
                    
                    # Способ 1: core/get_monitoring_data
                    print(f"  📊 Способ 1: core/get_monitoring_data")
                    try:
                        url = f"{base_url}/wialon/ajax.html"
                        params = {
                            'svc': 'core/get_monitoring_data',
                            'params': json.dumps({
                                'spec': [unit_id],
                                'timeFrom': 1759000000,
                                'timeTo': 1759067726,
                                'flags': 0x1
                            }),
                            'sid': sid
                        }
                        
                        response = requests.get(url, params=params, timeout=30)
                        if response.status_code == 200:
                            data = response.json()
                            print(f"    Response: {json.dumps(data, indent=2)}")
                            
                            if isinstance(data, dict) and 'items' in data:
                                items = data['items']
                                if items and len(items) > 0:
                                    item = items[0]
                                    if 'pos' in item:
                                        pos = item['pos']
                                        print(f"    ✅ Позиция найдена: {pos.get('y')}, {pos.get('x')}")
                                        print(f"    🚗 Скорость: {pos.get('s', 0) * 3.6:.1f} км/ч")
                                        print(f"    🕐 Время: {pos.get('t', 'N/A')}")
                                        continue
                    except Exception as e:
                        print(f"    ❌ Ошибка: {e}")
                    
                    # Способ 2: core/get_messages с большим временным окном
                    print(f"  📨 Способ 2: core/get_messages (большое окно)")
                    try:
                        url = f"{base_url}/wialon/ajax.html"
                        params = {
                            'svc': 'core/get_messages',
                            'params': json.dumps({
                                'itemId': unit_id,
                                'timeFrom': 1758000000,  # Больше окно - неделю назад
                                'timeTo': 1759067726,
                                'flags': 0x1
                            }),
                            'sid': sid
                        }
                        
                        response = requests.get(url, params=params, timeout=30)
                        if response.status_code == 200:
                            data = response.json()
                            print(f"    Response: {json.dumps(data, indent=2)}")
                            
                            if isinstance(data, dict) and 'messages' in data:
                                messages = data['messages']
                                if messages:
                                    last_msg = messages[-1]
                                    if 'pos' in last_msg:
                                        pos = last_msg['pos']
                                        print(f"    ✅ Последняя позиция: {pos.get('y')}, {pos.get('x')}")
                                        print(f"    🚗 Скорость: {pos.get('s', 0) * 3.6:.1f} км/ч")
                                        print(f"    🕐 Время: {last_msg.get('t', 'N/A')}")
                                        continue
                    except Exception as e:
                        print(f"    ❌ Ошибка: {e}")
                    
                    # Способ 3: core/search_item с флагом позиции
                    print(f"  🔍 Способ 3: core/search_item (флаг позиции)")
                    try:
                        url = f"{base_url}/wialon/ajax.html"
                        params = {
                            'svc': 'core/search_item',
                            'params': json.dumps({
                                'id': unit_id,
                                'flags': 0x4  # Флаг позиции
                            }),
                            'sid': sid
                        }
                        
                        response = requests.get(url, params=params, timeout=30)
                        if response.status_code == 200:
                            data = response.json()
                            print(f"    Response: {json.dumps(data, indent=2)}")
                            
                            if isinstance(data, dict) and 'item' in data:
                                item = data['item']
                                if 'pos' in item:
                                    pos = item['pos']
                                    print(f"    ✅ Позиция найдена: {pos.get('y')}, {pos.get('x')}")
                                    print(f"    🚗 Скорость: {pos.get('s', 0) * 3.6:.1f} км/ч")
                                    print(f"    🕐 Время: {pos.get('t', 'N/A')}")
                                    continue
                    except Exception as e:
                        print(f"    ❌ Ошибка: {e}")
                    
                    # Способ 4: core/get_position
                    print(f"  📍 Способ 4: core/get_position")
                    try:
                        url = f"{base_url}/wialon/ajax.html"
                        params = {
                            'svc': 'core/get_position',
                            'params': json.dumps({
                                'itemId': unit_id
                            }),
                            'sid': sid
                        }
                        
                        response = requests.get(url, params=params, timeout=30)
                        if response.status_code == 200:
                            data = response.json()
                            print(f"    Response: {json.dumps(data, indent=2)}")
                            
                            if isinstance(data, dict) and 'pos' in data:
                                pos = data['pos']
                                print(f"    ✅ Позиция найдена: {pos.get('y')}, {pos.get('x')}")
                                print(f"    🚗 Скорость: {pos.get('s', 0) * 3.6:.1f} км/ч")
                                print(f"    🕐 Время: {pos.get('t', 'N/A')}")
                                continue
                    except Exception as e:
                        print(f"    ❌ Ошибка: {e}")
                    
                    print(f"  ⚠️ Все способы не дали позицию")
                
                return True
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_different_flags(sid):
    """Проверяем разные флаги для получения данных"""
    print(f"\n🔍 Проверяем разные флаги...")
    
    devices = [
        {'name': '484 ATL 01', 'id': '29603155'},
        {'name': '355 ATL 01', 'id': '29682916'},
        {'name': '359 AUL 01', 'id': '29682864'},
        {'name': '695 BHS 02', 'id': '29682886'},
    ]
    
    for device in devices:
        print(f"\n🚛 Проверяем {device['name']} (ID: {device['id']})")
        
        # Тестируем разные флаги
        flags_to_test = [
            {'name': 'Базовые данные', 'value': 0x1},
            {'name': 'Параметры', 'value': 0x2},
            {'name': 'Позиция', 'value': 0x4},
            {'name': 'Датчики', 'value': 0x8},
            {'name': 'Состояние', 'value': 0x10},
            {'name': 'Все основные', 'value': 0x1F},
            {'name': 'Расширенные', 'value': 0x3F},
            {'name': 'Максимальные', 'value': 0x7F},
        ]
        
        for flag_test in flags_to_test:
            try:
                url = f"{base_url}/wialon/ajax.html"
                params = {
                    'svc': 'core/search_item',
                    'params': json.dumps({
                        'id': device['id'],
                        'flags': flag_test['value']
                    }),
                    'sid': sid
                }
                
                response = requests.get(url, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    
                    if isinstance(data, dict) and 'item' in data:
                        item = data['item']
                        if 'pos' in item:
                            pos = item['pos']
                            print(f"  ✅ {flag_test['name']} (0x{flag_test['value']:02X}): {pos.get('y')}, {pos.get('x')}")
                            break
                        else:
                            print(f"  ⚠️ {flag_test['name']} (0x{flag_test['value']:02X}): позиция не найдена")
            except Exception as e:
                print(f"  ❌ {flag_test['name']}: ошибка {e}")

if __name__ == "__main__":
    print("🛰️ Проверка активных GPS устройств")
    print("=" * 50)
    
    sid = test_auth()
    if sid:
        print(f"✅ Авторизация успешна! SID: {sid}")
        
        # Проверяем данные мониторинга
        test_monitoring_data(sid)
        
        # Проверяем разные флаги
        test_different_flags(sid)
    else:
        print("❌ Ошибка авторизации")
