#!/usr/bin/env python3
"""
Тестирование GPS тестовой страницы
"""

import requests
import time
import webbrowser

def test_gps_test_page():
    """Тестирование GPS тестовой страницы"""
    
    print("🛰️ Тестирование GPS тестовой страницы")
    print("=" * 60)
    
    # URL тестовой страницы
    test_page_url = "https://barlau.org/gps-test/"
    api_url = "https://barlau.org/api/vehicles/9/"
    
    print(f"📱 Тестовая страница: {test_page_url}")
    print(f"🔌 API endpoint: {api_url}")
    print()
    
    # Тестируем API endpoint
    print("🔍 Тестирование API endpoint...")
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API endpoint работает!")
            print(f"📊 Данные получены:")
            print(f"   🚛 Грузовик: {data.get('license_plate')}")
            print(f"   📍 Координаты: {data.get('gps_latitude')}, {data.get('gps_longitude')}")
            print(f"   🛰️ GPS enabled: {data.get('gps_enabled')}")
            print(f"   📱 Device ID: {data.get('gps_device_id')}")
            print(f"   🚗 Скорость: {data.get('gps_speed')}")
            print(f"   ⛽ Топливо: {data.get('gps_fuel_level')}")
            print(f"   ⏰ Последнее обновление: {data.get('gps_last_update')}")
            
            # Проверяем, есть ли координаты
            if data.get('gps_latitude') and data.get('gps_longitude'):
                print(f"✅ GPS координаты доступны для отображения на карте")
                return True
            else:
                print(f"⚠️ GPS координаты отсутствуют")
                return False
                
        else:
            print(f"❌ API endpoint не работает: {response.status_code}")
            print(f"📝 Ответ: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")
        return False

def open_gps_test_page():
    """Открытие GPS тестовой страницы в браузере"""
    
    print("\n🌐 Открытие GPS тестовой страницы в браузере...")
    
    test_page_url = "https://barlau.org/gps-test/"
    
    try:
        webbrowser.open(test_page_url)
        print(f"✅ Тестовая страница открыта: {test_page_url}")
        print(f"💡 Нажмите 'Запустить мониторинг' для начала отслеживания GPS координат")
        return True
    except Exception as e:
        print(f"❌ Ошибка открытия страницы: {e}")
        return False

def monitor_gps_updates():
    """Мониторинг обновлений GPS данных"""
    
    print("\n🔄 Мониторинг обновлений GPS данных...")
    print("=" * 50)
    
    api_url = "https://barlau.org/api/vehicles/9/"
    previous_coordinates = None
    update_count = 0
    
    try:
        while True:
            try:
                response = requests.get(api_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    current_coordinates = (data.get('gps_latitude'), data.get('gps_longitude'))
                    last_update = data.get('gps_last_update')
                    
                    print(f"🔄 Проверка {update_count + 1}: {time.strftime('%H:%M:%S')}")
                    print(f"   📍 Координаты: {current_coordinates}")
                    print(f"   🕐 Последнее обновление: {last_update}")
                    
                    # Проверяем, изменились ли координаты
                    if previous_coordinates and current_coordinates != previous_coordinates:
                        print(f"   ✅ Координаты обновлены!")
                        print(f"   📊 Было: {previous_coordinates}")
                        print(f"   📊 Стало: {current_coordinates}")
                    elif previous_coordinates and current_coordinates == previous_coordinates:
                        print(f"   ⚠️ Координаты не изменились")
                    else:
                        print(f"   📝 Начальные координаты")
                    
                    previous_coordinates = current_coordinates
                    update_count += 1
                    
                else:
                    print(f"❌ Ошибка получения данных: {response.status_code}")
                
                print()
                
                # Ждем 5 секунд до следующей проверки
                time.sleep(5)
                
            except KeyboardInterrupt:
                print(f"\n🛑 Мониторинг остановлен пользователем")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                time.sleep(5)
                
    except KeyboardInterrupt:
        print(f"\n🛑 Мониторинг остановлен")
    
    print(f"\n📊 Статистика мониторинга:")
    print(f"   Всего проверок: {update_count}")
    print(f"   Время работы: {update_count * 5} секунд")

def main():
    print("🛰️ Тестирование GPS тестовой страницы")
    print("=" * 80)
    
    # Тестируем API endpoint
    api_working = test_gps_test_page()
    
    if api_working:
        # Открываем тестовую страницу
        page_opened = open_gps_test_page()
        
        if page_opened:
            print(f"\n🎉 GPS тестовая страница готова к работе!")
            print(f"✅ API endpoint работает")
            print(f"✅ Тестовая страница открыта")
            print(f"✅ GPS координаты доступны")
            
            # Спрашиваем, хочет ли пользователь запустить мониторинг
            print(f"\n❓ Хотите запустить мониторинг обновлений GPS данных?")
            print(f"   (Нажмите Enter для запуска, Ctrl+C для остановки)")
            
            try:
                input()
                monitor_gps_updates()
            except KeyboardInterrupt:
                print(f"\n👋 Мониторинг отменен")
        else:
            print(f"\n⚠️ Не удалось открыть тестовую страницу")
    else:
        print(f"\n❌ GPS тестовая страница не готова к работе")
        print(f"📝 Проверьте настройки API endpoint")

if __name__ == "__main__":
    main()








































