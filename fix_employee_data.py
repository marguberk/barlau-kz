#!/usr/bin/env python3
"""
Скрипт для обновления данных сотрудников в продакшн базе
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

def update_employee_data():
    """Обновление данных сотрудников"""
    
    print("🔄 Обновление данных сотрудников...")
    
    # Правильные данные сотрудников с фотографиями
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
            'about_me': 'Опытный руководитель с более чем 10-летним стажем в логистике.',
            'experience': '10 лет',
            'education': 'Менеджмент',
            'skills': 'Стратегическое планирование, Управление командой',
            'achievements': 'Увеличение прибыли на 20% за год',
        },
        {
            'id': 2,
            'first_name': 'Юнус',
            'last_name': 'Алиев',
            'role': 'DRIVER',
            'phone': '+7 (777) 159 03 06',
            'position': 'Водитель',
            'date_joined': '2023-02-20T09:30:00Z',
            'photo': 'employee_photos/2.png', # Оставляем как есть
            'about_me': 'Профессиональный водитель с большим опытом международных перевозок.',
            'experience': '8 лет',
            'education': 'Среднее специальное',
            'skills': 'Безопасное вождение, Знание маршрутов',
            'achievements': 'Безаварийный стаж 5 лет',
        },
        {
            'id': 3,
            'first_name': 'Айдана',
            'last_name': 'Узакова',
            'role': 'LOGIST',
            'phone': '+77012345009',
            'position': 'Логист',
            'date_joined': '2023-03-10T11:00:00Z',
            'photo': 'employee_photos/aidana.png',
            'about_me': 'Специалист по оптимизации логистических процессов.',
            'experience': '5 лет',
            'education': 'Логистика',
            'skills': 'Планирование маршрутов, Управление запасами',
            'achievements': 'Сокращение затрат на 15%',
        },
        {
            'id': 4,
            'first_name': 'Муратжан',
            'last_name': 'Илахунов',
            'role': 'CONSULTANT',
            'phone': '+77012345008',
            'position': 'Консультант',
            'date_joined': '2023-04-01T14:00:00Z',
            'photo': 'employee_photos/muratjan.png',
            'about_me': 'Эксперт в области транспортного права и международных перевозок.',
            'experience': '12 лет',
            'education': 'Юриспруденция',
            'skills': 'Юридическая поддержка, Консультирование',
            'achievements': 'Успешное разрешение сложных кейсов',
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
            'about_me': 'Эффективный менеджер по работе с клиентами и партнерами.',
            'experience': '7 лет',
            'education': 'Экономика',
            'skills': 'Переговоры, Продажи',
            'achievements': 'Расширение клиентской базы',
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
            'about_me': 'Точный и ответственный бухгалтер, следящий за финансовой отчетностью.',
            'experience': '6 лет',
            'education': 'Бухгалтерский учет',
            'skills': 'Финансовый анализ, Налоговое планирование',
            'achievements': 'Успешное прохождение аудитов',
        },
        {
            'id': 7,
            'first_name': 'Ержан',
            'last_name': 'Сапаров',
            'role': 'DRIVER',
            'phone': '+77012345005',
            'position': 'Водитель',
            'date_joined': '2023-07-01T12:00:00Z',
            'photo': 'employee_photos/7.png', # Оставляем как есть
            'about_me': 'Опытный водитель-экспедитор, ответственный и пунктуальный.',
            'experience': '9 лет',
            'education': 'Среднее',
            'skills': 'Доставка грузов, Работа с документами',
            'achievements': 'Положительные отзывы клиентов',
        },
        {
            'id': 8,
            'first_name': 'Айгуль',
            'last_name': 'Байжанова',
            'role': 'DRIVER',
            'phone': '+77012345006',
            'position': 'Водитель',
            'date_joined': '2023-08-15T09:00:00Z',
            'photo': 'employee_photos/8.png', # Оставляем как есть
            'about_me': 'Молодая и энергичная водитель, готовая к любым задачам.',
            'experience': '3 года',
            'education': 'Среднее',
            'skills': 'Быстрая адаптация, Ответственность',
            'achievements': 'Успешное прохождение обучения',
        },
        {
            'id': 9,
            'first_name': 'Марат',
            'last_name': 'Тулегенов',
            'role': 'DRIVER',
            'phone': '+77012345007',
            'position': 'Водитель',
            'date_joined': '2023-09-01T10:00:00Z',
            'photo': 'employee_photos/9.png', # Оставляем как есть
            'about_me': 'Надежный водитель с опытом работы на дальних маршрутах.',
            'experience': '6 лет',
            'education': 'Среднее',
            'skills': 'Аккуратное вождение, Техническое обслуживание',
            'achievements': 'Отсутствие штрафов',
        },
        {
            'id': 10,
            'first_name': 'Жанар',
            'last_name': 'Калиева',
            'role': 'DRIVER',
            'phone': '+77012345010',
            'position': 'Водитель',
            'date_joined': '2023-10-01T11:00:00Z',
            'photo': 'employee_photos/364534896_313106267855822_2439338549827965295_n.jpg', # Оставляем как есть
            'about_me': 'Опытный водитель с безупречной репутацией.',
            'experience': '8 лет',
            'education': 'Среднее',
            'skills': 'Международные перевозки, Знание языков',
            'achievements': 'Более 500,000 км без аварий',
        },
        {
            'id': 11,
            'first_name': 'Асылбек',
            'last_name': '',
            'role': 'DRIVER',
            'phone': '',
            'position': 'Водитель',
            'date_joined': '2023-11-01T10:00:00Z',
            'photo': '', # Нет фото
            'about_me': '',
            'experience': '',
            'education': '',
            'skills': '',
            'achievements': '',
        },
        {
            'id': 12,
            'first_name': 'Айдана',
            'last_name': 'Узакова',
            'role': 'LOGIST',
            'phone': '',
            'position': 'Логист',
            'date_joined': '2023-12-01T11:00:00Z',
            'photo': '', # Нет фото
            'about_me': '',
            'experience': '',
            'education': '',
            'skills': '',
            'achievements': '',
        },
        {
            'id': 13,
            'first_name': 'Муратжан',
            'last_name': 'Илахунов',
            'role': 'CONSULTANT',
            'phone': '',
            'position': 'Консультант',
            'date_joined': '2024-01-01T12:00:00Z',
            'photo': '', # Нет фото
            'about_me': '',
            'experience': '',
            'education': '',
            'skills': '',
            'achievements': '',
        },
        {
            'id': 14,
            'first_name': 'Асет',
            'last_name': 'Ильямов',
            'role': 'TECH',
            'phone': '',
            'position': 'Техник',
            'date_joined': '2024-02-01T10:00:00Z',
            'photo': 'employee_photos/aset.png',
            'about_me': 'Квалифицированный техник по обслуживанию транспортных средств.',
            'experience': '4 года',
            'education': 'Техническое',
            'skills': 'Диагностика, Ремонт, Обслуживание',
            'achievements': 'Снижение простоев техники на 30%',
        },
        {
            'id': 15,
            'first_name': 'Габит',
            'last_name': 'Ахметов',
            'role': 'SUPPLIER',
            'phone': '',
            'position': 'Поставщик',
            'date_joined': '2024-03-01T11:00:00Z',
            'photo': 'employee_photos/gabit.png',
            'about_me': 'Надежный поставщик с обширной сетью контактов.',
            'experience': '5 лет',
            'education': 'Высшее',
            'skills': 'Поставки, Переговоры, Логистика',
            'achievements': 'Оптимизация поставок',
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
    
    print(f"\n✅ Обновление данных завершено!")

if __name__ == '__main__':
    try:
        update_employee_data()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 