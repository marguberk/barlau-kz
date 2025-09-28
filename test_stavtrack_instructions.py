#!/usr/bin/env python3
import requests
import json

# Тестируем согласно инструкции от StavTrack
base_url = "https://hst-api.wialon.com"
access_token = "84582de9332f6d15227795a639a37d94DD3C6E56E170623AAC680089A097C9D1CBD30C52"

def test_stavtrack_auth():
    """Тестируем авторизацию согласно инструкции StavTrack"""
    print("🔐 Тестируем авторизацию согласно инструкции StavTrack...")
    
    try:
        # Используем точный формат из инструкции
        auth_url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'token/login',
            'params': json.dumps({'token': access_token}),
            'sid': ''
        }
        
        print(f"URL: {auth_url}")
        print(f"Params: {params}")
        
        response = requests.get(auth_url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'eid' in data:
                sid = data['eid']
                print(f"✅ Авторизация успешна! SID: {sid}")
                
                # Проверяем пользователя
                if 'user' in data:
                    user = data['user']
                    print(f"👤 Пользователь: {user.get('nm', 'N/A')} (ID: {user.get('id', 'N/A')})")
                    
                    # Проверяем права доступа
                    if 'uacl' in user:
                        uacl = user['uacl']
                        print(f"🔑 Права доступа: {uacl}")
                        
                        # Проверяем права на мониторинг
                        if uacl & 0x1:  # Бит 0 - мониторинг
                            print("  ✅ Право на мониторинг")
                        else:
                            print("  ❌ Нет права на мониторинг")
                            
                        if uacl & 0x2:  # Бит 1 - отчеты
                            print("  ✅ Право на отчеты")
                        else:
                            print("  ❌ Нет права на отчеты")
                
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

def test_get_units_with_proper_flags(sid):
    """Тестируем получение устройств с правильными флагами"""
    print(f"\n📡 Получаем список устройств с правильными флагами...")
    
    try:
        # Используем флаги согласно документации Wialon
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
                'flags': 0x1  # Базовые флаги
            }),
            'sid': sid
        }
        
        response = requests.get(units_url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if isinstance(data, dict) and 'items' in data:
                units = data['items']
                print(f"✅ Получено {len(units)} устройств:")
                
                for i, unit in enumerate(units):
                    print(f"  {i+1}. {unit.get('nm', 'N/A')} (ID: {unit.get('id', 'N/A')})")
                    
                return units
            else:
                print(f"❌ Неожиданная структура ответа")
                return None
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка получения устройств: {e}")
        return None

def test_get_unit_data_with_flags(sid, unit_id):
    """Тестируем получение данных устройства с разными флагами"""
    print(f"\n📍 Тестируем получение данных устройства {unit_id}...")
    
    # Флаги согласно документации Wialon
    flags_to_test = [
        {'name': 'Базовые данные', 'value': 0x1},
        {'name': 'Параметры', 'value': 0x2},
        {'name': 'Позиция', 'value': 0x4},
        {'name': 'Датчики', 'value': 0x8},
        {'name': 'Состояние', 'value': 0x10},
        {'name': 'Все основные', 'value': 0x1F},
        {'name': 'Расширенные', 'value': 0x3F},
    ]
    
    for flag_test in flags_to_test:
        print(f"\n  🔍 Тестируем {flag_test['name']} (флаг: 0x{flag_test['value']:02X})")
        
        try:
            url = f"{base_url}/wialon/ajax.html"
            params = {
                'svc': 'core/search_item',
                'params': json.dumps({
                    'id': unit_id,
                    'flags': flag_test['value']
                }),
                'sid': sid
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, dict) and 'item' in data:
                    item = data['item']
                    
                    # Ищем позицию
                    if 'pos' in item:
                        pos = item['pos']
                        print(f"    ✅ Позиция найдена: {pos.get('y')}, {pos.get('x')}")
                        print(f"    🚗 Скорость: {pos.get('s', 0) * 3.6:.1f} км/ч")
                        print(f"    🕐 Время: {pos.get('t', 'N/A')}")
                        return True  # Найдена позиция
                    else:
                        print(f"    ⚠️ Позиция не найдена")
                        
                        # Проверяем другие поля
                        if 'nm' in item:
                            print(f"    📝 Название: {item['nm']}")
                        if 'prp' in item:
                            print(f"    ⚙️ Параметры: {len(item['prp'])} шт.")
                        if 'ct' in item:
                            print(f"    🕐 Создано: {item['ct']}")
                else:
                    print(f"    ❌ Неожиданная структура ответа")
            else:
                print(f"    ❌ HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"    ❌ Ошибка: {e}")
    
    return False

if __name__ == "__main__":
    print("🛰️ Тестирование согласно инструкции StavTrack")
    print("=" * 60)
    
    # Тестируем авторизацию
    sid = test_stavtrack_auth()
    
    if sid:
        # Получаем список устройств
        units = test_get_units_with_proper_flags(sid)
        
        if units:
            # Тестируем первое устройство
            if len(units) > 0:
                first_unit = units[0]
                unit_id = first_unit.get('id')
                unit_name = first_unit.get('nm')
                
                print(f"\n🎯 Тестируем устройство {unit_name} (ID: {unit_id})")
                has_position = test_get_unit_data_with_flags(sid, unit_id)
                
                if has_position:
                    print(f"\n✅ Устройство {unit_name} передает данные о позиции!")
                else:
                    print(f"\n⚠️ Устройство {unit_name} не передает данные о позиции")
                    
                print(f"\n💡 Рекомендации:")
                print(f"   1. Проверьте статус устройства в системе StavTrack")
                print(f"   2. Убедитесь, что устройство включено и имеет GPS сигнал")
                print(f"   3. Проверьте SIM-карту и баланс")
        else:
            print(f"\n❌ Не удалось получить список устройств")
    else:
        print(f"\n❌ Не удалось авторизоваться")
