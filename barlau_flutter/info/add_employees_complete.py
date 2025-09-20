#!/usr/bin/env python3
"""
Скрипт для добавления Молдиярова Аскара и Беркинбаева Мейрлана
с всеми обязательными полями
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

def add_employees_complete():
    print("➕ Добавляем новых сотрудников с полными данными...")
    print("📅 Дата: " + str(datetime.now()))
    
    from django.db import connection
    cursor = connection.cursor()
    
    # Отключаем внешние ключи для SQLite
    cursor.execute("PRAGMA foreign_keys = OFF")
    print("🔓 Внешние ключи отключены")
    
    try:
        # 1. Добавляем Молдиярова Аскара
        print(f"\n➕ Добавляем: Молдияров Аскар")
        try:
            # Проверяем, не существует ли уже
            cursor.execute("""
                SELECT id FROM accounts_user 
                WHERE first_name = 'Аскар' AND last_name = 'Молдияров'
            """)
            
            if cursor.fetchone():
                print(f"  ⚠️  Молдияров Аскар уже существует")
            else:
                # Создаем нового пользователя со всеми обязательными полями
                cursor.execute("""
                    INSERT INTO accounts_user (
                        username, email, first_name, last_name, role, position, 
                        phone, is_active, is_staff, is_superuser, date_joined, 
                        password, about_me, experience, education, skills, 
                        certifications, languages, desired_salary, location, 
                        skype, linkedin, portfolio_url, key_skills, achievements, 
                        courses, publications, recommendations, hobbies, 
                        recommendation_file, is_phone_verified, is_archived
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    'askar.moldiyarov',  # username
                    'askar.moldiyarov@barlau.kz',  # email
                    'Аскар',  # first_name
                    'Молдияров',  # last_name
                    'MANAGER',  # role
                    'Менеджер',  # position
                    '+77012345678',  # phone
                    1,  # is_active
                    0,  # is_staff
                    0,  # is_superuser
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # date_joined
                    'pbkdf2_sha256$600000$dummy$dummy',  # password (будет изменен)
                    'Опытный менеджер с многолетним стажем работы в транспортной логистике.',  # about_me
                    '5+ лет в транспортной логистике',  # experience
                    'Высшее экономическое образование',  # education
                    'Управление проектами, работа с клиентами',  # skills
                    'Сертификат по логистике',  # certifications
                    'Казахский, русский, английский',  # languages
                    '500000',  # desired_salary
                    'Алматы',  # location
                    '',  # skype
                    '',  # linkedin
                    '',  # portfolio_url
                    'Логистика, управление, клиентский сервис',  # key_skills
                    'Успешное внедрение системы управления флотом',  # achievements
                    'Курсы по логистике и управлению',  # courses
                    '',  # publications
                    '',  # recommendations
                    'Спорт, чтение',  # hobbies
                    '',  # recommendation_file
                    0,  # is_phone_verified
                    0   # is_archived
                ])
                print(f"  ✅ Добавлен: Молдияров Аскар (MANAGER)")
        except Exception as e:
            print(f"  🔴 Ошибка при добавлении Молдиярова Аскара: {e}")
        
        # 2. Добавляем Беркинбаева Мейрлана
        print(f"\n➕ Добавляем: Беркинбаев Мейрлан")
        try:
            # Проверяем, не существует ли уже
            cursor.execute("""
                SELECT id FROM accounts_user 
                WHERE first_name = 'Мейрлан' AND last_name = 'Беркинбаев'
            """)
            
            if cursor.fetchone():
                print(f"  ⚠️  Беркинбаев Мейрлан уже существует")
            else:
                # Создаем нового пользователя со всеми обязательными полями
                cursor.execute("""
                    INSERT INTO accounts_user (
                        username, email, first_name, last_name, role, position, 
                        phone, is_active, is_staff, is_superuser, date_joined, 
                        password, about_me, experience, education, skills, 
                        certifications, languages, desired_salary, location, 
                        skype, linkedin, portfolio_url, key_skills, achievements, 
                        courses, publications, recommendations, hobbies, 
                        recommendation_file, is_phone_verified, is_archived
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    'meirlan.berkinbaev',  # username
                    'meirlan.berkinbaev@barlau.kz',  # email
                    'Мейрлан',  # first_name
                    'Беркинбаев',  # last_name
                    'TECH',  # role
                    'Техник',  # position
                    '+77012345679',  # phone
                    1,  # is_active
                    0,  # is_staff
                    0,  # is_superuser
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # date_joined
                    'pbkdf2_sha256$600000$dummy$dummy',  # password (будет изменен)
                    'Квалифицированный техник по обслуживанию и ремонту транспортных средств.',  # about_me
                    '3+ года в автосервисе',  # experience
                    'Среднее техническое образование',  # education
                    'Диагностика, ремонт двигателей, электрооборудования',  # skills
                    'Сертификат автослесаря',  # certifications
                    'Казахский, русский',  # languages
                    '350000',  # desired_salary
                    'Алматы',  # location
                    '',  # skype
                    '',  # linkedin
                    '',  # portfolio_url
                    'Авторемонт, диагностика, техническое обслуживание',  # key_skills
                    'Снижение времени простоя техники на 30%',  # achievements
                    'Курсы по современным технологиям авторемонта',  # courses
                    '',  # publications
                    '',  # recommendations
                    'Автомобили, техника',  # hobbies
                    '',  # recommendation_file
                    0,  # is_phone_verified
                    0   # is_archived
                ])
                print(f"  ✅ Добавлен: Беркинбаев Мейрлан (TECH)")
        except Exception as e:
            print(f"  🔴 Ошибка при добавлении Беркинбаева Мейрлана: {e}")
        
    finally:
        # Включаем внешние ключи обратно
        cursor.execute("PRAGMA foreign_keys = ON")
        print("🔒 Внешние ключи включены")
    
    print(f"\n🎉 Операция завершена!")
    
    print(f"\n📈 Итоговая статистика базы данных:")
    print(f"  👤 Пользователей: {User.objects.count()}")
    
    # Показываем финальный список сотрудников
    print(f"\n👥 Финальный список сотрудников:")
    employees = User.objects.filter(role__in=['MANAGER', 'ACCOUNTANT', 'TECH']).order_by('first_name', 'last_name')
    for emp in employees:
        print(f"  - {emp.get_full_name()} ({emp.role}) - {emp.position}")
    
    # Показываем администраторов
    print(f"\n👑 Администраторы:")
    admins = User.objects.filter(role__in=['SUPERADMIN', 'ADMIN', 'DIRECTOR']).order_by('first_name', 'last_name')
    for admin in admins:
        print(f"  - {admin.get_full_name()} ({admin.role})")

if __name__ == "__main__":
    add_employees_complete()
