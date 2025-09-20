#!/usr/bin/env python3
"""
Простой скрипт для удаления дубликатов в продакшн базе
"""

import os
import sys
import django
from datetime import datetime

# Настройка Django
sys.path.append('/var/www/barlau')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from accounts.models import User
from logistics.models import Vehicle

def remove_duplicates():
    print("🔄 Удаляем дубликаты в продакшн базе...")
    print("📅 Дата: " + str(datetime.now()))
    
    # Удаляем дубликаты водителей
    print("\n🚗 Удаляем дубликаты водителей...")
    
    drivers_to_remove = [
        'Ерлан Тулеуов',
        'Данияр Садыков', 
        'Арман Вадиев',
        'Юнус Алиев',
        'Асылбек Нурланов',
        'Асылбек'
    ]
    
    removed_drivers = 0
    for driver_name in drivers_to_remove:
        try:
            if len(driver_name.split()) >= 2:
                driver = User.objects.filter(
                    first_name__icontains=driver_name.split()[0],
                    last_name__icontains=driver_name.split()[1],
                    role='DRIVER'
                ).first()
                
                if driver:
                    print(f"  ❌ Удаляем дубликат водителя: {driver_name}")
                    driver.delete()
                    removed_drivers += 1
            else:
                # Для имени "Асылбек" без фамилии
                driver = User.objects.filter(
                    first_name__icontains=driver_name,
                    role='DRIVER'
                ).first()
                
                if driver:
                    print(f"  ❌ Удаляем дубликат водителя: {driver_name}")
                    driver.delete()
                    removed_drivers += 1
                    
        except Exception as e:
            print(f"  🔴 Ошибка при удалении {driver_name}: {e}")
    
    # Удаляем дубликаты транспортных средств
    print(f"\n🚛 Удаляем дубликаты транспортных средств...")
    
    vehicles_to_remove = [
        '001 KZ 777',
        '002 KZ 777',
        '003 KZ 777', 
        '004 KZ 777',
        '005 KZ 777',
        '123ABX01',
        '533 ATL 01',
        '290 ATL 01',
        '484 ATL 01'
    ]
    
    removed_vehicles = 0
    for vehicle_number in vehicles_to_remove:
        try:
            vehicle = Vehicle.objects.filter(number=vehicle_number).first()
            if vehicle:
                print(f"  ❌ Удаляем старое ТС: {vehicle_number}")
                vehicle.delete()
                removed_vehicles += 1
                
        except Exception as e:
            print(f"  🔴 Ошибка при удалении ТС {vehicle_number}: {e}")
    
    # Удаляем дубликаты пользователей с одинаковыми email
    print(f"\n👥 Удаляем дубликаты пользователей...")
    
    # Находим пользователей с одинаковыми email
    from django.db.models import Count
    duplicate_emails = User.objects.values('email').annotate(
        count=Count('email')
    ).filter(count__gt=1)
    
    removed_users = 0
    for email_data in duplicate_emails:
        email = email_data['email']
        users_with_same_email = User.objects.filter(email=email).order_by('id')
        
        # Оставляем первого, удаляем остальных
        for user in users_with_same_email[1:]:
            print(f"  ❌ Удаляем дубликат пользователя: {user.get_full_name()} ({email})")
            user.delete()
            removed_users += 1
    
    print(f"\n🎉 Удаление дубликатов завершено!")
    print(f"📊 Статистика операции:")
    print(f"  ❌ Удалено дубликатов водителей: {removed_drivers}")
    print(f"  ❌ Удалено старых ТС: {removed_vehicles}")
    print(f"  ❌ Удалено дубликатов пользователей: {removed_users}")
    
    print(f"\n📈 Итоговая статистика базы данных:")
    print(f"  👤 Пользователей: {User.objects.count()}")
    print(f"  🚛 Транспортных средств: {Vehicle.objects.count()}")

if __name__ == "__main__":
    remove_duplicates()
