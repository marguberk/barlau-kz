#!/usr/bin/env python3
import requests
import json
import time

# Проверяем последние данные устройств
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

def test_recent_messages(sid):
    """Проверяем последние сообщения устройств"""
    print("📨 Проверяем последние сообщения устройств...")
    
    devices = [
        {'name': '484 ATL 01', 'id': '29603155'},
        {'name': '355 ATL 01', 'id': '29682916'},
        {'name': '359 AUL 01', 'id': '29682864'},
        {'name': '695 BHS 02', 'id': '29682886'},
    ]
    
    # Текущее время в Unix timestamp
    current_time = int(time.time())
    print(f"Текущее время: {current_time} ({time.ctime(current_time)})")
    
    # Проверяем разные временные окна
    time_windows = [
        {'name': 'Последний час', 'from': current_time - 3600},
        {'name': 'Последние 6 часов', 'from': current_time - 21600},
        {'name': 'Последний день', 'from': current_time - 86400},
        {'name': 'Последняя неделя', 'from': current_time - 604800},
        {'name': 'Последний месяц', 'from': current_time - 2592000},
    ]
    
    for device in devices:
        print(f"\n🚛 Проверяем {device['name']} (ID: {device['id']})")
        
        for time_window in time_windows:
            print(f"  ⏰ {time_window['name']} (с {time_window['from']})")
            
            try:
                url = f"{base_url}/wialon/ajax.html"
                params = {
                    'svc': 'core/get_messages',
                    'params': json.dumps({
                        'itemId': device['id'],
                        'timeFrom': time_window['from'],
                        'timeTo': current_time,
                        'flags': 0x1
                    }),
                    'sid': sid
                }
                
                response = requests.get(url, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    
                    if isinstance(data, dict) and 'messages' in data:
                        messages = data['messages']
                        if messages:
                            print(f"    ✅ Найдено {len(messages)} сообщений")
                            
                            # Показываем последнее сообщение
                            last_msg = messages[-1]
                            print(f"    📍 Последнее сообщение:")
                            print(f"      Время: {last_msg.get('t', 'N/A')} ({time.ctime(last_msg.get('t', 0))})")
                            
                            if 'pos' in last_msg:
                                pos = last_msg['pos']
                                print(f"      Позиция: {pos.get('y')}, {pos.get('x')}")
                                print(f"      Скорость: {pos.get('s', 0) * 3.6:.1f} км/ч")
                                print(f"      Направление: {pos.get('c', 'N/A')}°")
                                print(f"      Высота: {pos.get('z', 'N/A')} м")
                                print(f"      Спутники: {pos.get('sc', 'N/A')}")
                                break  # Нашли данные, выходим
                            else:
                                print(f"      ⚠️ Позиция не найдена в сообщении")
                        else:
                            print(f"    ⚠️ Нет сообщений")
                    elif isinstance(data, dict) and 'error' in data:
                        print(f"    ❌ Ошибка API: {data['error']}")
                    else:
                        print(f"    ❌ Неожиданная структура ответа")
                else:
                    print(f"    ❌ HTTP ошибка: {response.status_code}")
                    
            except Exception as e:
                print(f"    ❌ Ошибка: {e}")

def test_monitoring_data_recent(sid):
    """Проверяем данные мониторинга за последнее время"""
    print(f"\n📊 Проверяем данные мониторинга за последнее время...")
    
    devices = [
        {'name': '484 ATL 01', 'id': '29603155'},
        {'name': '355 ATL 01', 'id': '29682916'},
        {'name': '359 AUL 01', 'id': '29682864'},
        {'name': '695 BHS 02', 'id': '29682886'},
    ]
    
    current_time = int(time.time())
    
    for device in devices:
        print(f"\n🚛 Проверяем {device['name']} (ID: {device['id']})")
        
        try:
            url = f"{base_url}/wialon/ajax.html"
            params = {
                'svc': 'core/get_monitoring_data',
                'params': json.dumps({
                    'spec': [device['id']],
                    'timeFrom': current_time - 86400,  # Последний день
                    'timeTo': current_time,
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
                    if items:
                        item = items[0]
                        print(f"    ✅ Найдены данные мониторинга")
                        
                        if 'pos' in item:
                            pos = item['pos']
                            print(f"      Позиция: {pos.get('y')}, {pos.get('x')}")
                            print(f"      Скорость: {pos.get('s', 0) * 3.6:.1f} км/ч")
                        else:
                            print(f"      ⚠️ Позиция не найдена")
                    else:
                        print(f"    ⚠️ Нет данных мониторинга")
                elif isinstance(data, dict) and 'error' in data:
                    print(f"    ❌ Ошибка API: {data['error']}")
                else:
                    print(f"    ❌ Неожиданная структура ответа")
            else:
                print(f"    ❌ HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"    ❌ Ошибка: {e}")

def test_unit_status(sid):
    """Проверяем статус устройств"""
    print(f"\n🔍 Проверяем статус устройств...")
    
    devices = [
        {'name': '484 ATL 01', 'id': '29603155'},
        {'name': '355 ATL 01', 'id': '29682916'},
        {'name': '359 AUL 01', 'id': '29682864'},
        {'name': '695 BHS 02', 'id': '29682886'},
    ]
    
    for device in devices:
        print(f"\n🚛 Проверяем {device['name']} (ID: {device['id']})")
        
        try:
            url = f"{base_url}/wialon/ajax.html"
            params = {
                'svc': 'core/search_item',
                'params': json.dumps({
                    'id': device['id'],
                    'flags': 0x1F  # Все основные флаги
                }),
                'sid': sid
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, dict) and 'item' in data:
                    item = data['item']
                    print(f"    ✅ Данные устройства получены")
                    print(f"      Название: {item.get('nm', 'N/A')}")
                    print(f"      ID: {item.get('id', 'N/A')}")
                    print(f"      Класс: {item.get('cls', 'N/A')}")
                    print(f"      Создано: {item.get('ct', 'N/A')} ({time.ctime(item.get('ct', 0))})")
                    print(f"      Последняя активность: {item.get('bact', 'N/A')} ({time.ctime(item.get('bact', 0))})")
                    
                    if 'prp' in item:
                        prp = item['prp']
                        print(f"      Свойства:")
                        for key, value in prp.items():
                            print(f"        {key}: {value}")
                else:
                    print(f"    ❌ Неожиданная структура ответа")
            else:
                print(f"    ❌ HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"    ❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🛰️ Проверка последних данных GPS устройств")
    print("=" * 60)
    
    sid = test_auth()
    if sid:
        print(f"✅ Авторизация успешна! SID: {sid}")
        
        # Проверяем последние сообщения
        test_recent_messages(sid)
        
        # Проверяем данные мониторинга
        test_monitoring_data_recent(sid)
        
        # Проверяем статус устройств
        test_unit_status(sid)
    else:
        print("❌ Ошибка авторизации")
