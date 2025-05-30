#!/usr/bin/env python
"""
Скрипт для удаления тестовых пользователей test123 и webadmin
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings_production')
django.setup()

from accounts.models import User

def remove_test_users():
    """Удаляет тестовых пользователей test123 и webadmin"""
    
    test_usernames = ['test123', 'webadmin']
    removed_count = 0
    
    print("Удаление тестовых пользователей:")
    print("=" * 50)
    
    for username in test_usernames:
        try:
            user = User.objects.get(username=username)
            user_info = f"{user.username} ({user.get_full_name() or 'без имени'}) - {user.role}"
            
            # Проверяем, есть ли связанные данные
            related_info = []
            
            # Проверяем связанные объекты (если есть)
            try:
                # Проверяем грузовики, созданные этим пользователем
                from logistics.models import Vehicle
                vehicles_created = Vehicle.objects.filter(created_by=user).count()
                if vehicles_created > 0:
                    related_info.append(f"создал {vehicles_created} грузовиков")
                
                # Проверяем задачи
                from logistics.models import Task
                tasks_created = Task.objects.filter(created_by=user).count()
                if tasks_created > 0:
                    related_info.append(f"создал {tasks_created} задач")
                    
                # Проверяем документы грузовиков
                from logistics.models import VehicleDocument
                docs_created = VehicleDocument.objects.filter(created_by=user).count()
                if docs_created > 0:
                    related_info.append(f"создал {docs_created} документов")
                    
            except Exception as check_error:
                related_info.append(f"ошибка проверки связей: {check_error}")
            
            # Удаляем пользователя
            user.delete()
            
            status_msg = f"✓ {user_info} - удален"
            if related_info:
                status_msg += f" (был связан: {', '.join(related_info)})"
            
            print(status_msg)
            removed_count += 1
            
        except User.DoesNotExist:
            print(f"- {username} - не найден")
        except Exception as e:
            print(f"✗ {username} - ошибка при удалении: {e}")
    
    print("=" * 50)
    print(f"Всего удалено пользователей: {removed_count}")
    
    # Показываем оставшихся пользователей
    remaining_users = User.objects.all().order_by('username')
    print(f"\nОставшиеся пользователи ({remaining_users.count()}):")
    for user in remaining_users:
        role_display = user.get_role_display() if hasattr(user, 'get_role_display') else user.role
        name_display = user.get_full_name() or 'без имени'
        is_super = ' (суперпользователь)' if user.is_superuser else ''
        print(f"  {user.username} - {name_display} ({role_display}){is_super}")

if __name__ == '__main__':
    print("Запуск удаления тестовых пользователей...")
    remove_test_users()
    print("Готово!") 