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
        
        # Пробуем разные endpoints для получения уведомлений
        endpoints = [
            "https://barlau.org/api/notifications/",
            "https://barlau.org/api/v1/notifications/",
            "https://barlau.org/api/public-notifications/"
        ]
        
        notifications = []
        working_endpoint = None
        
        for endpoint in endpoints:
            print(f"🔍 Проверяем endpoint: {endpoint}")
            try:
                get_response = requests.get(endpoint, headers=headers, timeout=10)
                if get_response.status_code == 200:
                    data = get_response.json()
                    if isinstance(data, list):
                        notifications = data
                    elif isinstance(data, dict) and 'results' in data:
                        notifications = data['results']
                    else:
                        notifications = []
                    
                    working_endpoint = endpoint
                    print(f"✅ Найдено уведомлений: {len(notifications)}")
                    break
                else:
                    print(f"❌ Статус {get_response.status_code}")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
        
        if not working_endpoint:
            print("❌ Не удалось найти рабочий endpoint для уведомлений")
            return False
        
        if not notifications:
            print("🎉 Уведомлений не найдено - база уже чистая!")
            return True
        
        # Удаляем каждое уведомление
        deleted_count = 0
        for notification in notifications:
            notification_id = notification.get('id')
            if notification_id:
                # Пробуем разные endpoints для удаления
                delete_endpoints = [
                    f"https://barlau.org/api/notifications/{notification_id}/",
                    f"https://barlau.org/api/v1/notifications/{notification_id}/"
                ]
                
                deleted = False
                for delete_endpoint in delete_endpoints:
                    try:
                        delete_response = requests.delete(delete_endpoint, headers=headers, timeout=10)
                        if delete_response.status_code in [200, 204]:
                            deleted_count += 1
                            print(f"✅ Удалено уведомление ID: {notification_id}")
                            deleted = True
                            break
                    except Exception as e:
                        continue
                
                if not deleted:
                    print(f"❌ Не удалось удалить уведомление {notification_id}")
        
        print(f"🎉 Успешно удалено {deleted_count} уведомлений!")
        
        # Проверяем, что все уведомления удалены
        print("🔍 Проверяем результат...")
        final_response = requests.get(working_endpoint, headers=headers, timeout=10)
        if final_response.status_code == 200:
            final_data = final_response.json()
            if isinstance(final_data, list):
                remaining_count = len(final_data)
            elif isinstance(final_data, dict) and 'results' in final_data:
                remaining_count = len(final_data['results'])
            else:
                remaining_count = 0
            
            if remaining_count == 0:
                print("✅ Все уведомления успешно удалены!")
            else:
                print(f"⚠️ Осталось уведомлений: {remaining_count}")
        
        return True
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    clear_all_notifications()
