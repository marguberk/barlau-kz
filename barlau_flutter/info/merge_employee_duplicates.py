#!/usr/bin/env python3
"""
Скрипт для объединения дубликатов сотрудников
Объединяет информацию, оставляя новые имена (кириллица)
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

def merge_employee_duplicates():
    print("🔄 Объединяем дубликаты сотрудников...")
    print("📅 Дата: " + str(datetime.now()))
    
    # Пары для объединения: (новое_имя, старое_имя, новая_фамилия, старая_фамилия)
    employee_pairs = [
        ('Айдана', 'Айдана', 'Ұзақ', 'Узакова'),
        ('Мақсат', 'Максат', 'Құсайын', 'Кусаинов'),
        ('Алмасжан', 'Алмас', 'Сопашев', 'Сопашев'),
        ('Ғабит', 'Габит', 'Ахметов', 'Ахметов'),
        ('Азиз', 'Асет', 'Илямов', 'Ильямов'),
        ('Серік', 'Серик', 'Айдарбеков', 'Айдарбеков')
    ]
    
    merged_count = 0
    
    for new_first, old_first, new_last, old_last in employee_pairs:
        try:
            print(f"\n🔍 Обрабатываем: {old_first} {old_last} -> {new_first} {new_last}")
            
            # Находим нового пользователя (кириллица)
            new_user = User.objects.filter(
                first_name__icontains=new_first,
                last_name__icontains=new_last
            ).first()
            
            # Находим старого пользователя (латиница)
            old_user = User.objects.filter(
                first_name__icontains=old_first,
                last_name__icontains=old_last
            ).first()
            
            if new_user and old_user:
                print(f"  ✅ Найдены оба пользователя")
                
                # Объединяем информацию
                # Если у старого есть фото, а у нового нет - копируем
                if old_user.photo and not new_user.photo:
                    print(f"  📸 Копируем фото от старого пользователя")
                    new_user.photo = old_user.photo
                
                # Объединяем дополнительную информацию
                if old_user.about_me and not new_user.about_me:
                    print(f"  📝 Копируем информацию от старого пользователя")
                    new_user.about_me = old_user.about_me
                
                # Объединяем другие поля
                if old_user.experience and not new_user.experience:
                    new_user.experience = old_user.experience
                
                if old_user.education and not new_user.education:
                    new_user.education = old_user.education
                
                if old_user.skills and not new_user.skills:
                    new_user.skills = old_user.skills
                
                if old_user.certifications and not new_user.certifications:
                    new_user.certifications = old_user.certifications
                
                if old_user.languages and not new_user.languages:
                    new_user.languages = old_user.languages
                
                if old_user.desired_salary and not new_user.desired_salary:
                    new_user.desired_salary = old_user.desired_salary
                
                if old_user.location and not new_user.location:
                    new_user.location = old_user.location
                
                if old_user.skype and not new_user.skype:
                    new_user.skype = old_user.skype
                
                if old_user.linkedin and not new_user.linkedin:
                    new_user.linkedin = old_user.linkedin
                
                if old_user.portfolio_url and not new_user.portfolio_url:
                    new_user.portfolio_url = old_user.portfolio_url
                
                if old_user.key_skills and not new_user.key_skills:
                    new_user.key_skills = old_user.key_skills
                
                if old_user.achievements and not new_user.achievements:
                    new_user.achievements = old_user.achievements
                
                if old_user.courses and not new_user.courses:
                    new_user.courses = old_user.courses
                
                if old_user.publications and not new_user.publications:
                    new_user.publications = old_user.publications
                
                if old_user.recommendations and not new_user.recommendations:
                    new_user.recommendations = old_user.recommendations
                
                if old_user.hobbies and not new_user.hobbies:
                    new_user.hobbies = old_user.hobbies
                
                if old_user.recommendation_file and not new_user.recommendation_file:
                    new_user.recommendation_file = old_user.recommendation_file
                
                # Сохраняем обновленного пользователя
                new_user.save()
                print(f"  💾 Обновлен пользователь: {new_user.get_full_name()}")
                
                # Удаляем старого пользователя
                old_user.delete()
                print(f"  ❌ Удален старый пользователь: {old_first} {old_last}")
                
                merged_count += 1
                
            elif new_user and not old_user:
                print(f"  ⚠️  Найден только новый пользователь: {new_user.get_full_name()}")
            elif old_user and not new_user:
                print(f"  ⚠️  Найден только старый пользователь: {old_user.get_full_name()}")
            else:
                print(f"  ❌ Пользователи не найдены")
                
        except Exception as e:
            print(f"  🔴 Ошибка при объединении {old_first} {old_last}: {e}")
    
    # Обновляем информацию о сотрудниках согласно предоставленным данным
    print(f"\n📝 Обновляем информацию о сотрудниках...")
    
    employee_info = {
        'Айдана Ұзақ': 'Родилась 1 февраля 1998 года в г.Жаркент. 2020 году окончила АТУ, по специальности-технология. Семейное положение-Замужем. Дети-1.',
        'Мақсат Құсайын': 'Родился 16 мая 1988 года в г.Жаркент. Семейное положение-Женат.',
        'Алмасжан Сопашев': 'Родился 24 декабря 1988 года в г.Жаркент. Семейное положение-Женат. Окончил Международный университет «Silkway».',
        'Ғабит Ахметов': 'Родился 13 декабря 1990 года в г.Жаркент. Семейное положение-Холостой.',
        'Азиз Илямов': 'Родился 22 октября 1995 года в г.Жаркент. Семейное положение-Женат.',
        'Серік Айдарбеков': 'Родился 1 июня 1986 года.'
    }
    
    updated_count = 0
    for full_name, info in employee_info.items():
        try:
            first_name, last_name = full_name.split(' ', 1)
            user = User.objects.filter(
                first_name__icontains=first_name,
                last_name__icontains=last_name
            ).first()
            
            if user:
                user.about_me = info
                user.save()
                print(f"  ✅ Обновлена информация: {user.get_full_name()}")
                updated_count += 1
            else:
                print(f"  ⚠️  Пользователь не найден: {full_name}")
                
        except Exception as e:
            print(f"  🔴 Ошибка при обновлении {full_name}: {e}")
    
    print(f"\n🎉 Объединение дубликатов сотрудников завершено!")
    print(f"📊 Статистика операции:")
    print(f"  🔄 Объединено пар пользователей: {merged_count}")
    print(f"  📝 Обновлена информация: {updated_count}")
    
    print(f"\n📈 Итоговая статистика базы данных:")
    print(f"  👤 Пользователей: {User.objects.count()}")
    
    # Показываем финальный список сотрудников
    print(f"\n👥 Финальный список сотрудников:")
    employees = User.objects.filter(role__in=['MANAGER', 'ACCOUNTANT', 'TECH']).order_by('first_name', 'last_name')
    for emp in employees:
        print(f"  - {emp.get_full_name()} ({emp.role})")

if __name__ == "__main__":
    merge_employee_duplicates()
