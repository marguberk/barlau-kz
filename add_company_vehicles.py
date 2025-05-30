#!/usr/bin/env python
"""
Скрипт для добавления автопарка ТОО "Barlau" с полными техническими характеристиками
"""

import os
import sys
import django
from datetime import date, timedelta
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings_production')
django.setup()

from logistics.models import Vehicle, VehicleDocument, VehicleMaintenance
from accounts.models import User

def add_company_vehicles():
    """Добавляет автопарк компании с полными техническими характеристиками"""
    
    # Получаем пользователя, который будет указан как создатель
    try:
        admin_user = User.objects.filter(role='DIRECTOR').first() or User.objects.filter(is_superuser=True).first()
    except:
        admin_user = None
    
    vehicles_data = [
        # VOLVO FH 460 (2020) - 5 штук
        {
            'number': '474 ATL 01',
            'brand': 'VOLVO',
            'model': 'FH 460',
            'year': 2020,
            'vehicle_type': 'TRUCK',
            'status': 'ACTIVE',
            'color': 'Белый',
            'description': 'Тандем тягач с полуприцепом голова 65 м³. Основной рабочий автомобиль для дальних международных перевозок.',
            
            # Технические характеристики VOLVO FH 460
            'engine_capacity': 12.8,  # л
            'fuel_type': 'DIESEL',
            'fuel_consumption': 28.5,  # л/100км
            'length': 16.5,  # м (с полуприцепом)
            'width': 2.55,   # м
            'height': 4.0,   # м
            'max_weight': 44000,  # кг
            'cargo_capacity': 26000,  # кг
            
            # VIN генерируем как реалистичные для VOLVO
            'vin_number': f'YV2A4D{random.randint(10000, 99999)}',
            'engine_number': f'D13K{random.randint(100000, 999999)}',
            'chassis_number': f'FH4{random.randint(100000, 999999)}'
        },
        {
            'number': '484 ATL 01',
            'brand': 'VOLVO',
            'model': 'FH 460',
            'year': 2020,
            'vehicle_type': 'TRUCK',
            'status': 'ACTIVE',
            'color': 'Белый',
            'description': 'Тандем тягач с полуприцепом голова 65 м³. Резервный автомобиль для срочных заказов.',
            'engine_capacity': 12.8,
            'fuel_type': 'DIESEL',
            'fuel_consumption': 28.5,
            'length': 16.5,
            'width': 2.55,
            'height': 4.0,
            'max_weight': 44000,
            'cargo_capacity': 26000,
            'vin_number': f'YV2A4D{random.randint(10000, 99999)}',
            'engine_number': f'D13K{random.randint(100000, 999999)}',
            'chassis_number': f'FH4{random.randint(100000, 999999)}'
        },
        {
            'number': '355 ATL 01',
            'brand': 'VOLVO',
            'model': 'FH 460',
            'year': 2020,
            'vehicle_type': 'TRUCK',
            'status': 'ACTIVE',
            'color': 'Белый',
            'description': 'Тандем тягач с полуприцепом голова 65 м³. Используется для перевозок по маршруту Алматы-Астана.',
            'engine_capacity': 12.8,
            'fuel_type': 'DIESEL',
            'fuel_consumption': 28.5,
            'length': 16.5,
            'width': 2.55,
            'height': 4.0,
            'max_weight': 44000,
            'cargo_capacity': 26000,
            'vin_number': f'YV2A4D{random.randint(10000, 99999)}',
            'engine_number': f'D13K{random.randint(100000, 999999)}',
            'chassis_number': f'FH4{random.randint(100000, 999999)}'
        },
        {
            'number': '290 ATL 01',
            'brand': 'VOLVO',
            'model': 'FH 460',
            'year': 2020,
            'vehicle_type': 'TRUCK',
            'status': 'ACTIVE',
            'color': 'Белый',
            'description': 'Тандем тягач с полуприцепом голова 65 м³. Специализируется на перевозке стройматериалов.',
            'engine_capacity': 12.8,
            'fuel_type': 'DIESEL',
            'fuel_consumption': 28.5,
            'length': 16.5,
            'width': 2.55,
            'height': 4.0,
            'max_weight': 44000,
            'cargo_capacity': 26000,
            'vin_number': f'YV2A4D{random.randint(10000, 99999)}',
            'engine_number': f'D13K{random.randint(100000, 999999)}',
            'chassis_number': f'FH4{random.randint(100000, 999999)}'
        },
        {
            'number': '533 ATL 01',
            'brand': 'VOLVO',
            'model': 'FH 460',
            'year': 2020,
            'vehicle_type': 'TRUCK',
            'status': 'ACTIVE',
            'color': 'Белый',
            'description': 'Тандем тягач с полуприцепом голова 65 м³. Флагман автопарка для VIP клиентов.',
            'engine_capacity': 12.8,
            'fuel_type': 'DIESEL',
            'fuel_consumption': 28.5,
            'length': 16.5,
            'width': 2.55,
            'height': 4.0,
            'max_weight': 44000,
            'cargo_capacity': 26000,
            'vin_number': f'YV2A4D{random.randint(10000, 99999)}',
            'engine_number': f'D13K{random.randint(100000, 999999)}',
            'chassis_number': f'FH4{random.randint(100000, 999999)}'
        },
        
        # MERCEDES ACTROS 420 (2018) - 5 штук
        {
            'number': 'MB 001 RK',
            'brand': 'MERCEDES',
            'model': 'ACTROS 420',
            'year': 2018,
            'vehicle_type': 'TRUCK',
            'status': 'MAINTENANCE',  # На растаможке
            'color': 'Серебристый',
            'description': 'Тандем тягач с полуприцепом голова 70 м³. Находится на растаможке в РК. Увеличенный объем кузова.',
            
            # Технические характеристики MERCEDES ACTROS 420
            'engine_capacity': 10.7,  # л
            'fuel_type': 'DIESEL',
            'fuel_consumption': 26.8,  # л/100км
            'length': 16.8,  # м (с полуприцепом)
            'width': 2.55,   # м
            'height': 4.0,   # м
            'max_weight': 44000,  # кг
            'cargo_capacity': 27500,  # кг (больше чем у Volvo)
            
            'vin_number': f'WDB9{random.randint(100000, 999999)}',
            'engine_number': f'OM47{random.randint(100000, 999999)}',
            'chassis_number': f'ACT{random.randint(100000, 999999)}'
        },
        {
            'number': 'MB 002 RK',
            'brand': 'MERCEDES',
            'model': 'ACTROS 420',
            'year': 2018,
            'vehicle_type': 'TRUCK',
            'status': 'MAINTENANCE',
            'color': 'Серебристый',
            'description': 'Тандем тягач с полуприцепом голова 70 м³. Находится на растаможке в РК. Планируется для маршрута Алматы-Шымкент.',
            'engine_capacity': 10.7,
            'fuel_type': 'DIESEL',
            'fuel_consumption': 26.8,
            'length': 16.8,
            'width': 2.55,
            'height': 4.0,
            'max_weight': 44000,
            'cargo_capacity': 27500,
            'vin_number': f'WDB9{random.randint(100000, 999999)}',
            'engine_number': f'OM47{random.randint(100000, 999999)}',
            'chassis_number': f'ACT{random.randint(100000, 999999)}'
        },
        {
            'number': 'MB 003 RK',
            'brand': 'MERCEDES',
            'model': 'ACTROS 420',
            'year': 2018,
            'vehicle_type': 'TRUCK',
            'status': 'MAINTENANCE',
            'color': 'Серебристый',
            'description': 'Тандем тягач с полуприцепом голова 70 м³. Находится на растаможке в РК. Резерв для расширения автопарка.',
            'engine_capacity': 10.7,
            'fuel_type': 'DIESEL',
            'fuel_consumption': 26.8,
            'length': 16.8,
            'width': 2.55,
            'height': 4.0,
            'max_weight': 44000,
            'cargo_capacity': 27500,
            'vin_number': f'WDB9{random.randint(100000, 999999)}',
            'engine_number': f'OM47{random.randint(100000, 999999)}',
            'chassis_number': f'ACT{random.randint(100000, 999999)}'
        },
        {
            'number': 'MB 004 RK',
            'brand': 'MERCEDES',
            'model': 'ACTROS 420',
            'year': 2018,
            'vehicle_type': 'TRUCK',
            'status': 'MAINTENANCE',
            'color': 'Серебристый',
            'description': 'Тандем тягач с полуприцепом голова 70 м³. Находится на растаможке в РК. Для международных перевозок.',
            'engine_capacity': 10.7,
            'fuel_type': 'DIESEL',
            'fuel_consumption': 26.8,
            'length': 16.8,
            'width': 2.55,
            'height': 4.0,
            'max_weight': 44000,
            'cargo_capacity': 27500,
            'vin_number': f'WDB9{random.randint(100000, 999999)}',
            'engine_number': f'OM47{random.randint(100000, 999999)}',
            'chassis_number': f'ACT{random.randint(100000, 999999)}'
        },
        {
            'number': 'MB 005 RK',
            'brand': 'MERCEDES',
            'model': 'ACTROS 420',
            'year': 2018,
            'vehicle_type': 'TRUCK',
            'status': 'MAINTENANCE',
            'color': 'Серебристый',
            'description': 'Тандем тягач с полуприцепом голова 70 м³. Находится на растаможке в РК. Последний в серии Mercedes.',
            'engine_capacity': 10.7,
            'fuel_type': 'DIESEL',
            'fuel_consumption': 26.8,
            'length': 16.8,
            'width': 2.55,
            'height': 4.0,
            'max_weight': 44000,
            'cargo_capacity': 27500,
            'vin_number': f'WDB9{random.randint(100000, 999999)}',
            'engine_number': f'OM47{random.randint(100000, 999999)}',
            'chassis_number': f'ACT{random.randint(100000, 999999)}'
        },
        
        # DAF 106 480 (2021) - 1 штука
        {
            'number': 'DAF 106 EU',
            'brand': 'DAF',
            'model': '106 480',
            'year': 2021,
            'vehicle_type': 'TRUCK',
            'status': 'INACTIVE',  # В пути из Европы
            'color': 'Синий',
            'description': 'Тандем тягач с полуприцепом голова 65 м³. В пути из Европы. Новейший автомобиль в автопарке с передовыми технологиями.',
            
            # Технические характеристики DAF 106 480
            'engine_capacity': 12.9,  # л
            'fuel_type': 'DIESEL',
            'fuel_consumption': 27.2,  # л/100км
            'length': 16.5,  # м (с полуприцепом)
            'width': 2.55,   # м  
            'height': 4.0,   # м
            'max_weight': 44000,  # кг
            'cargo_capacity': 26500,  # кг
            
            'vin_number': f'XLRA{random.randint(100000, 999999)}',
            'engine_number': f'MX13{random.randint(100000, 999999)}',
            'chassis_number': f'XF1{random.randint(100000, 999999)}'
        }
    ]
    
    created_count = 0
    print("Добавление автопарка ТОО 'Barlau':")
    print("=" * 70)
    
    for vehicle_data in vehicles_data:
        try:
            # Проверяем, не существует ли уже такой номер
            if Vehicle.objects.filter(number=vehicle_data['number']).exists():
                print(f"✗ {vehicle_data['number']} - уже существует")
                continue
            
            # Создаем автомобиль
            vehicle = Vehicle.objects.create(
                number=vehicle_data['number'],
                brand=vehicle_data['brand'],
                model=vehicle_data['model'],
                year=vehicle_data['year'],
                vehicle_type=vehicle_data['vehicle_type'],
                status=vehicle_data['status'],
                color=vehicle_data['color'],
                description=vehicle_data['description'],
                engine_capacity=vehicle_data['engine_capacity'],
                fuel_type=vehicle_data['fuel_type'],
                fuel_consumption=vehicle_data['fuel_consumption'],
                length=vehicle_data['length'],
                width=vehicle_data['width'],
                height=vehicle_data['height'],
                max_weight=vehicle_data['max_weight'],
                cargo_capacity=vehicle_data['cargo_capacity'],
                vin_number=vehicle_data['vin_number'],
                engine_number=vehicle_data['engine_number'],
                chassis_number=vehicle_data['chassis_number'],
                created_by=admin_user
            )
            
            # Добавляем документы для активных автомобилей
            if vehicle.status == 'ACTIVE':
                # Свидетельство о регистрации
                VehicleDocument.objects.create(
                    vehicle=vehicle,
                    document_type='REGISTRATION',
                    number=f'СР-{vehicle.number.replace(" ", "")}',
                    issue_date=date(2020, 3, 15),
                    expiry_date=date(2025, 3, 15),
                    issuing_authority='ДВД г. Алматы',
                    description='Свидетельство о государственной регистрации транспортного средства',
                    created_by=admin_user
                )
                
                # Страховка
                VehicleDocument.objects.create(
                    vehicle=vehicle,
                    document_type='INSURANCE',
                    number=f'ОС-{random.randint(100000, 999999)}',
                    issue_date=date(2024, 1, 1),
                    expiry_date=date(2024, 12, 31),
                    issuing_authority='СК "Евразия"',
                    description='Полис обязательного страхования гражданской ответственности',
                    created_by=admin_user
                )
                
                # Техосмотр
                VehicleDocument.objects.create(
                    vehicle=vehicle,
                    document_type='TECHNICAL_INSPECTION',
                    number=f'ТО-{random.randint(10000, 99999)}',
                    issue_date=date(2024, 6, 1),
                    expiry_date=date(2025, 6, 1),
                    issuing_authority='СТО "Автотехцентр"',
                    description='Свидетельство о прохождении технического осмотра',
                    created_by=admin_user
                )
                
                # Записи о техническом обслуживании
                VehicleMaintenance.objects.create(
                    vehicle=vehicle,
                    maintenance_type='ROUTINE',
                    date=date(2024, 10, 15),
                    mileage=random.randint(80000, 120000),
                    description='Плановое ТО: замена масла, фильтров, проверка тормозной системы',
                    cost=85000,
                    next_maintenance_date=date(2024, 12, 15),
                    next_maintenance_mileage=random.randint(130000, 140000),
                    performed_by='СТО Barlau',
                    created_by=admin_user
                )
            
            print(f"✓ {vehicle.brand} {vehicle.model} ({vehicle.number}) - добавлен")
            created_count += 1
            
        except Exception as e:
            print(f"✗ {vehicle_data['number']} - ошибка: {e}")
    
    print("=" * 70)
    print(f"Всего добавлено автомобилей: {created_count}")
    
    # Статистика по маркам
    volvo_count = Vehicle.objects.filter(brand='VOLVO').count()
    mercedes_count = Vehicle.objects.filter(brand='MERCEDES').count()
    daf_count = Vehicle.objects.filter(brand='DAF').count()
    
    print(f"\nАвтопарк ТОО 'Barlau':")
    print(f"  VOLVO FH 460 (2020): {volvo_count} шт.")
    print(f"  MERCEDES ACTROS 420 (2018): {mercedes_count} шт.")
    print(f"  DAF 106 480 (2021): {daf_count} шт.")
    print(f"  Общий размер автопарка: {volvo_count + mercedes_count + daf_count} автомобилей")

if __name__ == '__main__':
    print("Запуск добавления автопарка компании...")
    add_company_vehicles()
    print("Готово!") 