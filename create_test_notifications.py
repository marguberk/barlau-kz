#!/usr/bin/env python3

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from accounts.models import User
from core.models import Notification

def create_test_notifications():
    """Создает тестовые уведомления для всех пользователей"""
    
    # Получаем всех активных пользователей
    users = User.objects.filter(is_active=True)
    print(f"Найдено пользователей: {users.count()}")
    
    for user in users:
        print(f"Создаю уведомления для {user.username} ({user.role})")
        
        # Создаем несколько разных типов уведомлений
        notifications_data = [
            {
                'type': Notification.Type.SYSTEM,
                'title': 'Добро пожаловать в BARLAU.KZ',
                'message': f'Привет, {user.first_name}! Система уведомлений работает корректно.'
            },
            {
                'type': Notification.Type.TASK,
                'title': 'Новая задача назначена',
                'message': 'Вам назначена новая задача "Проверка технического состояния автомобиля"'
            },
            {
                'type': Notification.Type.DOCUMENT,
                'title': 'Документ требует внимания',
                'message': 'У автомобиля Mercedes Actros (533 ATL 01) истекает техосмотр через 15 дней'
            }
        ]
        
        for notif_data in notifications_data:
            notification = Notification.objects.create(
                user=user,
                type=notif_data['type'],
                title=notif_data['title'],
                message=notif_data['message'],
                read=False
            )
            print(f"  ✓ Создано: {notification.title}")
    
    total_notifications = Notification.objects.count()
    print(f"\nВсего уведомлений в системе: {total_notifications}")
    
    # Показываем последние 5
    print("\nПоследние 5 уведомлений:")
    recent = Notification.objects.order_by('-created_at')[:5]
    for n in recent:
        print(f"  {n.created_at.strftime('%d.%m.%Y %H:%M')} | {n.user.username} | {n.title}")

if __name__ == '__main__':
    create_test_notifications() 