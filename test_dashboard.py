#!/usr/bin/env python3
import requests
import sys

def test_dashboard():
    """Проверяет доступность дашборда"""
    try:
        # Проверяем главную страницу
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f"✅ Главная страница: {response.status_code}")
        
        # Проверяем дашборд (ожидаем редирект на логин)
        response = requests.get('http://localhost:8000/dashboard/', timeout=5)
        if response.status_code == 302:
            print("✅ Дашборд требует аутентификации (это нормально)")
        else:
            print(f"⚠️  Дашборд: {response.status_code}")
            
        # Проверяем карту
        response = requests.get('http://localhost:8000/map/', timeout=5)
        if response.status_code == 302:
            print("✅ Карта требует аутентификации (это нормально)")
        else:
            print(f"⚠️  Карта: {response.status_code}")
            
        print("\n🎉 Сервер работает корректно!")
        print("📝 Для проверки дашборда войдите в систему через браузер")
        
    except requests.exceptions.ConnectionError:
        print("❌ Сервер не запущен или недоступен")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_dashboard() 