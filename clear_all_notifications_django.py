#!/usr/bin/env python3
"""
Скрипт для полной очистки всех уведомлений у всех пользователей через Django shell
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from core.models import Notification

def clear_all_notifications():
    """Удалить ВСЕ уведомления из базы данных"""
    
    print("🧹 ПОЛНАЯ ОЧИСТКА УВЕДОМЛЕНИЙ BARLAU")
    print("=" * 50)
    
    try:
        # Получаем общее количество уведомлений
        total_count = Notification.objects.count()
        print(f"📊 Всего уведомлений в базе: {total_count}")
        
        if total_count == 0:
            print("✅ База данных уже чистая!")
            return True
        
        # Удаляем ВСЕ уведомления
        print("🗑️ Удаляем ВСЕ уведомления...")
        deleted_count, _ = Notification.objects.all().delete()
        
        print(f"🎉 Успешно удалено {deleted_count} уведомлений!")
        
        # Проверяем результат
        remaining_count = Notification.objects.count()
        if remaining_count == 0:
            print("✅ ВСЕ уведомления успешно удалены!")
        else:
            print(f"⚠️ Осталось уведомлений: {remaining_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    clear_all_notifications()
