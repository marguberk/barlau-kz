#!/usr/bin/env python3
"""
Агрессивная очистка дубликатов с отключением внешних ключей
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

def aggressive_cleanup():
    print("🔄 Агрессивная очистка дубликатов в продакшн базе...")
    print("📅 Дата: " + str(datetime.now()))
    
    from django.db import connection
    cursor = connection.cursor()
    
    # Отключаем внешние ключи для SQLite
    cursor.execute("PRAGMA foreign_keys = OFF")
    print("🔓 Внешние ключи отключены")
    
    try:
        # ЭТАП 1: Удаление старых тестовых ТС
        print("\n🚛 ЭТАП 1: Удаление старых тестовых ТС...")
        
        old_test_vehicles = [
            '001 KZ 777',
            '002 KZ 777', 
            '003 KZ 777',
            '004 KZ 777',
            '005 KZ 777',
            '123ABX01'
        ]
        
        removed_vehicles = 0
        for vehicle_number in old_test_vehicles:
            try:
                cursor.execute("DELETE FROM logistics_vehicle WHERE number = ?", [vehicle_number])
                if cursor.rowcount > 0:
                    print(f"  ❌ Удалено старое тестовое ТС: {vehicle_number}")
                    removed_vehicles += 1
                else:
                    print(f"  ⚠️  ТС не найдено: {vehicle_number}")
            except Exception as e:
                print(f"  🔴 Ошибка при удалении ТС {vehicle_number}: {e}")
        
        # ЭТАП 2: Объединение ТС с одинаковыми номерами
        print(f"\n🔧 ЭТАП 2: Объединение ТС с одинаковыми номерами...")
        
        vehicle_pairs = [
            ('484ATL01', '484 ATL 01'),
            ('533ATL01', '533 ATL 01'), 
            ('290ATL01', '290 ATL 01')
        ]
        
        merged_vehicles = 0
        for new_number, old_number in vehicle_pairs:
            try:
                # Проверяем существование обоих ТС
                cursor.execute("SELECT id FROM logistics_vehicle WHERE number = ?", [new_number])
                new_vehicle = cursor.fetchone()
                
                cursor.execute("SELECT id FROM logistics_vehicle WHERE number = ?", [old_number])
                old_vehicle = cursor.fetchone()
                
                if new_vehicle and old_vehicle:
                    print(f"  🔄 Объединяем ТС: {old_number} -> {new_number}")
                    cursor.execute("DELETE FROM logistics_vehicle WHERE number = ?", [old_number])
                    merged_vehicles += 1
                elif old_vehicle and not new_vehicle:
                    print(f"  🔄 Переименовываем ТС: {old_number} -> {new_number}")
                    cursor.execute("UPDATE logistics_vehicle SET number = ? WHERE number = ?", [new_number, old_number])
                    merged_vehicles += 1
                else:
                    print(f"  ⚠️  ТС не найдены для объединения: {old_number} -> {new_number}")
                    
            except Exception as e:
                print(f"  🔴 Ошибка при объединении ТС {old_number}: {e}")
        
        # ЭТАП 3: Удаление оставшихся старых тестовых водителей
        print(f"\n🚗 ЭТАП 3: Удаление оставшихся старых тестовых водителей...")
        
        old_drivers = [
            'Ерлан Тулеуов',
            'Данияр Садыков',
            'Арман Вадиев', 
            'Юнус Алиев'
        ]
        
        removed_drivers = 0
        for driver_name in old_drivers:
            try:
                if len(driver_name.split()) >= 2:
                    first_name, last_name = driver_name.split()[0], driver_name.split()[1]
                    cursor.execute("""
                        DELETE FROM accounts_user 
                        WHERE first_name LIKE ? AND last_name LIKE ? AND role = 'DRIVER'
                    """, [f'%{first_name}%', f'%{last_name}%'])
                else:
                    cursor.execute("""
                        DELETE FROM accounts_user 
                        WHERE first_name LIKE ? AND role = 'DRIVER'
                    """, [f'%{driver_name}%'])
                
                if cursor.rowcount > 0:
                    print(f"  ❌ Удален старый тестовый водитель: {driver_name}")
                    removed_drivers += 1
                else:
                    print(f"  ⚠️  Водитель не найден: {driver_name}")
                    
            except Exception as e:
                print(f"  🔴 Ошибка при удалении водителя {driver_name}: {e}")
        
        # ЭТАП 4: Удаление дубликатов пользователей с одинаковыми email
        print(f"\n👥 ЭТАП 4: Удаление дубликатов пользователей...")
        
        # Находим пользователей с одинаковыми email
        cursor.execute("""
            SELECT email, COUNT(*) as count 
            FROM accounts_user 
            GROUP BY email 
            HAVING COUNT(*) > 1
        """)
        
        duplicate_emails = cursor.fetchall()
        removed_users = 0
        
        for email, count in duplicate_emails:
            print(f"  🔍 Найдены дубликаты для email: {email} ({count} записей)")
            
            # Получаем всех пользователей с этим email
            cursor.execute("""
                SELECT id, first_name, last_name, role 
                FROM accounts_user 
                WHERE email = ? 
                ORDER BY id
            """, [email])
            
            users = cursor.fetchall()
            
            # Оставляем первого, удаляем остальных
            for user in users[1:]:
                user_id, first_name, last_name, role = user
                print(f"    ❌ Удаляем дубликат: {first_name} {last_name} ({role})")
                cursor.execute("DELETE FROM accounts_user WHERE id = ?", [user_id])
                removed_users += 1
        
        # ЭТАП 5: Удаление дубликатов по имени и фамилии
        print(f"\n👥 ЭТАП 5: Удаление дубликатов по имени и фамилии...")
        
        # Находим дубликаты по имени и фамилии
        cursor.execute("""
            SELECT first_name, last_name, COUNT(*) as count 
            FROM accounts_user 
            WHERE role NOT IN ('SUPERADMIN', 'ADMIN', 'DIRECTOR')
            GROUP BY first_name, last_name 
            HAVING COUNT(*) > 1
        """)
        
        duplicate_names = cursor.fetchall()
        removed_name_duplicates = 0
        
        for first_name, last_name, count in duplicate_names:
            print(f"  🔍 Найдены дубликаты: {first_name} {last_name} ({count} записей)")
            
            # Получаем всех пользователей с этим именем
            cursor.execute("""
                SELECT id, first_name, last_name, role 
                FROM accounts_user 
                WHERE first_name = ? AND last_name = ? AND role NOT IN ('SUPERADMIN', 'ADMIN', 'DIRECTOR')
                ORDER BY id
            """, [first_name, last_name])
            
            users = cursor.fetchall()
            
            # Оставляем первого, удаляем остальных
            for user in users[1:]:
                user_id, fname, lname, role = user
                print(f"    ❌ Удаляем дубликат: {fname} {lname} ({role})")
                cursor.execute("DELETE FROM accounts_user WHERE id = ?", [user_id])
                removed_name_duplicates += 1
        
    finally:
        # Включаем внешние ключи обратно
        cursor.execute("PRAGMA foreign_keys = ON")
        print("🔒 Внешние ключи включены")
    
    print(f"\n🎉 Агрессивная очистка дубликатов завершена!")
    print(f"📊 Статистика операции:")
    print(f"  ❌ Удалено старых ТС: {removed_vehicles}")
    print(f"  🔄 Объединено ТС: {merged_vehicles}")
    print(f"  ❌ Удалено старых водителей: {removed_drivers}")
    print(f"  ❌ Удалено дубликатов по email: {removed_users}")
    print(f"  ❌ Удалено дубликатов по имени: {removed_name_duplicates}")
    
    print(f"\n📈 Итоговая статистика базы данных:")
    print(f"  👤 Пользователей: {User.objects.count()}")
    print(f"  🚛 Транспортных средств: {Vehicle.objects.count()}")

if __name__ == "__main__":
    aggressive_cleanup()
