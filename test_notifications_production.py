#!/usr/bin/env python
"""
Скрипт для тестирования уведомлений на продакшн сервере
Нужно запустить на сервере: python manage.py shell < test_notifications_production.py
"""

print("🔍 Тестируем систему уведомлений на продакшн сервере...")

# Импорты
from accounts.models import User
from core.models import Notification
from django.conf import settings

print(f"DEBUG режим: {settings.DEBUG}")

# Проверяем пользователей
admin_users = User.objects.filter(role__in=['SUPERADMIN', 'DIRECTOR']).filter(is_active=True)
print(f"Найдено администраторов: {admin_users.count()}")
for admin in admin_users:
    print(f"  - {admin.username} ({admin.email}) - {admin.role}")

# Проверяем существующие уведомления
total_notifications = Notification.objects.count()
print(f"Всего уведомлений в базе: {total_notifications}")

if admin_users.exists():
    admin = admin_users.first()
    user_notifications = Notification.objects.filter(user=admin).count()
    print(f"Уведомлений у пользователя {admin.username}: {user_notifications}")
    
    # Создаем тестовое уведомление
    test_notification = Notification.create_system_notification(
        admin,
        "Тест продакшн уведомлений",
        "Это тестовое уведомление для проверки работы системы на продакшн сервере"
    )
    print(f"✅ Создано тестовое уведомление ID: {test_notification.id}")
    
    # Проверяем API endpoint
    from django.urls import reverse
    try:
        api_url = reverse('logistics:notification-list')
        print(f"API URL: {api_url}")
    except:
        print("❌ Не удалось получить API URL")

print("�� Тест завершен!") 