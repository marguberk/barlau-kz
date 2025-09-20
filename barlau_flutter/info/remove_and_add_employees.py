#!/usr/bin/env python3
"""
Скрипт для удаления Асет Ільямов и Супер Администратор,
и добавления Молдиярова Аскара и Беркинбаева Мейрлана
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

def remove_and_add_employees():
    print("🔄 Удаляем старых сотрудников и добавляем новых...")
    print("📅 Дата: " + str(datetime.now()))
    
    from django.db import connection
    cursor = connection.cursor()
    
    # Отключаем внешние ключи для SQLite
    cursor.execute("PRAGMA foreign_keys = OFF")
    print("🔓 Внешние ключи отключены")
    
    try:
        # 1. Удаляем Асет Ільямов
        print(f"\n🔍 Ищем для удаления: Асет Ільямов")
        cursor.execute("""
            SELECT id, first_name, last_name, role 
            FROM accounts_user 
            WHERE first_name = 'Асет' AND last_name = 'Ільямов'
        """)
        
        aset_users = cursor.fetchall()
        if aset_users:
            for user in aset_users:
                user_id, fname, lname, role = user
                print(f"  ❌ Удаляем: {fname} {lname} ({role})")
                cursor.execute("DELETE FROM accounts_user WHERE id = ?", [user_id])
        else:
            print(f"  ⚠️  Асет Ільямов не найден")
        
        # 2. Удаляем Супер Администратор
        print(f"\n🔍 Ищем для удаления: Супер Администратор")
        cursor.execute("""
            SELECT id, first_name, last_name, role 
            FROM accounts_user 
            WHERE first_name = 'Супер' AND last_name = 'Администратор'
        """)
        
        super_admin_users = cursor.fetchall()
        if super_admin_users:
            for user in super_admin_users:
                user_id, fname, lname, role = user
                print(f"  ❌ Удаляем: {fname} {lname} ({role})")
                cursor.execute("DELETE FROM accounts_user WHERE id = ?", [user_id])
        else:
            print(f"  ⚠️  Супер Администратор не найден")
        
        # 3. Добавляем Молдиярова Аскара
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
                # Создаем нового пользователя
                cursor.execute("""
                    INSERT INTO accounts_user (
                        username, email, first_name, last_name, role, position, 
                        phone, is_active, is_staff, is_superuser, date_joined, 
                        password, about_me
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    'Опытный менеджер с многолетним стажем работы в транспортной логистике.'
                ])
                print(f"  ✅ Добавлен: Молдияров Аскар (MANAGER)")
        except Exception as e:
            print(f"  🔴 Ошибка при добавлении Молдиярова Аскара: {e}")
        
        # 4. Добавляем Беркинбаева Мейрлана
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
                # Создаем нового пользователя
                cursor.execute("""
                    INSERT INTO accounts_user (
                        username, email, first_name, last_name, role, position, 
                        phone, is_active, is_staff, is_superuser, date_joined, 
                        password, about_me
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    'Квалифицированный техник по обслуживанию и ремонту транспортных средств.'
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
    remove_and_add_employees()
