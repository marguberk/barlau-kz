#!/usr/bin/env python3
"""
Скрипт для удаления конкретных пользователей и объединения Максат/Мақсат
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

def remove_specific_users():
    print("🔄 Удаляем конкретных пользователей и объединяем Максат/Мақсат...")
    print("📅 Дата: " + str(datetime.now()))
    
    from django.db import connection
    cursor = connection.cursor()
    
    # Отключаем внешние ключи для SQLite
    cursor.execute("PRAGMA foreign_keys = OFF")
    print("🔓 Внешние ключи отключены")
    
    try:
        # 1. Удаляем Асет Ильямов
        print(f"\n🔍 Ищем для удаления: Асет Ильямов")
        cursor.execute("""
            SELECT id, first_name, last_name, role 
            FROM accounts_user 
            WHERE first_name = 'Асет' AND last_name = 'Ильямов'
        """)
        
        aset_users = cursor.fetchall()
        if aset_users:
            for user in aset_users:
                user_id, fname, lname, role = user
                print(f"  ❌ Удаляем: {fname} {lname} ({role})")
                cursor.execute("DELETE FROM accounts_user WHERE id = ?", [user_id])
        else:
            print(f"  ⚠️  Асет Ильямов не найден")
        
        # 2. Удаляем Муратжан Илахунов
        print(f"\n🔍 Ищем для удаления: Муратжан Илахунов")
        cursor.execute("""
            SELECT id, first_name, last_name, role 
            FROM accounts_user 
            WHERE first_name = 'Муратжан' AND last_name = 'Илахунов'
        """)
        
        murat_users = cursor.fetchall()
        if murat_users:
            for user in murat_users:
                user_id, fname, lname, role = user
                print(f"  ❌ Удаляем: {fname} {lname} ({role})")
                cursor.execute("DELETE FROM accounts_user WHERE id = ?", [user_id])
        else:
            print(f"  ⚠️  Муратжан Илахунов не найден")
        
        # 3. Объединяем Максат Кусаинов и Мақсат Құсайын
        print(f"\n🔍 Объединяем: Максат Кусаинов -> Мақсат Құсайын")
        
        # Ищем Максат Кусаинов (старый)
        cursor.execute("""
            SELECT id, first_name, last_name, role, photo, about_me, experience, education, skills, certifications, languages, desired_salary, location, skype, linkedin, portfolio_url, key_skills, achievements, courses, publications, recommendations, hobbies, recommendation_file
            FROM accounts_user 
            WHERE first_name = 'Максат' AND last_name = 'Кусаинов'
        """)
        
        old_maksat = cursor.fetchone()
        
        # Ищем Мақсат Құсайын (новый)
        cursor.execute("""
            SELECT id, first_name, last_name, role, photo, about_me, experience, education, skills, certifications, languages, desired_salary, location, skype, linkedin, portfolio_url, key_skills, achievements, courses, publications, recommendations, hobbies, recommendation_file
            FROM accounts_user 
            WHERE first_name = 'Мақсат' AND last_name = 'Құсайын'
        """)
        
        new_maksat = cursor.fetchone()
        
        if old_maksat and new_maksat:
            print(f"  ✅ Найдены оба пользователя")
            
            old_id, old_fname, old_lname, old_role, old_photo, old_about_me, old_experience, old_education, old_skills, old_certifications, old_languages, old_desired_salary, old_location, old_skype, old_linkedin, old_portfolio_url, old_key_skills, old_achievements, old_courses, old_publications, old_recommendations, old_hobbies, old_recommendation_file = old_maksat
            new_id, new_fname, new_lname, new_role, new_photo, new_about_me, new_experience, new_education, new_skills, new_certifications, new_languages, new_desired_salary, new_location, new_skype, new_linkedin, new_portfolio_url, new_key_skills, new_achievements, new_courses, new_publications, new_recommendations, new_hobbies, new_recommendation_file = new_maksat
            
            # Объединяем информацию
            updates = []
            if old_photo and not new_photo:
                updates.append(("photo = ?", old_photo))
                print(f"  📸 Копируем фото от старого пользователя")
            
            if old_about_me and not new_about_me:
                updates.append(("about_me = ?", old_about_me))
                print(f"  📝 Копируем информацию от старого пользователя")
            
            if old_experience and not new_experience:
                updates.append(("experience = ?", old_experience))
            
            if old_education and not new_education:
                updates.append(("education = ?", old_education))
            
            if old_skills and not new_skills:
                updates.append(("skills = ?", old_skills))
            
            if old_certifications and not new_certifications:
                updates.append(("certifications = ?", old_certifications))
            
            if old_languages and not new_languages:
                updates.append(("languages = ?", old_languages))
            
            if old_desired_salary and not new_desired_salary:
                updates.append(("desired_salary = ?", old_desired_salary))
            
            if old_location and not new_location:
                updates.append(("location = ?", old_location))
            
            if old_skype and not new_skype:
                updates.append(("skype = ?", old_skype))
            
            if old_linkedin and not new_linkedin:
                updates.append(("linkedin = ?", old_linkedin))
            
            if old_portfolio_url and not new_portfolio_url:
                updates.append(("portfolio_url = ?", old_portfolio_url))
            
            if old_key_skills and not new_key_skills:
                updates.append(("key_skills = ?", old_key_skills))
            
            if old_achievements and not new_achievements:
                updates.append(("achievements = ?", old_achievements))
            
            if old_courses and not new_courses:
                updates.append(("courses = ?", old_courses))
            
            if old_publications and not new_publications:
                updates.append(("publications = ?", old_publications))
            
            if old_recommendations and not new_recommendations:
                updates.append(("recommendations = ?", old_recommendations))
            
            if old_hobbies and not new_hobbies:
                updates.append(("hobbies = ?", old_hobbies))
            
            if old_recommendation_file and not new_recommendation_file:
                updates.append(("recommendation_file = ?", old_recommendation_file))
            
            # Обновляем нового пользователя
            if updates:
                set_clause = ", ".join([update[0] for update in updates])
                values = [update[1] for update in updates] + [new_id]
                
                cursor.execute(f"""
                    UPDATE accounts_user 
                    SET {set_clause}
                    WHERE id = ?
                """, values)
                
                print(f"  💾 Обновлен пользователь: {new_fname} {new_lname}")
            
            # Удаляем старого пользователя
            cursor.execute("DELETE FROM accounts_user WHERE id = ?", [old_id])
            print(f"  ❌ Удален старый пользователь: {old_fname} {old_lname}")
            
        elif new_maksat and not old_maksat:
            print(f"  ⚠️  Найден только новый пользователь: Мақсат Құсайын")
        elif old_maksat and not new_maksat:
            print(f"  ⚠️  Найден только старый пользователь: Максат Кусаинов")
        else:
            print(f"  ❌ Пользователи не найдены")
        
    finally:
        # Включаем внешние ключи обратно
        cursor.execute("PRAGMA foreign_keys = ON")
        print("🔒 Внешние ключи включены")
    
    print(f"\n🎉 Операции завершены!")
    
    print(f"\n📈 Итоговая статистика базы данных:")
    print(f"  👤 Пользователей: {User.objects.count()}")
    
    # Показываем финальный список сотрудников
    print(f"\n👥 Финальный список сотрудников:")
    employees = User.objects.filter(role__in=['MANAGER', 'ACCOUNTANT', 'TECH']).order_by('first_name', 'last_name')
    for emp in employees:
        print(f"  - {emp.get_full_name()} ({emp.role})")

if __name__ == "__main__":
    remove_specific_users()
