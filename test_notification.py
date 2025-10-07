#!/usr/bin/env python3
"""
Скрипт для тестирования отправки уведомлений через API
"""
import requests
import json
import sys

# Конфигурация
API_BASE_URL = "https://barlau.org"
ADMIN_TOKEN = "your_admin_token_here"  # Нужно заменить на реальный токен

def send_test_notification():
    """Отправка тестового уведомления"""
    
    url = f"{API_BASE_URL}/api/notifications/broadcast/"
    
    headers = {
        'Authorization': f'Bearer {ADMIN_TOKEN}',
        'Content-Type': 'application/json',
    }
    
    # Тестовое уведомление для всех водителей
    data = {
        "title": "🔔 ТЕСТ УВЕДОМЛЕНИЯ ДЛЯ ВОДИТЕЛЕЙ",
        "message": "Это тестовое уведомление для проверки звука и вибрации! 🔊 Если вы слышите это - звук работает!",
        "recipients": "drivers",  # Отправляем всем водителям
        "type": "SYSTEM",
        "priority": "HIGH",
        "link": "https://barlau.org"
    }
    
    try:
        print("📤 Отправляем тестовое уведомление...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"📊 Статус ответа: {response.status_code}")
        print(f"📊 Ответ сервера: {response.text}")
        
        if response.status_code == 201:
            print("✅ Уведомление успешно отправлено!")
            result = response.json()
            print(f"📋 ID уведомления: {result.get('id')}")
            return True
        else:
            print(f"❌ Ошибка отправки: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def get_admin_token():
    """Получение токена администратора"""
    login_url = f"{API_BASE_URL}/api/v1/auth/token/"
    
    # Замените на реальные данные администратора
    login_data = {
        "username": "admin",  # или номер телефона администратора
        "password": "barlau2025"
    }
    
    try:
        print("🔐 Получаем токен администратора...")
        response = requests.post(login_url, json=login_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"📊 Ответ сервера: {json.dumps(result, indent=2, ensure_ascii=False)}")
            token = result.get('access_token') or result.get('token') or result.get('access')
            if token:
                print("✅ Токен получен успешно!")
                return token
            else:
                print("❌ Токен не найден в ответе")
                print(f"Доступные поля: {list(result.keys())}")
                return None
        else:
            print(f"❌ Ошибка авторизации: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка получения токена: {e}")
        return None

if __name__ == "__main__":
    print("🧪 Тестирование уведомлений BARLAU")
    print("=" * 50)
    
    # Получаем токен
    token = get_admin_token()
    if not token:
        print("❌ Не удалось получить токен. Проверьте данные для входа.")
        sys.exit(1)
    
    # Обновляем токен в скрипте
    ADMIN_TOKEN = token
    
    # Отправляем тестовое уведомление
    success = send_test_notification()
    
    if success:
        print("\n🎉 Тест завершен успешно!")
        print("📱 Проверьте приложение - должно прийти уведомление с звуком")
    else:
        print("\n❌ Тест не прошел")
        sys.exit(1)
