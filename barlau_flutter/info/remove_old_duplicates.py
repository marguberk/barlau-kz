#!/usr/bin/env python3
"""
Скрипт для удаления старых дубликатов сотрудников
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

def remove_old_duplicates():
    print("🔄 Удаляем старые дубликаты сотрудников...")
    print("📅 Дата: " + str(datetime.now()))
    
    from django.db import connection
    cursor = connection.cursor()
    
    # Отключаем внешние ключи для SQLite
    cursor.execute("PRAGMA foreign_keys = OFF")
    print("🔓 Внешние ключи отключены")
    
    try:
        # Список старых пользователей для удаления
        old_users_to_remove = [
            ('Айдана', 'Узакова'),
            ('Алмас', 'Сопашев'),
            ('Габит', 'Ахметов'),
            ('Асет', 'Ильямов'),
            ('Серик', 'Айдарбеков')
        ]
        
        removed_count = 0
        
        for first_name, last_name in old_users_to_remove:
            try:
                print(f"  🔍 Ищем для удаления: {first_name} {last_name}")
                
                # Ищем пользователя
                cursor.execute("""
                    SELECT id, first_name, last_name, role 
                    FROM accounts_user 
                    WHERE first_name LIKE ? AND last_name LIKE ?
                """, [f'%{first_name}%', f'%{last_name}%'])
                
                users = cursor.fetchall()
                
                if users:
                    for user in users:
                        user_id, fname, lname, role = user
                        print(f"    ❌ Удаляем: {fname} {lname} ({role})")
                        cursor.execute("DELETE FROM accounts_user WHERE id = ?", [user_id])
                        removed_count += 1
                else:
                    print(f"    ⚠️  Пользователь не найден: {first_name} {last_name}")
                    
            except Exception as e:
                print(f"  🔴 Ошибка при удалении {first_name} {last_name}: {e}")
        
        # Удаляем дубликат "Асет Ильямов" (оставляем "Азиз Илямов")
        try:
            print(f"  🔍 Ищем дубликат Асет Ильямов для удаления")
            cursor.execute("""
                SELECT id, first_name, last_name, role 
                FROM accounts_user 
                WHERE first_name = 'Асет' AND last_name = 'Ильямов'
            """)
            
            aset_users = cursor.fetchall()
            if aset_users:
                for user in aset_users:
                    user_id, fname, lname, role = user
                    print(f"    ❌ Удаляем дубликат: {fname} {lname} ({role})")
                    cursor.execute("DELETE FROM accounts_user WHERE id = ?", [user_id])
                    removed_count += 1
            else:
                print(f"    ⚠️  Дубликат Асет Ильямов не найден")
                
        except Exception as e:
            print(f"  🔴 Ошибка при удалении дубликата Асет Ильямов: {e}")
        
    finally:
        # Включаем внешние ключи обратно
        cursor.execute("PRAGMA foreign_keys = ON")
        print("🔒 Внешние ключи включены")
    
    print(f"\n🎉 Удаление старых дубликатов завершено!")
    print(f"📊 Статистика операции:")
    print(f"  ❌ Удалено старых пользователей: {removed_count}")
    
    print(f"\n📈 Итоговая статистика базы данных:")
    print(f"  👤 Пользователей: {User.objects.count()}")
    
    # Показываем финальный список сотрудников
    print(f"\n👥 Финальный список сотрудников:")
    employees = User.objects.filter(role__in=['MANAGER', 'ACCOUNTANT', 'TECH']).order_by('first_name', 'last_name')
    for emp in employees:
        print(f"  - {emp.get_full_name()} ({emp.role})")

if __name__ == "__main__":
    remove_old_duplicates()
