#!/usr/bin/env python3
"""
Скрипт для исправления дубликатов в продакшн базе
Удаляет дубликаты и обновляет существующие записи
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
from django.db import transaction

def fix_duplicates():
    print("🔄 Исправляем дубликаты в продакшн базе...")
    print("📅 Дата: " + str(datetime.now()))
    
    with transaction.atomic():
        # Исправляем дубликаты пользователей
        print("\n👥 Исправляем дубликаты пользователей...")
        
        # Словарь соответствий кириллица -> латиница
        name_mappings = {
            'Серік': 'Серик',
            'Алмасжан': 'Алмас',
            'Мақсат': 'Максат',
            'Құсайын': 'Кусайын',
            'Ғабит': 'Габит',
            'Азиз': 'Асет',
            'Айдана': 'Айдана',
            'Ұзақ': 'Узакова',
            'Асель': 'Асель',
            'Мұрат': 'Мурат'
        }
        
        # Обновляем существующих пользователей
        updated_users = 0
        for cyrillic_name, latin_name in name_mappings.items():
            try:
                # Находим пользователя с кириллическим именем
                cyrillic_user = User.objects.filter(
                    first_name__icontains=cyrillic_name
                ).first()
                
                # Находим пользователя с латинским именем
                latin_user = User.objects.filter(
                    first_name__icontains=latin_name
                ).first()
                
                if cyrillic_user and latin_user:
                    print(f"  🔄 Обновляем: {cyrillic_name} -> {latin_name}")
                    
                    # Обновляем латинского пользователя данными из кириллического
                    latin_user.first_name = cyrillic_name
                    latin_user.about_me = cyrillic_user.about_me
                    latin_user.phone = cyrillic_user.phone
                    latin_user.email = cyrillic_user.email
                    latin_user.save()
                    
                    # Удаляем кириллического пользователя
                    cyrillic_user.delete()
                    updated_users += 1
                    
            except Exception as e:
                print(f"  🔴 Ошибка при обновлении {cyrillic_name}: {e}")
        
        # Удаляем дубликаты водителей
        print(f"\n🚗 Удаляем дубликаты водителей...")
        
        # Список водителей для удаления (дубликаты)
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
                driver = User.objects.filter(
                    first_name__icontains=driver_name.split()[0],
                    last_name__icontains=driver_name.split()[1],
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
        
        # Список ТС для удаления (старые тестовые)
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
        
        # Обновляем номера ТС (убираем пробелы)
        print(f"\n🔧 Обновляем номера ТС...")
        
        updated_vehicles = 0
        vehicles_to_update = [
            ('484ATL01', '484 ATL 01'),
            ('533ATL01', '533 ATL 01'),
            ('290ATL01', '290 ATL 01')
        ]
        
        for new_number, old_number in vehicles_to_update:
            try:
                # Ищем ТС с пробелами в номере
                old_vehicle = Vehicle.objects.filter(number=old_number).first()
                # Ищем ТС без пробелов
                new_vehicle = Vehicle.objects.filter(number=new_number).first()
                
                if old_vehicle and new_vehicle:
                    print(f"  🔄 Объединяем ТС: {old_number} -> {new_number}")
                    # Обновляем данные нового ТС
                    new_vehicle.brand = old_vehicle.brand
                    new_vehicle.model = old_vehicle.model
                    new_vehicle.save()
                    # Удаляем старое
                    old_vehicle.delete()
                    updated_vehicles += 1
                    
            except Exception as e:
                print(f"  🔴 Ошибка при обновлении ТС {old_number}: {e}")
        
        print(f"\n🎉 Исправление дубликатов завершено!")
        print(f"📊 Статистика операции:")
        print(f"  🔄 Обновлено пользователей: {updated_users}")
        print(f"  ❌ Удалено дубликатов водителей: {removed_drivers}")
        print(f"  ❌ Удалено старых ТС: {removed_vehicles}")
        print(f"  🔄 Обновлено ТС: {updated_vehicles}")
        
        print(f"\n📈 Итоговая статистика базы данных:")
        print(f"  👤 Пользователей: {User.objects.count()}")
        print(f"  🚛 Транспортных средств: {Vehicle.objects.count()}")

if __name__ == "__main__":
    fix_duplicates()
