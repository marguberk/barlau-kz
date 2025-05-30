#!/usr/bin/env python
"""
Скрипт для создания полного кадрового состава компании в MySQL базе данных
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings_production')
django.setup()

from accounts.models import User

def create_company_employees():
    """Создает полный кадровый состав компании согласно организационной схеме 2025"""
    
    employees_data = [
        {
            'username': 'serik.aidarbe',
            'email': 'serik.aidarbe@barlau.org',
            'first_name': 'Серик',
            'last_name': 'Айдарбеков',
            'position': 'Директор',
            'role': 'DIRECTOR',
            'phone': '+77771234567',
            'location': 'Алматы, Казахстан',
            'experience': 'Более 15 лет опыта в управлении логистическими компаниями. Руководил крупными транспортными проектами.',
            'education': 'КазНУ им. аль-Фараби, экономический факультет. MBA в области логистики.',
            'key_skills': 'Стратегическое планирование, управление персоналом, развитие бизнеса, логистика',
            'desired_salary': '800000',
            'age': 45,
        },
        {
            'username': 'almas.sopashev',
            'email': 'almas.sopashev@barlau.org',
            'first_name': 'Алмас',
            'last_name': 'Сопашев',
            'position': 'Заместитель директора и главный диспетчер грузовых перевозок',
            'role': 'MANAGER',
            'phone': '+77771234568',
            'location': 'Алматы, Казахстан',
            'experience': '12 лет в сфере грузовых перевозок. Опыт координации международных маршрутов.',
            'education': 'КазАТК им. М. Тынышпаева, факультет транспорта и логистики.',
            'key_skills': 'Диспетчерская работа, планирование маршрутов, управление автопарком',
            'desired_salary': '600000',
            'age': 38,
        },
        {
            'username': 'erbolat.kudaibergen',
            'email': 'erbolat.kudaibergen@barlau.org',
            'first_name': 'Ерболат',
            'last_name': 'Кудайбергенов',
            'position': 'Начальник автобазы',
            'role': 'MANAGER',
            'phone': '+77771234569',
            'location': 'Алматы, Казахстан',
            'experience': '10 лет управления автопарком. Специалист по техническому обслуживанию транспорта.',
            'education': 'Алматинский технологический университет, автомобильный факультет.',
            'key_skills': 'Управление автопарком, техническое обслуживание, планирование ремонтов',
            'desired_salary': '550000',
            'age': 42,
        },
        {
            'username': 'nazerke.sadvakasova',
            'email': 'nazerke.sadvakasova@barlau.org',
            'first_name': 'Назерке',
            'last_name': 'Садвакасова',
            'position': 'Главный бухгалтер',
            'role': 'ACCOUNTANT',
            'phone': '+77771234570',
            'location': 'Алматы, Казахстан',
            'experience': '8 лет в области бухгалтерского учета транспортных компаний.',
            'education': 'КазЭУ им. Т. Рыскулова, факультет учета и аудита.',
            'key_skills': 'Бухгалтерский учет, налоговое планирование, финансовая отчетность',
            'desired_salary': '450000',
            'age': 35,
        },
        {
            'username': 'maksat.kusaiyn',
            'email': 'maksat.kusaiyn@barlau.org',
            'first_name': 'Максат',
            'last_name': 'Кусайын',
            'position': 'Начальник службы логистики и IT программирования',
            'role': 'MANAGER',
            'phone': '+77771234571',
            'location': 'Алматы, Казахстан',
            'experience': '7 лет в IT и логистике. Разработчик систем управления транспортом.',
            'education': 'КБТУ, факультет информационных технологий.',
            'key_skills': 'Программирование, системы управления, логистическая оптимизация',
            'desired_salary': '700000',
            'age': 32,
        },
        {
            'username': 'gabit.akhmetov',
            'email': 'gabit.akhmetov@barlau.org',
            'first_name': 'Габит',
            'last_name': 'Ахметов',
            'position': 'Снабженец',
            'role': 'SUPPLIER',
            'phone': '+77771234572',
            'location': 'Алматы, Казахстан',
            'experience': '5 лет в сфере снабжения и закупок для транспортных компаний.',
            'education': 'КазНТУ им. К.И. Сатпаева, экономический факультет.',
            'key_skills': 'Закупки, поиск поставщиков, управление складом',
            'desired_salary': '350000',
            'age': 29,
        },
        {
            'username': 'aset.ilyamov',
            'email': 'aset.ilyamov@barlau.org',
            'first_name': 'Асет',
            'last_name': 'Ильямов',
            'position': 'Главный механик',
            'role': 'TECH',
            'phone': '+77771234573',
            'location': 'Алматы, Казахстан',
            'experience': '12 лет ремонта и обслуживания грузового транспорта.',
            'education': 'Алматинский колледж транспорта и коммуникаций.',
            'key_skills': 'Ремонт двигателей, диагностика, техническое обслуживание',
            'desired_salary': '400000',
            'age': 40,
        },
        {
            'username': 'muratjan.ilakhunov',
            'email': 'muratjan.ilakhunov@barlau.org',
            'first_name': 'Муратжан',
            'last_name': 'Илахунов',
            'position': 'Внештатный консультант',
            'role': 'EMPLOYEE',
            'phone': '+77771234574',
            'location': 'Алматы, Казахстан',
            'experience': '20 лет в транспортной отрасли. Консультант по развитию бизнеса.',
            'education': 'КазНУ им. аль-Фараби, экономический факультет.',
            'key_skills': 'Бизнес-консультирование, стратегическое планирование, анализ рынка',
            'desired_salary': '500000',
            'age': 50,
        },
        {
            'username': 'aidana.uzakova',
            'email': 'aidana.uzakova@barlau.org',
            'first_name': 'Айдана',
            'last_name': 'Узакова',
            'position': 'Логист / Офис-менеджер',
            'role': 'EMPLOYEE',
            'phone': '+77771234575',
            'location': 'Алматы, Казахстан',
            'experience': '3 года в логистике и офис-менеджменте.',
            'education': 'КазЭУ им. Т. Рыскулова, факультет логистики.',
            'key_skills': 'Планирование маршрутов, документооборот, клиентский сервис',
            'desired_salary': '300000',
            'age': 26,
        }
    ]
    
    created_count = 0
    
    for emp_data in employees_data:
        # Проверяем, существует ли уже пользователь с таким email
        if User.objects.filter(email=emp_data['email']).exists():
            print(f"Пользователь с email {emp_data['email']} уже существует, пропускаем...")
            continue
            
        # Создаем пользователя
        user = User.objects.create_user(
            username=emp_data['username'],
            email=emp_data['email'],
            password='barlau2025',  # Временный пароль
            first_name=emp_data['first_name'],
            last_name=emp_data['last_name'],
            position=emp_data['position'],
            role=emp_data['role'],
            phone=emp_data['phone'],
            location=emp_data['location'],
            experience=emp_data['experience'],
            education=emp_data['education'],
            key_skills=emp_data['key_skills'],
            desired_salary=emp_data['desired_salary'],
            age=emp_data['age'],
            is_active=True
        )
        
        print(f"✓ Создан сотрудник: {user.get_full_name()} ({user.position})")
        created_count += 1
    
    print(f"\nВсего создано сотрудников: {created_count}")
    print(f"Общее количество пользователей в системе: {User.objects.count()}")

if __name__ == '__main__':
    print("Создание кадрового состава компании BARLAU.KZ...")
    print("=" * 50)
    create_company_employees()
    print("=" * 50)
    print("Готово!") 