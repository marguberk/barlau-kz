#!/usr/bin/env python
"""
Скрипт для обновления ролей сотрудников на более конкретные в соответствии с их должностями в MySQL базе
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings_production')
django.setup()

from accounts.models import User

def update_employee_roles():
    """Обновляет роли сотрудников в соответствии с их должностями"""
    
    # Маппинг должностей на роли
    role_mapping = {
        'Заместитель директора и главный диспетчер грузовых перевозок': 'DISPATCHER',
        'Начальник автобазы': 'MANAGER',
        'Начальник службы логистики и IT программирования': 'IT_MANAGER',
        'Внештатный консультант': 'CONSULTANT',
        'Логист / Офис-менеджер': 'LOGIST',
    }
    
    updated_count = 0
    
    print("Проверяем текущие роли сотрудников:")
    all_employees = User.objects.filter(is_active=True, first_name__isnull=False).exclude(first_name='')
    for emp in all_employees:
        print(f"  {emp.get_full_name()} - Роль: {emp.role} - Должность: '{emp.position}'")
    
    print("\nОбновляем роли на основе должностей:")
    
    # Обновляем роли на основе должностей
    for position, new_role in role_mapping.items():
        employees = User.objects.filter(position=position)
        for employee in employees:
            old_role = employee.role
            employee.role = new_role
            employee.save()
            print(f"✓ {employee.get_full_name()}: {old_role} → {new_role} ({position})")
            updated_count += 1
    
    # Обновляем сотрудников с должностями "Главный механик" на роль TECH
    main_mechanics = User.objects.filter(position='Главный механик')
    for employee in main_mechanics:
        if employee.role != 'TECH':
            old_role = employee.role
            employee.role = 'TECH'
            employee.save()
            print(f"✓ {employee.get_full_name()}: {old_role} → TECH (Главный механик)")
            updated_count += 1
    
    print(f"\nВсего обновлено ролей: {updated_count}")
    
    # Показываем итоговое распределение ролей
    print("\n=== Итоговое распределение ролей ===")
    for role_code, role_name in User.Role.choices:
        count = User.objects.filter(role=role_code, is_active=True).count()
        if count > 0:
            print(f"{role_name}: {count}")
            # Показываем сотрудников этой роли
            employees = User.objects.filter(role=role_code, is_active=True, first_name__isnull=False).exclude(first_name='')
            for emp in employees:
                print(f"  - {emp.get_full_name()} ({emp.position})")

if __name__ == '__main__':
    print("Обновление ролей сотрудников в MySQL...")
    print("=" * 50)
    update_employee_roles()
    print("=" * 50)
    print("Готово!") 