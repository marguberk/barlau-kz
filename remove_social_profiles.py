#!/usr/bin/env python
"""
Скрипт для удаления LinkedIn и Skype профилей у всех сотрудников
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings_production')
django.setup()

from accounts.models import User

def remove_social_profiles():
    """Удаляет LinkedIn и Skype профили у всех сотрудников"""
    
    print("Удаление LinkedIn и Skype профилей у всех сотрудников:")
    print("=" * 60)
    
    # Получаем всех активных пользователей с именами
    employees = User.objects.filter(
        is_active=True,
        first_name__isnull=False
    ).exclude(first_name='')
    
    updated_count = 0
    
    for employee in employees:
        try:
            # Проверяем, есть ли что удалять
            had_linkedin = bool(employee.linkedin)
            had_skype = bool(employee.skype)
            
            if had_linkedin or had_skype:
                # Очищаем поля
                employee.linkedin = ''
                employee.skype = ''
                employee.save()
                
                removed_fields = []
                if had_linkedin:
                    removed_fields.append("LinkedIn")
                if had_skype:
                    removed_fields.append("Skype")
                
                print(f"✓ {employee.get_full_name()} - удалены: {', '.join(removed_fields)}")
                updated_count += 1
            else:
                print(f"- {employee.get_full_name()} - нет LinkedIn/Skype профилей")
                
        except Exception as e:
            print(f"✗ {employee.get_full_name()} - ошибка: {e}")
    
    print("=" * 60)
    print(f"Всего обновлено профилей: {updated_count}")

if __name__ == '__main__':
    print("Запуск удаления социальных профилей...")
    remove_social_profiles()
    print("Готово!") 