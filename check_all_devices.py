#!/usr/bin/env python3
import requests
import json

# Проверяем статус всех GPS устройств
base_url = "https://hst-api.wialon.com"
access_token = "84582de9332f6d15227795a639a37d94DD3C6E56E170623AAC680089A097C9D1CBD30C52"

# Все GPS устройства
devices = [
    {'name': '484 ATL 01', 'id': '29603155', 'vehicle': '484ATL01'},
    {'name': '355 ATL 01', 'id': '29682916', 'vehicle': '290ATL01'},
    {'name': '359 AUL 01', 'id': '29682864', 'vehicle': '533ATL01'},
    {'name': '695 BHS 02', 'id': '29682886', 'vehicle': '105AGR19'},
]

def check_device_status(sid, device):
    """Проверяем статус конкретного устройства"""
    print(f"\n🚛 Проверяем {device['name']} (ID: {device['id']}) - {device['vehicle']}")
    
    try:
        # Пробуем получить позицию
        url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/get_position',
            'params': json.dumps({'itemId': device['id']}),
            'sid': sid
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                if data['error'] == 2:
                    print(f"  ❌ Устройство неактивно (error: 2)")
                else:
                    print(f"  ⚠️ Ошибка: {data['error']}")
            else:
                print(f"  ✅ Устройство активно, данные получены")
                if 'pos' in data:
                    pos = data['pos']
                    print(f"    📍 Позиция: {pos.get('y')}, {pos.get('x')}")
                    print(f"    🚗 Скорость: {pos.get('s', 0) * 3.6:.1f} км/ч")
        else:
            print(f"  ❌ HTTP ошибка: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Ошибка проверки: {e}")

def check_device_messages(sid, device):
    """Проверяем последние сообщения устройства"""
    try:
        url = f"{base_url}/wialon/ajax.html"
        params = {
            'svc': 'core/get_messages',
            'params': json.dumps({
                'itemId': device['id'],
                'timeFrom': 1759000000,  # Недавнее время
                'timeTo': 1759067329,    # Текущее время
                'flags': 0x1
            }),
            'sid': sid
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                if data['error'] == 2:
                    print(f"  📨 Нет сообщений (устройство неактивно)")
                else:
                    print(f"  📨 Ошибка получения сообщений: {data['error']}")
            else:
                messages = data.get('messages', [])
                if messages:
                    print(f"  📨 Получено {len(messages)} сообщений")
                    # Показываем последнее сообщение
                    last_msg = messages[-1]
                    if 'pos' in last_msg:
                        pos = last_msg['pos']
                        print(f"    📍 Последняя позиция: {pos.get('y')}, {pos.get('x')}")
                        print(f"    🕐 Время: {last_msg.get('t', 'N/A')}")
                else:
                    print(f"  📨 Нет сообщений за указанный период")
        else:
            print(f"  ❌ HTTP ошибка получения сообщений: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Ошибка получения сообщений: {e}")

if __name__ == "__main__":
    print("🛰️ Проверка статуса всех GPS устройств")
    print("=" * 50)
    
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
                
                # Проверяем каждое устройство
                active_count = 0
                for device in devices:
                    check_device_status(sid, device)
                    check_device_messages(sid, device)
                    
                    # Проверяем, есть ли данные о позиции
                    try:
                        url = f"{base_url}/wialon/ajax.html"
                        params = {
                            'svc': 'core/get_position',
                            'params': json.dumps({'itemId': device['id']}),
                            'sid': sid
                        }
                        
                        response = requests.get(url, params=params, timeout=30)
                        if response.status_code == 200:
                            data = response.json()
                            if 'error' not in data:
                                active_count += 1
                    except:
                        pass
                
                print(f"\n📊 Итого: {active_count} из {len(devices)} устройств активны")
                
                if active_count == 0:
                    print("\n⚠️ Все GPS устройства неактивны!")
                    print("💡 Рекомендации:")
                    print("   1. Проверьте статус устройств в системе StavTrack")
                    print("   2. Убедитесь, что устройства включены и имеют связь")
                    print("   3. Проверьте SIM-карты и баланс")
                    print("   4. Обратитесь к поставщику GPS трекеров")
                else:
                    print(f"\n✅ {active_count} устройств передают данные")
                    
            else:
                print(f"❌ Ошибка авторизации")
        else:
            print(f"❌ HTTP ошибка авторизации: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка авторизации: {e}")
