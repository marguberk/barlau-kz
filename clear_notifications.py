#!/usr/bin/env python3
import requests
import json

def clear_all_notifications():
    """Удалить все уведомления из базы данных"""
    
    # Данные для авторизации
    auth_data = {
        "username": "+77761605888",  # Админ
        "password": "barlau2025"
    }
    
    print("🧹 Очистка уведомлений BARLAU")
    print("=" * 50)
    
    try:
        # Получаем токен
        print("🔐 Получаем токен администратора...")
        auth_response = requests.post(
            "https://barlau.org/api/v1/auth/token/",
            json=auth_data,
            timeout=10
        )
        
        if auth_response.status_code != 200:
            print(f"❌ Ошибка авторизации: {auth_response.status_code}")
            print(f"Ответ: {auth_response.text}")
            return False
        
        auth_result = auth_response.json()
        access_token = auth_result.get('access')
        
        if not access_token:
            print("❌ Токен не получен")
            return False
        
        print("✅ Токен получен успешно!")
        
        # Удаляем все уведомления
        print("🗑️ Удаляем все уведомления...")
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Сначала получаем все уведомления
        get_response = requests.get(
            "https://barlau.org/api/v1/notifications/",
            headers=headers,
            timeout=10
        )
        
        if get_response.status_code == 200:
            notifications = get_response.json()
            print(f"📊 Найдено уведомлений: {len(notifications)}")
            
            # Удаляем каждое уведомление
            deleted_count = 0
            for notification in notifications:
                notification_id = notification.get('id')
                if notification_id:
                    delete_response = requests.delete(
                        f"https://barlau.org/api/v1/notifications/{notification_id}/",
                        headers=headers,
                        timeout=10
                    )
                    
                    if delete_response.status_code in [200, 204]:
                        deleted_count += 1
                        print(f"✅ Удалено уведомление ID: {notification_id}")
                    else:
                        print(f"❌ Ошибка удаления уведомления {notification_id}: {delete_response.status_code}")
            
            print(f"🎉 Успешно удалено {deleted_count} уведомлений!")
            return True
        else:
            print(f"❌ Ошибка получения уведомлений: {get_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    clear_all_notifications()
