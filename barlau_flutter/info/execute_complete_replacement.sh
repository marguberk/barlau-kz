#!/bin/bash

# Скрипт для полной замены данных на продакшн сервере
# Удаляет тестовые данные и добавляет реальные

echo "🔄 Выполняем полную замену данных в продакшн базе BARLAU.KZ"
echo "📅 Дата: $(date)"
echo ""

# Параметры подключения
SERVER="85.202.192.33"
USER="ubuntu"
PASSWORD="33q97KKRfmnHTY6dCiyuA3g="

echo "🔌 Подключаемся к серверу $SERVER..."

# Выполняем полную замену данных на сервере
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USER@$SERVER" << 'EOF'
# Создаем директорию для скриптов
mkdir -p /home/ubuntu/cleanup_scripts

# Создаем Python скрипт полной замены данных
cat > /home/ubuntu/cleanup_scripts/complete_data_replacement.py << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Комбинированный скрипт для полной замены данных в продакшн базе
1. Удаляет тестовые данные
2. Добавляет реальные данные из предоставленных файлов
"""

import os
import sys
import django
from datetime import datetime

# Настройка Django
sys.path.append('/home/ubuntu/barlau_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Employee, Vehicle, Trip, Expense
from django.db import transaction

def complete_data_replacement():
    """
    Полная замена данных в продакшн базе данных
    """
    
    print("🔄 Начинаем полную замену данных в продакшн базе...")
    print("📅 Дата: " + str(datetime.now()))
    print("")
    
    with transaction.atomic():
        # ЭТАП 1: Очистка тестовых данных
        print("🧹 ЭТАП 1: Очистка тестовых данных...")
        
        # Список сотрудников для удаления (обычные сотрудники)
        employees_to_remove = [
            "Айдарбеков Серік Шайдолдаұлы",
            "Сопашев Алмасжан Сематжанович", 
            "Құсайын Мақсат Ермекұлы",
            "Кудайбергенов Ерболат Чингизович",
            "Садвакасова Назерке Касымхановна",
            "Ахметов Ғабит Сәбитұлы",
            "Илямов Азиз Алымжанұлы",
            "Ұзақ Айдана Ербосынқызы",
            "Мұрат Асель Мұратқызы"
        ]
        
        # Список водителей для удаления
        drivers_to_remove = [
            "Касимов Сухрат Алимжанович",
            "Қасенов Хезиз Ибраимұлы",
            "Сабит Ғабит Нұрғалиұлы",
            "Садыров Рустем Шаукетович",
            "Пида Хамражан Магаметжанович",
            "Камердинов Азизжан Якупжанович",
            "Рузиев Сраилжан Смаилович",
            "Саит Абдулжан Адилович",
            "Абдуллаев Хамит Рахемжанович",
            "Муталипов Марат Хасанович",
            "Исмаилов Розахун Рахимжанович",
            "Касымов Шахмурат Дильмуратович",
            "Кудайбергенов Жасулан Берикович",
            "Умурбеков Елдос Болатханович"
        ]
        
        # Список транспортных средств для удаления
        vehicles_to_remove = [
            "484ATL01", "057AUC01", "456AUC01", "956AUN01", "533ATL01",
            "290ATL01", "355ATL01", "474ATL01", "257ASC01", "108AGR19",
            "481ACA19", "523BMT02", "213AUL01", "208AUL01", "203AUL01",
            "359AUL01", "355AUL01", "287AUL01", "917AQM01", "913AQM01",
            "105AGR19", "042BJK02", "695BHS02", "494AVW01"
        ]
        
        # Удаляем обычных сотрудников
        print("\n👥 Удаляем тестовых сотрудников...")
        removed_employees = 0
        for employee_name in employees_to_remove:
            try:
                employee = Employee.objects.filter(
                    first_name__icontains=employee_name.split()[0],
                    last_name__icontains=employee_name.split()[1]
                ).first()
                
                if employee:
                    print(f"  ❌ Удаляем: {employee_name}")
                    employee.delete()
                    removed_employees += 1
                else:
                    print(f"  ⚠️  Не найден: {employee_name}")
            except Exception as e:
                print(f"  🔴 Ошибка при удалении {employee_name}: {e}")
        
        # Удаляем водителей
        print(f"\n🚗 Удаляем тестовых водителей...")
        removed_drivers = 0
        for driver_name in drivers_to_remove:
            try:
                driver = Employee.objects.filter(
                    first_name__icontains=driver_name.split()[0],
                    last_name__icontains=driver_name.split()[1],
                    role='DRIVER'
                ).first()
                
                if driver:
                    print(f"  ❌ Удаляем водителя: {driver_name}")
                    driver.delete()
                    removed_drivers += 1
                else:
                    print(f"  ⚠️  Водитель не найден: {driver_name}")
            except Exception as e:
                print(f"  🔴 Ошибка при удалении водителя {driver_name}: {e}")
        
        # Удаляем транспортные средства
        print(f"\n🚛 Удаляем тестовые транспортные средства...")
        removed_vehicles = 0
        for vehicle_number in vehicles_to_remove:
            try:
                vehicle = Vehicle.objects.filter(license_plate=vehicle_number).first()
                if vehicle:
                    print(f"  ❌ Удаляем ТС: {vehicle_number}")
                    vehicle.delete()
                    removed_vehicles += 1
                else:
                    print(f"  ⚠️  ТС не найдено: {vehicle_number}")
            except Exception as e:
                print(f"  🔴 Ошибка при удалении ТС {vehicle_number}: {e}")
        
        # Удаляем связанные данные
        print(f"\n🧹 Очищаем связанные данные...")
        trips_deleted = Trip.objects.filter(driver__isnull=True).count()
        Trip.objects.filter(driver__isnull=True).delete()
        expenses_deleted = Expense.objects.filter(employee__isnull=True).count()
        Expense.objects.filter(employee__isnull=True).delete()
        
        print(f"  ❌ Удалено поездок: {trips_deleted}")
        print(f"  ❌ Удалено расходов: {expenses_deleted}")
        
        # ЭТАП 2: Добавление реальных данных
        print(f"\n📝 ЭТАП 2: Добавление реальных данных...")
        
        # Обновляем существующих администраторов
        print("\n👑 Обновляем информацию об администраторах...")
        
        # Беркинбаев Мейрлан Камалбекұлы
        try:
            berkinbaev = User.objects.filter(
                first_name__icontains='Мейрлан',
                last_name__icontains='Беркинбаев'
            ).first()
            
            if berkinbaev:
                print(f"  ✅ Обновляем: Беркинбаев Мейрлан Камалбекұлы")
                berkinbaev.first_name = 'Мейрлан'
                berkinbaev.last_name = 'Беркинбаев'
                berkinbaev.save()
                
                employee, created = Employee.objects.get_or_create(
                    user=berkinbaev,
                    defaults={
                        'first_name': 'Мейрлан',
                        'last_name': 'Беркинбаев',
                        'role': 'SUPERADMIN',
                        'phone': '+77777777777',
                        'email': 'admin@barlau.org',
                        'is_active': True,
                        'date_of_birth': None,
                        'biography': 'Руководитель компании BARLAU Truck Logistics'
                    }
                )
                if not created:
                    employee.first_name = 'Мейрлан'
                    employee.last_name = 'Беркинбаев'
                    employee.role = 'SUPERADMIN'
                    employee.biography = 'Руководитель компании BARLAU Truck Logistics'
                    employee.save()
            else:
                print(f"  ⚠️  Беркинбаев Мейрлан не найден в системе")
        except Exception as e:
            print(f"  🔴 Ошибка при обновлении Беркинбаева: {e}")
        
        # Молдияров Аскар Ахатович
        try:
            moldiyarov = User.objects.filter(
                first_name__icontains='Аскар',
                last_name__icontains='Молдияров'
            ).first()
            
            if moldiyarov:
                print(f"  ✅ Обновляем: Молдияров Аскар Ахатович")
                moldiyarov.first_name = 'Аскар'
                moldiyarov.last_name = 'Молдияров'
                moldiyarov.save()
                
                employee, created = Employee.objects.get_or_create(
                    user=moldiyarov,
                    defaults={
                        'first_name': 'Аскар',
                        'last_name': 'Молдияров',
                        'role': 'DIRECTOR',
                        'phone': '+77758881220',
                        'email': 'askar@barlau.org',
                        'is_active': True,
                        'date_of_birth': datetime(1988, 12, 20),
                        'biography': 'Родился 20 декабря 1988 года в г. Караганда. Семейное положение-Женат. Окончил Российский Университет Дружбы Народов, г.Москва'
                    }
                )
                if not created:
                    employee.first_name = 'Аскар'
                    employee.last_name = 'Молдияров'
                    employee.role = 'DIRECTOR'
                    employee.phone = '+77758881220'
                    employee.date_of_birth = datetime(1988, 12, 20)
                    employee.biography = 'Родился 20 декабря 1988 года в г. Караганда. Семейное положение-Женат. Окончил Российский Университет Дружбы Народов, г.Москва'
                    employee.save()
            else:
                print(f"  ⚠️  Молдияров Аскар не найден в системе")
        except Exception as e:
            print(f"  🔴 Ошибка при обновлении Молдиярова: {e}")
        
        # Добавляем реальных сотрудников
        print(f"\n👥 Добавляем реальных сотрудников...")
        
        real_employees = [
            {
                'first_name': 'Серік',
                'last_name': 'Айдарбеков',
                'middle_name': 'Шайдолдаұлы',
                'role': 'MANAGER',
                'phone': '+77757599686',
                'email': 'serik@barlau.org',
                'date_of_birth': datetime(1986, 6, 1),
                'biography': 'Родился 1 июня 1986 года. ИИН: 890601301168'
            },
            {
                'first_name': 'Алмасжан',
                'last_name': 'Сопашев',
                'middle_name': 'Сематжанович',
                'role': 'MANAGER',
                'phone': '+77057057876',
                'email': 'almaszhan@barlau.org',
                'date_of_birth': datetime(1988, 12, 24),
                'biography': 'Родился 24 декабря 1988 года в г.Жаркент. Семейное положение-Женат. Окончил Международный университет «Silkway». ИИН: 881224302564'
            },
            {
                'first_name': 'Мақсат',
                'last_name': 'Құсайын',
                'middle_name': 'Ермекұлы',
                'role': 'MANAGER',
                'phone': '+77014977888',
                'email': 'maksat@barlau.org',
                'date_of_birth': datetime(1988, 5, 16),
                'biography': 'Родился 16 мая 1988 года в г.Жаркент. Семейное положение-Женат. ИИН: 880516300512'
            },
            {
                'first_name': 'Ерболат',
                'last_name': 'Кудайбергенов',
                'middle_name': 'Чингизович',
                'role': 'MANAGER',
                'phone': '+77017525437',
                'email': 'erbolat@barlau.org',
                'date_of_birth': datetime(1978, 2, 25),
                'biography': 'Родился 25 февраля 1978 года с.Елтай, Ерейментауский р-он, Акмолинская область. ИИН: 780225350070'
            },
            {
                'first_name': 'Назерке',
                'last_name': 'Садвакасова',
                'middle_name': 'Касымхановна',
                'role': 'ACCOUNTANT',
                'phone': '+77023200506',
                'email': 'nazerke@barlau.org',
                'date_of_birth': datetime(1992, 8, 1),
                'biography': 'Родилась 1 августа 1992 года в г.Жаркент. Семейное положение-Замужем. Окончила КазНУ'
            },
            {
                'first_name': 'Ғабит',
                'last_name': 'Ахметов',
                'middle_name': 'Сәбитұлы',
                'role': 'TECH',
                'phone': '+77071778202',
                'email': 'gabit@barlau.org',
                'date_of_birth': datetime(1990, 12, 13),
                'biography': 'Родился 13 декабря 1990 года в г.Жаркент. Семейное положение-Холостой. ИИН: 901213302223'
            },
            {
                'first_name': 'Азиз',
                'last_name': 'Илямов',
                'middle_name': 'Алымжанұлы',
                'role': 'TECH',
                'phone': '+777789509264',
                'email': 'aziz@barlau.org',
                'date_of_birth': datetime(1995, 10, 22),
                'biography': 'Родился 22 октября 1995 года в г.Жаркент. Семейное положение-Женат. ИИН: 951022300812'
            },
            {
                'first_name': 'Айдана',
                'last_name': 'Ұзақ',
                'middle_name': 'Ербосынқызы',
                'role': 'HR_MANAGER',
                'phone': '+77076156475',
                'email': 'aidana@barlau.org',
                'date_of_birth': datetime(1998, 2, 1),
                'biography': 'Родилась 1 февраля 1998 года в г.Жаркент. 2020 году окончила АТУ, по специальности-технология. Семейное положение-Замужем. Дети-1. ИИН: 980201400864'
            },
            {
                'first_name': 'Асель',
                'last_name': 'Мұрат',
                'middle_name': 'Мұратқызы',
                'role': 'HR_MANAGER',
                'phone': '+777781008373',
                'email': 'asel@barlau.org',
                'date_of_birth': datetime(1995, 9, 19),
                'biography': 'Родилась 19 сентября 1995 года в г.Жаркент. Образование-незаконченное высшее. Семейное положение-в разводе. Дети-1. ИИН: 950919401325'
            }
        ]
        
        added_employees = 0
        for emp_data in real_employees:
            try:
                username = f"{emp_data['first_name'].lower()}_{emp_data['last_name'].lower()}"
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': emp_data['first_name'],
                        'last_name': emp_data['last_name'],
                        'email': emp_data['email'],
                        'is_active': True,
                        'is_staff': emp_data['role'] in ['ADMIN', 'SUPERADMIN', 'DIRECTOR'],
                        'is_superuser': emp_data['role'] == 'SUPERADMIN'
                    }
                )
                
                if created:
                    user.set_password('barlau2025')
                    user.save()
                
                employee, created = Employee.objects.get_or_create(
                    user=user,
                    defaults={
                        'first_name': emp_data['first_name'],
                        'last_name': emp_data['last_name'],
                        'middle_name': emp_data.get('middle_name', ''),
                        'role': emp_data['role'],
                        'phone': emp_data['phone'],
                        'email': emp_data['email'],
                        'is_active': True,
                        'date_of_birth': emp_data['date_of_birth'],
                        'biography': emp_data['biography']
                    }
                )
                
                if created:
                    added_employees += 1
                    print(f"  ✅ Добавлен сотрудник: {emp_data['first_name']} {emp_data['last_name']} - {emp_data['role']}")
                    
            except Exception as e:
                print(f"  🔴 Ошибка при добавлении {emp_data['first_name']} {emp_data['last_name']}: {e}")
        
        # Добавляем реальных водителей
        print(f"\n🚗 Добавляем реальных водителей...")
        
        real_drivers = [
            {'first_name': 'Сухрат', 'last_name': 'Касимов', 'middle_name': 'Алимжанович', 'phone': '+777775251777', 'date_of_birth': datetime(2001, 10, 1), 'license_number': '011001500617'},
            {'first_name': 'Хезиз', 'last_name': 'Қасенов', 'middle_name': 'Ибраимұлы', 'phone': '+77015843537', 'date_of_birth': datetime(1990, 7, 20), 'license_number': '900720302326'},
            {'first_name': 'Ғабит', 'last_name': 'Сабит', 'middle_name': 'Нұрғалиұлы', 'phone': '+77479499219', 'date_of_birth': datetime(1999, 9, 20), 'license_number': '990920300224'},
            {'first_name': 'Рустем', 'last_name': 'Садыров', 'middle_name': 'Шаукетович', 'phone': '+77054029789', 'date_of_birth': datetime(1985, 10, 15), 'license_number': '851015303223'},
            {'first_name': 'Хамражан', 'last_name': 'Пида', 'middle_name': 'Магаметжанович', 'phone': '+77471676916', 'date_of_birth': datetime(1994, 8, 3), 'license_number': '940803300734'},
            {'first_name': 'Азизжан', 'last_name': 'Камердинов', 'middle_name': 'Якупжанович', 'phone': '+77477020048', 'date_of_birth': datetime(1990, 10, 26), 'license_number': '901026301546'},
            {'first_name': 'Сраилжан', 'last_name': 'Рузиев', 'middle_name': 'Смаилович', 'phone': '+77025432163', 'date_of_birth': datetime(1990, 8, 21), 'license_number': '900821301208'},
            {'first_name': 'Абдулжан', 'last_name': 'Саит', 'middle_name': 'Адилович', 'phone': '+777714592745', 'date_of_birth': datetime(1995, 1, 16), 'license_number': '950116300573'},
            {'first_name': 'Хамит', 'last_name': 'Абдуллаев', 'middle_name': 'Рахемжанович', 'phone': '+77472506006', 'date_of_birth': datetime(1993, 4, 27), 'license_number': '930427301112'},
            {'first_name': 'Марат', 'last_name': 'Муталипов', 'middle_name': 'Хасанович', 'phone': '+777761605888', 'date_of_birth': datetime(1988, 1, 28), 'license_number': '880128302163'},
            {'first_name': 'Розахун', 'last_name': 'Исмаилов', 'middle_name': 'Рахимжанович', 'phone': '+777777242458', 'date_of_birth': datetime(1997, 1, 10), 'license_number': '970110300425'},
            {'first_name': 'Шахмурат', 'last_name': 'Касымов', 'middle_name': 'Дильмуратович', 'phone': '+77079114708', 'date_of_birth': datetime(1983, 8, 28), 'license_number': '830828300014'},
            {'first_name': 'Жасулан', 'last_name': 'Кудайбергенов', 'middle_name': 'Берикович', 'phone': '+77052224788', 'date_of_birth': datetime(1988, 12, 4), 'license_number': '881204301349'},
            {'first_name': 'Елдос', 'last_name': 'Умурбеков', 'middle_name': 'Болатханович', 'phone': '+777759922900', 'date_of_birth': datetime(1991, 4, 5), 'license_number': '910405301367'}
        ]
        
        added_drivers = 0
        for driver_data in real_drivers:
            try:
                username = f"driver_{driver_data['first_name'].lower()}_{driver_data['last_name'].lower()}"
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': driver_data['first_name'],
                        'last_name': driver_data['last_name'],
                        'email': f"{driver_data['first_name'].lower()}@barlau.org",
                        'is_active': True,
                        'is_staff': False,
                        'is_superuser': False
                    }
                )
                
                if created:
                    user.set_password('barlau2025')
                    user.save()
                
                employee, created = Employee.objects.get_or_create(
                    user=user,
                    defaults={
                        'first_name': driver_data['first_name'],
                        'last_name': driver_data['last_name'],
                        'middle_name': driver_data.get('middle_name', ''),
                        'role': 'DRIVER',
                        'phone': driver_data['phone'],
                        'email': f"{driver_data['first_name'].lower()}@barlau.org",
                        'is_active': True,
                        'date_of_birth': driver_data['date_of_birth'],
                        'biography': f"Родился {driver_data['date_of_birth'].strftime('%d.%m.%Y')}. Водительское удостоверение: {driver_data['license_number']}"
                    }
                )
                
                if created:
                    added_drivers += 1
                    print(f"  ✅ Добавлен водитель: {driver_data['first_name']} {driver_data['last_name']}")
                    
            except Exception as e:
                print(f"  🔴 Ошибка при добавлении водителя {driver_data['first_name']} {driver_data['last_name']}: {e}")
        
        # Добавляем реальные транспортные средства
        print(f"\n🚛 Добавляем реальные транспортные средства...")
        
        real_vehicles = [
            {'license_plate': '484ATL01', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '057AUC01', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '456AUC01', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '956AUN01', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '533ATL01', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '290ATL01', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '355ATL01', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '474ATL01', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '257ASC01', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '108AGR19', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '481ACA19', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '523BMT02', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '042BJK02', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '695BHS02', 'model': 'ВОЛЬВО', 'type': 'TRUCK'},
            {'license_plate': '213AUL01', 'model': 'МЕРСЕДЕС', 'type': 'TRUCK'},
            {'license_plate': '208AUL01', 'model': 'МЕРСЕДЕС', 'type': 'TRUCK'},
            {'license_plate': '203AUL01', 'model': 'МЕРСЕДЕС', 'type': 'TRUCK'},
            {'license_plate': '359AUL01', 'model': 'МЕРСЕДЕС', 'type': 'TRUCK'},
            {'license_plate': '355AUL01', 'model': 'МЕРСЕДЕС', 'type': 'TRUCK'},
            {'license_plate': '287AUL01', 'model': 'КАМАЗ', 'type': 'TRUCK'},
            {'license_plate': '917AQM01', 'model': 'КАМАЗ', 'type': 'TRUCK'},
            {'license_plate': '913AQM01', 'model': 'КАМАЗ', 'type': 'TRUCK'},
            {'license_plate': '105AGR19', 'model': 'КАМАЗ', 'type': 'TRUCK'},
            {'license_plate': '494AVW01', 'model': 'DAF', 'type': 'TRUCK'}
        ]
        
        added_vehicles = 0
        for vehicle_data in real_vehicles:
            try:
                vehicle, created = Vehicle.objects.get_or_create(
                    license_plate=vehicle_data['license_plate'],
                    defaults={
                        'model': vehicle_data['model'],
                        'type': vehicle_data['type'],
                        'is_active': True,
                        'year': 2020,
                        'capacity': 20.0,
                        'fuel_type': 'DIESEL',
                        'status': 'AVAILABLE'
                    }
                )
                
                if created:
                    added_vehicles += 1
                    print(f"  ✅ Добавлено ТС: {vehicle_data['license_plate']} - {vehicle_data['model']}")
                    
            except Exception as e:
                print(f"  🔴 Ошибка при добавлении ТС {vehicle_data['license_plate']}: {e}")
        
        print(f"\n🎉 Полная замена данных завершена!")
        print(f"📊 Статистика операции:")
        print(f"  ❌ Удалено сотрудников: {removed_employees}")
        print(f"  ❌ Удалено водителей: {removed_drivers}")
        print(f"  ❌ Удалено ТС: {removed_vehicles}")
        print(f"  ✅ Добавлено сотрудников: {added_employees}")
        print(f"  ✅ Добавлено водителей: {added_drivers}")
        print(f"  ✅ Добавлено ТС: {added_vehicles}")
        
        print(f"\n📈 Итоговая статистика базы данных:")
        print(f"  👤 Пользователей: {User.objects.count()}")
        print(f"  👥 Сотрудников: {Employee.objects.count()}")
        print(f"  🚛 Транспортных средств: {Vehicle.objects.count()}")
        print(f"  🗺️  Поездок: {Trip.objects.count()}")
        print(f"  💰 Расходов: {Expense.objects.count()}")

if __name__ == "__main__":
    complete_data_replacement()
PYTHON_EOF

# Переходим в директорию проекта
cd /home/ubuntu/barlau_project

# Активируем виртуальное окружение
source venv/bin/activate

# Создаем резервную копию
echo "💾 Создаем резервную копию базы данных..."
BACKUP_FILE="backup_before_replacement_$(date +%Y%m%d_%H%M%S).sql"
mkdir -p /home/ubuntu/backups
pg_dump -h localhost -U barlau_user -d barlau_db > "/home/ubuntu/backups/$BACKUP_FILE"
echo "✅ Резервная копия создана: $BACKUP_FILE"

# Выполняем полную замену данных
echo "🔄 Выполняем полную замену данных..."
python /home/ubuntu/cleanup_scripts/complete_data_replacement.py

echo "✅ Полная замена данных завершена!"
EOF

echo ""
echo "🎉 Полная замена данных в продакшн базе завершена!"
echo "📅 Время завершения: $(date)"
