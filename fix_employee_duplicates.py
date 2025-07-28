#!/usr/bin/env python3
"""
Скрипт для удаления дублей сотрудников и восстановления полной информации
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

def fix_employee_duplicates():
    """Удаление дублей и восстановление полной информации"""
    
    print("🔄 Удаление дублей сотрудников и восстановление информации...")
    
    # Список ID дублей для удаления (оставляем только оригиналы)
    duplicates_to_delete = [11, 12, 13, 16, 17, 18, 19, 20]
    
    # Удаляем дубли
    for duplicate_id in duplicates_to_delete:
        try:
            user = User.objects.get(id=duplicate_id)
            user.delete()
            print(f"   ✅ Удален дубль: ID {duplicate_id} - {user.first_name} {user.last_name}")
        except User.DoesNotExist:
            print(f"   ⚠️  Дубль с ID {duplicate_id} не найден")
        except Exception as e:
            print(f"   ❌ Ошибка удаления дубля {duplicate_id}: {e}")
    
    # Полная информация о сотрудниках
    employee_data = [
        {
            'id': 1,
            'first_name': 'Серик',
            'last_name': 'Айдарбеков',
            'role': 'DIRECTOR',
            'phone': '+77757599686',
            'position': 'Директор',
            'date_joined': '2023-01-15T10:00:00Z',
            'photo': 'employee_photos/serik.png',
            'about_me': 'Опытный руководитель с более чем 15-летним стажем в логистической отрасли.',
            'experience': '15 лет',
            'education': 'КазНУ им. аль-Фараби, экономический факультет',
            'skills': 'Стратегическое планирование, Управление командой, Развитие бизнеса',
            'achievements': 'Развитие компании с 5 до 50+ сотрудников',
        },
        {
            'id': 2,
            'first_name': 'Юнус',
            'last_name': 'Алиев',
            'role': 'DRIVER',
            'phone': '+7 (777) 159 03 06',
            'position': 'Водитель',
            'date_joined': '2023-02-20T09:30:00Z',
            'photo': 'employee_photos/2.png',
            'about_me': 'Профессиональный водитель международных рейсов с безупречной репутацией.',
            'experience': '8 лет',
            'education': 'Автотранспортный колледж',
            'skills': 'Безопасное вождение, Знание маршрутов, Международные перевозки',
            'achievements': 'Более 500,000 км без аварий',
        },
        {
            'id': 3,
            'first_name': 'Айдана',
            'last_name': 'Узакова',
            'role': 'LOGIST',
            'phone': '+77012345009',
            'position': 'Логист / Офис-менеджер',
            'date_joined': '2023-03-10T11:00:00Z',
            'photo': 'employee_photos/aidana.png',
            'about_me': 'Специалист по планированию маршрутов и координации поставок.',
            'experience': '5 лет',
            'education': 'КазЭУ им. Т. Рыскулова, логистика',
            'skills': 'Планирование маршрутов, Управление запасами, Координация',
            'achievements': 'Оптимизация маршрутов на 25%',
        },
        {
            'id': 4,
            'first_name': 'Муратжан',
            'last_name': 'Илахунов',
            'role': 'CONSULTANT',
            'phone': '+77012345008',
            'position': 'Внештатный консультант',
            'date_joined': '2023-04-01T14:00:00Z',
            'photo': 'employee_photos/muratjan.png',
            'about_me': 'Консультант по развитию бизнеса и стратегическому планированию.',
            'experience': '12 лет',
            'education': 'КИМЭП, MBA',
            'skills': 'Юридическая поддержка, Консультирование, Стратегическое планирование',
            'achievements': 'Консультирование 20+ компаний',
        },
        {
            'id': 5,
            'first_name': 'Ерболат',
            'last_name': 'Кудайбергенов',
            'role': 'MANAGER',
            'phone': '+77012345003',
            'position': 'Менеджер',
            'date_joined': '2023-05-05T10:00:00Z',
            'photo': 'employee_photos/erbolat.png',
            'about_me': 'Менеджер по работе с клиентами и развитию партнерских отношений.',
            'experience': '7 лет',
            'education': 'АТУ, менеджмент',
            'skills': 'Переговоры, Продажи, Управление клиентами',
            'achievements': 'Привлечение 15+ новых клиентов',
        },
        {
            'id': 6,
            'first_name': 'Назерке',
            'last_name': 'Садвакасова',
            'role': 'ACCOUNTANT',
            'phone': '+77012345004',
            'position': 'Бухгалтер',
            'date_joined': '2023-06-01T11:00:00Z',
            'photo': 'employee_photos/nazerke.png',
            'about_me': 'Главный бухгалтер с опытом ведения учета в транспортных компаниях.',
            'experience': '6 лет',
            'education': 'КазЭУ, учет и аудит',
            'skills': 'Финансовый анализ, Налоговое планирование, Бухгалтерский учет',
            'achievements': 'Безупречная отчетность 5+ лет',
        },
        {
            'id': 7,
            'first_name': 'Максат',
            'last_name': 'Кусайын',
            'role': 'IT_MANAGER',
            'phone': '+77012345005',
            'position': 'IT-менеджер',
            'date_joined': '2023-07-01T12:00:00Z',
            'photo': 'employee_photos/7.png',
            'about_me': 'Руководитель IT-отдела, отвечает за цифровизацию процессов.',
            'experience': '9 лет',
            'education': 'КазНТУ, информационные системы',
            'skills': 'Управление IT-проектами, Внедрение систем, Техническая поддержка',
            'achievements': 'Внедрение CRM и ERP систем',
        },
        {
            'id': 8,
            'first_name': 'Габит',
            'last_name': 'Ахметов',
            'role': 'SUPPLIER',
            'phone': '+77012345006',
            'position': 'Снабженец',
            'date_joined': '2023-08-15T09:00:00Z',
            'photo': 'employee_photos/gabit.png',
            'about_me': 'Специалист по закупкам и управлению складскими запасами.',
            'experience': '5 лет',
            'education': 'Торгово-экономический институт',
            'skills': 'Поставки, Переговоры, Логистика, Управление запасами',
            'achievements': 'Снижение затрат на закупки на 20%',
        },
        {
            'id': 9,
            'first_name': 'Асет',
            'last_name': 'Ільямов',
            'role': 'TECH',
            'phone': '+77012345007',
            'position': 'Технический специалист',
            'date_joined': '2023-09-01T10:00:00Z',
            'photo': 'employee_photos/aset.png',
            'about_me': 'Механик по обслуживанию и ремонту транспортных средств.',
            'experience': '4 года',
            'education': 'Автомеханический техникум',
            'skills': 'Диагностика, Ремонт, Обслуживание, Сертификация',
            'achievements': 'Сертификация по ремонту европейских грузовиков',
        },
        {
            'id': 10,
            'first_name': 'Асылбек',
            'last_name': 'Нурланов',
            'role': 'DRIVER',
            'phone': '+77701234567',
            'position': 'Водитель',
            'date_joined': '2023-10-01T11:00:00Z',
            'photo': 'employee_photos/364534896_313106267855822_2439338549827965295_n.jpg',
            'about_me': 'Опытный водитель дальних рейсов, специализация на международных перевозках.',
            'experience': '8 лет',
            'education': 'Автошкола категории E',
            'skills': 'Международные перевозки, Знание языков, Безопасное вождение',
            'achievements': 'Водитель года 2023',
        },
    ]
    
    # Обновляем данные сотрудников
    for data in employee_data:
        try:
            user = User.objects.get(id=data['id'])
            
            # Обновляем основные поля
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.role = data['role']
            user.phone = data['phone']
            user.photo = data['photo'] if data['photo'] else ''
            
            # Обновляем дополнительные поля, если они есть в модели
            if hasattr(user, 'position'):
                user.position = data['position']
            if hasattr(user, 'about_me'):
                user.about_me = data['about_me']
            if hasattr(user, 'experience'):
                user.experience = data['experience']
            if hasattr(user, 'education'):
                user.education = data['education']
            if hasattr(user, 'skills'):
                user.skills = data['skills']
            if hasattr(user, 'achievements'):
                user.achievements = data['achievements']
            
            user.save()
            
            print(f"   ✅ Сотрудник {data['id']}: {data['first_name']} {data['last_name']} - обновлен")
            
        except User.DoesNotExist:
            print(f"   ⚠️  Сотрудник с ID {data['id']} не найден")
        except Exception as e:
            print(f"   ❌ Ошибка обновления сотрудника {data['id']}: {e}")
    
    print(f"\n✅ Удаление дублей и обновление данных завершено!")

if __name__ == '__main__':
    try:
        fix_employee_duplicates()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 