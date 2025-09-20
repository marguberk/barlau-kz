#!/usr/bin/env python3
"""
Скрипт для добавления реальных данных в продакшн базу
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

def add_real_data():
    print("🔄 Добавляем реальные данные в продакшн базу...")
    print("📅 Дата: " + str(datetime.now()))
    
    with transaction.atomic():
        # Добавляем реальных сотрудников
        print(f"\n👥 Добавляем реальных сотрудников...")
        
        real_employees = [
            {
                'first_name': 'Серік',
                'last_name': 'Айдарбеков',
                'username': 'serik_aydarbekov',
                'role': 'MANAGER',
                'phone': '+77757599686',
                'email': 'serik@barlau.org',
                'about_me': 'Родился 1 июня 1986 года. ИИН: 890601301168',
                'position': 'Менеджер'
            },
            {
                'first_name': 'Алмасжан',
                'last_name': 'Сопашев',
                'username': 'almaszhan_sopashev',
                'role': 'MANAGER',
                'phone': '+77057057876',
                'email': 'almaszhan@barlau.org',
                'about_me': 'Родился 24 декабря 1988 года в г.Жаркент. Семейное положение-Женат. Окончил Международный университет «Silkway». ИИН: 881224302564',
                'position': 'Менеджер'
            },
            {
                'first_name': 'Мақсат',
                'last_name': 'Құсайын',
                'username': 'maksat_kusayin',
                'role': 'MANAGER',
                'phone': '+77014977888',
                'email': 'maksat@barlau.org',
                'about_me': 'Родился 16 мая 1988 года в г.Жаркент. Семейное положение-Женат. ИИН: 880516300512',
                'position': 'Менеджер'
            },
            {
                'first_name': 'Ерболат',
                'last_name': 'Кудайбергенов',
                'username': 'erbolat_kudaybergenov',
                'role': 'MANAGER',
                'phone': '+77017525437',
                'email': 'erbolat@barlau.org',
                'about_me': 'Родился 25 февраля 1978 года с.Елтай, Ерейментауский р-он, Акмолинская область. ИИН: 780225350070',
                'position': 'Менеджер'
            },
            {
                'first_name': 'Назерке',
                'last_name': 'Садвакасова',
                'username': 'nazerke_sadvakasova',
                'role': 'ACCOUNTANT',
                'phone': '+77023200506',
                'email': 'nazerke@barlau.org',
                'about_me': 'Родилась 1 августа 1992 года в г.Жаркент. Семейное положение-Замужем. Окончила КазНУ',
                'position': 'Бухгалтер'
            },
            {
                'first_name': 'Ғабит',
                'last_name': 'Ахметов',
                'username': 'gabit_akhmetov',
                'role': 'TECH',
                'phone': '+77071778202',
                'email': 'gabit@barlau.org',
                'about_me': 'Родился 13 декабря 1990 года в г.Жаркент. Семейное положение-Холостой. ИИН: 901213302223',
                'position': 'Техник'
            },
            {
                'first_name': 'Азиз',
                'last_name': 'Илямов',
                'username': 'aziz_ilyamov',
                'role': 'TECH',
                'phone': '+777789509264',
                'email': 'aziz@barlau.org',
                'about_me': 'Родился 22 октября 1995 года в г.Жаркент. Семейное положение-Женат. ИИН: 951022300812',
                'position': 'Техник'
            },
            {
                'first_name': 'Айдана',
                'last_name': 'Ұзақ',
                'username': 'aidana_uzak',
                'role': 'MANAGER',
                'phone': '+77076156475',
                'email': 'aidana@barlau.org',
                'about_me': 'Родилась 1 февраля 1998 года в г.Жаркент. 2020 году окончила АТУ, по специальности-технология. Семейное положение-Замужем. Дети-1. ИИН: 980201400864',
                'position': 'Менеджер'
            },
            {
                'first_name': 'Асель',
                'last_name': 'Мұрат',
                'username': 'asel_murat',
                'role': 'MANAGER',
                'phone': '+777781008373',
                'email': 'asel@barlau.org',
                'about_me': 'Родилась 19 сентября 1995 года в г.Жаркент. Образование-незаконченное высшее. Семейное положение-в разводе. Дети-1. ИИН: 950919401325',
                'position': 'Менеджер'
            }
        ]
        
        added_employees = 0
        for emp_data in real_employees:
            try:
                user, created = User.objects.get_or_create(
                    username=emp_data['username'],
                    defaults={
                        'first_name': emp_data['first_name'],
                        'last_name': emp_data['last_name'],
                        'email': emp_data['email'],
                        'role': emp_data['role'],
                        'phone': emp_data['phone'],
                        'about_me': emp_data['about_me'],
                        'position': emp_data['position'],
                        'is_active': True,
                        'is_staff': emp_data['role'] in ['ADMIN', 'SUPERADMIN', 'DIRECTOR'],
                        'is_superuser': emp_data['role'] == 'SUPERADMIN'
                    }
                )
                
                if created:
                    user.set_password('barlau2025')
                    user.save()
                    added_employees += 1
                    print(f"  ✅ Добавлен сотрудник: {emp_data['first_name']} {emp_data['last_name']} - {emp_data['role']}")
                else:
                    print(f"  ⚠️  Сотрудник уже существует: {emp_data['first_name']} {emp_data['last_name']}")
                    
            except Exception as e:
                print(f"  🔴 Ошибка при добавлении {emp_data['first_name']} {emp_data['last_name']}: {e}")
        
        # Добавляем реальных водителей
        print(f"\n🚗 Добавляем реальных водителей...")
        
        real_drivers = [
            {'first_name': 'Сухрат', 'last_name': 'Касимов', 'username': 'driver_sukhrat_kasimov', 'phone': '+777775251777', 'license_number': '011001500617'},
            {'first_name': 'Хезиз', 'last_name': 'Қасенов', 'username': 'driver_kheziz_kassenov', 'phone': '+77015843537', 'license_number': '900720302326'},
            {'first_name': 'Ғабит', 'last_name': 'Сабит', 'username': 'driver_gabit_sabit', 'phone': '+77479499219', 'license_number': '990920300224'},
            {'first_name': 'Рустем', 'last_name': 'Садыров', 'username': 'driver_rustem_sadyrov', 'phone': '+77054029789', 'license_number': '851015303223'},
            {'first_name': 'Хамражан', 'last_name': 'Пида', 'username': 'driver_khamrazhan_pida', 'phone': '+77471676916', 'license_number': '940803300734'},
            {'first_name': 'Азизжан', 'last_name': 'Камердинов', 'username': 'driver_azizhan_kamerdinov', 'phone': '+77477020048', 'license_number': '901026301546'},
            {'first_name': 'Сраилжан', 'last_name': 'Рузиев', 'username': 'driver_srailzhan_ruziev', 'phone': '+77025432163', 'license_number': '900821301208'},
            {'first_name': 'Абдулжан', 'last_name': 'Саит', 'username': 'driver_abdulzhan_sait', 'phone': '+777714592745', 'license_number': '950116300573'},
            {'first_name': 'Хамит', 'last_name': 'Абдуллаев', 'username': 'driver_khamit_abdullayev', 'phone': '+77472506006', 'license_number': '930427301112'},
            {'first_name': 'Марат', 'last_name': 'Муталипов', 'username': 'driver_marat_mutalipov', 'phone': '+777761605888', 'license_number': '880128302163'},
            {'first_name': 'Розахун', 'last_name': 'Исмаилов', 'username': 'driver_rozakhun_ismailov', 'phone': '+777777242458', 'license_number': '970110300425'},
            {'first_name': 'Шахмурат', 'last_name': 'Касымов', 'username': 'driver_shakhmurat_kassymov', 'phone': '+77079114708', 'license_number': '830828300014'},
            {'first_name': 'Жасулан', 'last_name': 'Кудайбергенов', 'username': 'driver_zhasulan_kudaybergenov', 'phone': '+77052224788', 'license_number': '881204301349'},
            {'first_name': 'Елдос', 'last_name': 'Умурбеков', 'username': 'driver_yeldos_umurbekov', 'phone': '+777759922900', 'license_number': '910405301367'}
        ]
        
        added_drivers = 0
        for driver_data in real_drivers:
            try:
                user, created = User.objects.get_or_create(
                    username=driver_data['username'],
                    defaults={
                        'first_name': driver_data['first_name'],
                        'last_name': driver_data['last_name'],
                        'email': f"{driver_data['first_name'].lower()}@barlau.org",
                        'role': 'DRIVER',
                        'phone': driver_data['phone'],
                        'about_me': f"Водительское удостоверение: {driver_data['license_number']}",
                        'position': 'Водитель',
                        'is_active': True,
                        'is_staff': False,
                        'is_superuser': False
                    }
                )
                
                if created:
                    user.set_password('barlau2025')
                    user.save()
                    added_drivers += 1
                    print(f"  ✅ Добавлен водитель: {driver_data['first_name']} {driver_data['last_name']}")
                else:
                    print(f"  ⚠️  Водитель уже существует: {driver_data['first_name']} {driver_data['last_name']}")
                    
            except Exception as e:
                print(f"  🔴 Ошибка при добавлении водителя {driver_data['first_name']} {driver_data['last_name']}: {e}")
        
        # Добавляем реальные транспортные средства
        print(f"\n🚛 Добавляем реальные транспортные средства...")
        
        real_vehicles = [
            {'number': '484ATL01', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '057AUC01', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '456AUC01', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '956AUN01', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '533ATL01', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '290ATL01', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '355ATL01', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '474ATL01', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '257ASC01', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '108AGR19', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '481ACA19', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '523BMT02', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '042BJK02', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '695BHS02', 'brand': 'ВОЛЬВО', 'model': 'ВОЛЬВО', 'vehicle_type': 'TRUCK'},
            {'number': '213AUL01', 'brand': 'МЕРСЕДЕС', 'model': 'МЕРСЕДЕС', 'vehicle_type': 'TRUCK'},
            {'number': '208AUL01', 'brand': 'МЕРСЕДЕС', 'model': 'МЕРСЕДЕС', 'vehicle_type': 'TRUCK'},
            {'number': '203AUL01', 'brand': 'МЕРСЕДЕС', 'model': 'МЕРСЕДЕС', 'vehicle_type': 'TRUCK'},
            {'number': '359AUL01', 'brand': 'МЕРСЕДЕС', 'model': 'МЕРСЕДЕС', 'vehicle_type': 'TRUCK'},
            {'number': '355AUL01', 'brand': 'МЕРСЕДЕС', 'model': 'МЕРСЕДЕС', 'vehicle_type': 'TRUCK'},
            {'number': '287AUL01', 'brand': 'КАМАЗ', 'model': 'КАМАЗ', 'vehicle_type': 'TRUCK'},
            {'number': '917AQM01', 'brand': 'КАМАЗ', 'model': 'КАМАЗ', 'vehicle_type': 'TRUCK'},
            {'number': '913AQM01', 'brand': 'КАМАЗ', 'model': 'КАМАЗ', 'vehicle_type': 'TRUCK'},
            {'number': '105AGR19', 'brand': 'КАМАЗ', 'model': 'КАМАЗ', 'vehicle_type': 'TRUCK'},
            {'number': '494AVW01', 'brand': 'DAF', 'model': 'DAF', 'vehicle_type': 'TRUCK'}
        ]
        
        added_vehicles = 0
        for vehicle_data in real_vehicles:
            try:
                vehicle, created = Vehicle.objects.get_or_create(
                    number=vehicle_data['number'],
                    defaults={
                        'brand': vehicle_data['brand'],
                        'model': vehicle_data['model'],
                        'vehicle_type': vehicle_data['vehicle_type'],
                        'year': 2020,
                        'status': 'AVAILABLE',
                        'cargo_capacity': 20.0,
                        'fuel_type': 'DIESEL',
                        'is_archived': False
                    }
                )
                
                if created:
                    added_vehicles += 1
                    print(f"  ✅ Добавлено ТС: {vehicle_data['number']} - {vehicle_data['brand']}")
                else:
                    print(f"  ⚠️  ТС уже существует: {vehicle_data['number']}")
                    
            except Exception as e:
                print(f"  🔴 Ошибка при добавлении ТС {vehicle_data['number']}: {e}")
        
        print(f"\n🎉 Добавление реальных данных завершено!")
        print(f"📊 Статистика операции:")
        print(f"  ✅ Добавлено сотрудников: {added_employees}")
        print(f"  ✅ Добавлено водителей: {added_drivers}")
        print(f"  ✅ Добавлено ТС: {added_vehicles}")
        
        print(f"\n📈 Итоговая статистика базы данных:")
        print(f"  👤 Пользователей: {User.objects.count()}")
        print(f"  🚛 Транспортных средств: {Vehicle.objects.count()}")

if __name__ == "__main__":
    add_real_data()