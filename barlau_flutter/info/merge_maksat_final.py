#!/usr/bin/env python3
"""
Скрипт для объединения двух профилей Мақсат Құсайын
Максат Кусайын (ID: 7) -> Мақсат Құсайын (ID: 28)
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

def merge_maksat_final():
    print("🔄 Объединяем два профиля Мақсат Құсайын...")
    print("📅 Дата: " + str(datetime.now()))
    
    from django.db import connection
    cursor = connection.cursor()
    
    # Отключаем внешние ключи для SQLite
    cursor.execute("PRAGMA foreign_keys = OFF")
    print("🔓 Внешние ключи отключены")
    
    try:
        # Ищем оба профиля
        print(f"\n🔍 Ищем профили для объединения...")
        
        # Старый профиль (Максат Кусайын)
        cursor.execute("""
            SELECT id, first_name, last_name, role, position, phone, photo, about_me, experience, education, skills, certifications, languages, desired_salary, location, skype, linkedin, portfolio_url, key_skills, achievements, courses, publications, recommendations, hobbies, recommendation_file, date_joined
            FROM accounts_user 
            WHERE id = 7
        """)
        
        old_profile = cursor.fetchone()
        
        # Новый профиль (Мақсат Құсайын)
        cursor.execute("""
            SELECT id, first_name, last_name, role, position, phone, photo, about_me, experience, education, skills, certifications, languages, desired_salary, location, skype, linkedin, portfolio_url, key_skills, achievements, courses, publications, recommendations, hobbies, recommendation_file, date_joined
            FROM accounts_user 
            WHERE id = 28
        """)
        
        new_profile = cursor.fetchone()
        
        if old_profile and new_profile:
            print(f"  ✅ Найдены оба профиля")
            
            old_id, old_fname, old_lname, old_role, old_position, old_phone, old_photo, old_about_me, old_experience, old_education, old_skills, old_certifications, old_languages, old_desired_salary, old_location, old_skype, old_linkedin, old_portfolio_url, old_key_skills, old_achievements, old_courses, old_publications, old_recommendations, old_hobbies, old_recommendation_file, old_date_joined = old_profile
            new_id, new_fname, new_lname, new_role, new_position, new_phone, new_photo, new_about_me, new_experience, new_education, new_skills, new_certifications, new_languages, new_desired_salary, new_location, new_skype, new_linkedin, new_portfolio_url, new_key_skills, new_achievements, new_courses, new_publications, new_recommendations, new_hobbies, new_recommendation_file, new_date_joined = new_profile
            
            print(f"  📋 Старый профиль (ID: {old_id}): {old_fname} {old_lname} - {old_role} - {old_position} - {old_phone}")
            print(f"  📋 Новый профиль (ID: {new_id}): {new_fname} {new_lname} - {new_role} - {new_position} - {new_phone}")
            
            # Объединяем информацию
            updates = []
            
            # Если у старого профиля есть фото, а у нового нет
            if old_photo and not new_photo:
                updates.append(("photo = ?", old_photo))
                print(f"    📸 Копируем фото от старого профиля")
            
            # Если у старого профиля есть более подробная информация
            if old_about_me and not new_about_me:
                updates.append(("about_me = ?", old_about_me))
                print(f"    📝 Копируем информацию от старого профиля")
            
            # Объединяем другие поля
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
            
            # Обновляем новый профиль
            if updates:
                set_clause = ", ".join([update[0] for update in updates])
                values = [update[1] for update in updates] + [new_id]
                
                cursor.execute(f"""
                    UPDATE accounts_user 
                    SET {set_clause}
                    WHERE id = ?
                """, values)
                
                print(f"    💾 Обновлен новый профиль данными от старого")
            
            # Удаляем старый профиль
            cursor.execute("DELETE FROM accounts_user WHERE id = ?", [old_id])
            print(f"    ❌ Удален старый профиль (ID: {old_id})")
            
            print(f"\n  ✅ Объединение завершено! Остался профиль Мақсат Құсайын (ID: {new_id})")
            
        else:
            print(f"  ❌ Не удалось найти оба профиля")
            if not old_profile:
                print(f"    ⚠️  Старый профиль (ID: 7) не найден")
            if not new_profile:
                print(f"    ⚠️  Новый профиль (ID: 28) не найден")
        
    finally:
        # Включаем внешние ключи обратно
        cursor.execute("PRAGMA foreign_keys = ON")
        print("🔒 Внешние ключи включены")
    
    print(f"\n🎉 Операция завершена!")
    
    print(f"\n📈 Итоговая статистика базы данных:")
    print(f"  👤 Пользователей: {User.objects.count()}")
    
    # Показываем финальный профиль Мақсат Құсайын
    print(f"\n👤 Финальный профиль Мақсат Құсайын:")
    maksat = User.objects.filter(id=28).first()
    if maksat:
        print(f"  - Имя: {maksat.get_full_name()}")
        print(f"  - Роль: {maksat.role}")
        print(f"  - Позиция: {maksat.position}")
        print(f"  - Телефон: {maksat.phone}")
        print(f"  - Фото: {'Есть' if maksat.photo else 'Нет'}")
        print(f"  - Информация: {maksat.about_me[:100] + '...' if maksat.about_me else 'Нет'}")
    else:
        print(f"  ❌ Профиль не найден")

if __name__ == "__main__":
    merge_maksat_final()
