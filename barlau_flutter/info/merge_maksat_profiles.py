#!/usr/bin/env python3
"""
Скрипт для объединения двух профилей Мақсат Құсайын
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

def merge_maksat_profiles():
    print("🔄 Объединяем два профиля Мақсат Құсайын...")
    print("📅 Дата: " + str(datetime.now()))
    
    from django.db import connection
    cursor = connection.cursor()
    
    # Отключаем внешние ключи для SQLite
    cursor.execute("PRAGMA foreign_keys = OFF")
    print("🔓 Внешние ключи отключены")
    
    try:
        # Ищем все профили Мақсат Құсайын
        print(f"\n🔍 Ищем все профили Мақсат Құсайын...")
        cursor.execute("""
            SELECT id, first_name, last_name, role, position, phone, photo, about_me, experience, education, skills, certifications, languages, desired_salary, location, skype, linkedin, portfolio_url, key_skills, achievements, courses, publications, recommendations, hobbies, recommendation_file, date_joined
            FROM accounts_user 
            WHERE first_name = 'Мақсат' AND last_name = 'Құсайын'
            ORDER BY date_joined
        """)
        
        profiles = cursor.fetchall()
        
        if len(profiles) >= 2:
            print(f"  ✅ Найдено {len(profiles)} профилей Мақсат Құсайын")
            
            # Берем первый профиль как основной (более старый)
            main_profile = profiles[0]
            main_id, main_fname, main_lname, main_role, main_position, main_phone, main_photo, main_about_me, main_experience, main_education, main_skills, main_certifications, main_languages, main_desired_salary, main_location, main_skype, main_linkedin, main_portfolio_url, main_key_skills, main_achievements, main_courses, main_publications, main_recommendations, main_hobbies, main_recommendation_file, main_date_joined = main_profile
            
            print(f"  📋 Основной профиль (ID: {main_id}): {main_role}, телефон: {main_phone}")
            
            # Объединяем информацию из всех остальных профилей
            for i, profile in enumerate(profiles[1:], 1):
                profile_id, fname, lname, role, position, phone, photo, about_me, experience, education, skills, certifications, languages, desired_salary, location, skype, linkedin, portfolio_url, key_skills, achievements, courses, publications, recommendations, hobbies, recommendation_file, date_joined = profile
                
                print(f"  📋 Профиль {i+1} (ID: {profile_id}): {role}, телефон: {phone}")
                
                # Объединяем информацию
                updates = []
                
                # Если у дополнительного профиля есть фото, а у основного нет
                if photo and not main_photo:
                    updates.append(("photo = ?", photo))
                    print(f"    📸 Копируем фото от профиля {i+1}")
                
                # Если у дополнительного профиля есть более подробная информация
                if about_me and not main_about_me:
                    updates.append(("about_me = ?", about_me))
                    print(f"    📝 Копируем информацию от профиля {i+1}")
                
                # Объединяем другие поля
                if experience and not main_experience:
                    updates.append(("experience = ?", experience))
                
                if education and not main_education:
                    updates.append(("education = ?", education))
                
                if skills and not main_skills:
                    updates.append(("skills = ?", skills))
                
                if certifications and not main_certifications:
                    updates.append(("certifications = ?", certifications))
                
                if languages and not main_languages:
                    updates.append(("languages = ?", languages))
                
                if desired_salary and not main_desired_salary:
                    updates.append(("desired_salary = ?", desired_salary))
                
                if location and not main_location:
                    updates.append(("location = ?", location))
                
                if skype and not main_skype:
                    updates.append(("skype = ?", skype))
                
                if linkedin and not main_linkedin:
                    updates.append(("linkedin = ?", linkedin))
                
                if portfolio_url and not main_portfolio_url:
                    updates.append(("portfolio_url = ?", portfolio_url))
                
                if key_skills and not main_key_skills:
                    updates.append(("key_skills = ?", key_skills))
                
                if achievements and not main_achievements:
                    updates.append(("achievements = ?", achievements))
                
                if courses and not main_courses:
                    updates.append(("courses = ?", courses))
                
                if publications and not main_publications:
                    updates.append(("publications = ?", publications))
                
                if recommendations and not main_recommendations:
                    updates.append(("recommendations = ?", recommendations))
                
                if hobbies and not main_hobbies:
                    updates.append(("hobbies = ?", hobbies))
                
                if recommendation_file and not main_recommendation_file:
                    updates.append(("recommendation_file = ?", recommendation_file))
                
                # Обновляем основной профиль
                if updates:
                    set_clause = ", ".join([update[0] for update in updates])
                    values = [update[1] for update in updates] + [main_id]
                    
                    cursor.execute(f"""
                        UPDATE accounts_user 
                        SET {set_clause}
                        WHERE id = ?
                    """, values)
                    
                    print(f"    💾 Обновлен основной профиль данными от профиля {i+1}")
                
                # Удаляем дополнительный профиль
                cursor.execute("DELETE FROM accounts_user WHERE id = ?", [profile_id])
                print(f"    ❌ Удален дополнительный профиль {i+1} (ID: {profile_id})")
            
            print(f"\n  ✅ Объединение завершено! Остался один профиль Мақсат Құсайын")
            
        elif len(profiles) == 1:
            print(f"  ⚠️  Найден только один профиль Мақсат Құсайын")
        else:
            print(f"  ❌ Профили Мақсат Құсайын не найдены")
        
    finally:
        # Включаем внешние ключи обратно
        cursor.execute("PRAGMA foreign_keys = ON")
        print("🔒 Внешние ключи включены")
    
    print(f"\n🎉 Операция завершена!")
    
    print(f"\n📈 Итоговая статистика базы данных:")
    print(f"  👤 Пользователей: {User.objects.count()}")
    
    # Показываем финальный профиль Мақсат Құсайын
    print(f"\n👤 Финальный профиль Мақсат Құсайын:")
    maksat = User.objects.filter(first_name='Мақсат', last_name='Құсайын').first()
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
    merge_maksat_profiles()
