#!/bin/bash

# Скрипт для создания аккаунтов всех сотрудников и водителей на продакшн сервере

echo "🔄 Создаем аккаунты для всех сотрудников и водителей..."

# Подключаемся к серверу и выполняем скрипт
sshpass -p '33q97KKRfmnHTY6dCiyuA3g=' ssh ubuntu@85.202.192.33 << 'EOF'

cd /var/www/barlau
source venv/bin/activate

# Выполняем Python скрипт для создания аккаунтов
python3 -c "
import os
import sys
import django
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from accounts.models import User
from django.db import transaction

def calculate_age(birth_date_str):
    try:
        birth_date = datetime.strptime(birth_date_str, '%d.%m.%Y')
        today = datetime.now()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age
    except:
        return None

def create_employee_accounts():
    # Данные сотрудников из файла
    employees_data = [
        {
            'name': 'Айдарбеков Серік Шайдолдаұлы',
            'first_name': 'Серік',
            'last_name': 'Айдарбеков',
            'phone': '+77757599686',
            'birth_date': '01.06.1986',
            'about_me': 'Родился 1 июня 1986 года. ИИН: 890601301168',
            'role': 'driver'
        },
        {
            'name': 'Молдияров Аскар Ахатович',
            'first_name': 'Аскар',
            'last_name': 'Молдияров',
            'phone': '+77758881220',
            'birth_date': '20.12.1988',
            'about_me': 'Родился 20 декабря 1988 года в г. Караганда. Семейное положение-Женат.Окончил Российский Университет Дружбы Народов, г.Москва. ИИН: 881220350265',
            'role': 'employee'
        },
        {
            'name': 'Беркинбаев Мейрлан Камалбекұлы',
            'first_name': 'Мейрлан',
            'last_name': 'Беркинбаев',
            'phone': '+77000000000',
            'birth_date': None,
            'about_me': 'Сотрудник компании BARLAU Truck Logistics',
            'role': 'employee'
        },
        {
            'name': 'Құсайын Мақсат Ермекұлы',
            'first_name': 'Мақсат',
            'last_name': 'Құсайын',
            'phone': '+77014977888',
            'birth_date': '16.05.1988',
            'about_me': 'Родился 16 мая 1988 года в г.Жаркент. Семейное положение-Женат. ИИН: 880516300512',
            'role': 'driver'
        },
        {
            'name': 'Кудайбергенов Ерболат Чингизович',
            'first_name': 'Ерболат',
            'last_name': 'Кудайбергенов',
            'phone': '+77017525437',
            'birth_date': '25.02.1978',
            'about_me': 'Родился 25 февраля 1978 года с.Елтай,Ерейментауский р-он,Акмолинская область. ИИН: 780225350070',
            'role': 'driver'
        },
        {
            'name': 'Садвакасова Назерке Касымхановна',
            'first_name': 'Назерке',
            'last_name': 'Садвакасова',
            'phone': '+77023200506',
            'birth_date': '01.08.1992',
            'about_me': 'Родилась 01 августа 1992 года в г.Жаркент. Семейное положение-Замужем.Окончила КазНУ',
            'role': 'employee'
        },
        {
            'name': 'Ахметов Ғабит Сәбитұлы',
            'first_name': 'Ғабит',
            'last_name': 'Ахметов',
            'phone': '+77071778202',
            'birth_date': '13.12.1990',
            'about_me': 'Родился 13 декабря 1990 года в г.Жаркент. Семейное положение-Холостой. ИИН: 901213302223',
            'role': 'driver'
        },
        {
            'name': 'Илямов Азиз Алымжанұлы',
            'first_name': 'Азиз',
            'last_name': 'Илямов',
            'phone': '+77789509264',
            'birth_date': '22.10.1995',
            'about_me': 'Родился 22 октября 1995 года в г.Жаркент. Семейное положение-Женат. ИИН: 951022300812',
            'role': 'driver'
        },
        {
            'name': 'Ұзақ Айдана Ербосынқызы',
            'first_name': 'Айдана',
            'last_name': 'Ұзақ',
            'phone': '+77076156475',
            'birth_date': '01.02.1998',
            'about_me': 'Родилась 01 февраля 1998 года в г.Жаркент. 2020 году окончила АТУ,по специальности-технология. Семейное положение-Замужем.Дети-1. ИИН: 980201400864',
            'role': 'employee'
        },
        {
            'name': 'Мұрат Асель Мұратқызы',
            'first_name': 'Асель',
            'last_name': 'Мұрат',
            'phone': '+77781008373',
            'birth_date': '19.09.1995',
            'about_me': 'Родилась 19 сентября 1995 года в г.Жаркент.Образование-незаконченное высшее. Семейное положение-в разводе.Дети-1. ИИН: 950919401325',
            'role': 'employee'
        }
    ]
    
    # Данные водителей из файла
    drivers_data = [
        {
            'name': 'Касимов Сухрат Алимжанович',
            'first_name': 'Сухрат',
            'last_name': 'Касимов',
            'phone': '+77775251777',
            'birth_date': '01.10.2001',
            'about_me': 'Родился 1 октября 2001 года. Водительское удостоверение: 011001500617',
            'role': 'driver'
        },
        {
            'name': 'Қасенов Хезиз Ибраимұлы',
            'first_name': 'Хезиз',
            'last_name': 'Қасенов',
            'phone': '+77015843537',
            'birth_date': '20.07.1990',
            'about_me': 'Родился 20 июля 1990 года. Водительское удостоверение: 900720302326',
            'role': 'driver'
        },
        {
            'name': 'Сабит Ғабит Нұрғалиұлы',
            'first_name': 'Ғабит',
            'last_name': 'Сабит',
            'phone': '+77479499219',
            'birth_date': '20.09.1999',
            'about_me': 'Родился 20 сентября 1999 года. Водительское удостоверение: 990920300224',
            'role': 'driver'
        },
        {
            'name': 'Садыров Рустем Шаукетович',
            'first_name': 'Рустем',
            'last_name': 'Садыров',
            'phone': '+77054029789',
            'birth_date': '15.10.1985',
            'about_me': 'Родился 15 октября 1985 года. Водительское удостоверение: 851015303223',
            'role': 'driver'
        },
        {
            'name': 'Пида Хамражан Магаметжанович',
            'first_name': 'Хамражан',
            'last_name': 'Пида',
            'phone': '+77471676916',
            'birth_date': '03.08.1994',
            'about_me': 'Родился 3 августа 1994 года. Водительское удостоверение: 940803300734',
            'role': 'driver'
        },
        {
            'name': 'Камердинов Азизжан Якупжанович',
            'first_name': 'Азизжан',
            'last_name': 'Камердинов',
            'phone': '+77477020048',
            'birth_date': '26.10.1990',
            'about_me': 'Родился 26 октября 1990 года. Водительское удостоверение: 901026301546',
            'role': 'driver'
        },
        {
            'name': 'Рузиев Сраилжан Смаилович',
            'first_name': 'Сраилжан',
            'last_name': 'Рузиев',
            'phone': '+77025432163',
            'birth_date': '21.08.1990',
            'about_me': 'Родился 21 августа 1990 года. Водительское удостоверение: 900821301208',
            'role': 'driver'
        },
        {
            'name': 'Саит Абдулжан Адилович',
            'first_name': 'Абдулжан',
            'last_name': 'Саит',
            'phone': '+77714592745',
            'birth_date': '16.01.1995',
            'about_me': 'Родился 16 января 1995 года. Водительское удостоверение: 950116300573',
            'role': 'driver'
        },
        {
            'name': 'Абдуллаев Хамит Рахемжанович',
            'first_name': 'Хамит',
            'last_name': 'Абдуллаев',
            'phone': '+77472506006',
            'birth_date': '27.04.1993',
            'about_me': 'Родился 27 апреля 1993 года. Водительское удостоверение: 930427301112',
            'role': 'driver'
        },
        {
            'name': 'Муталипов Марат Хасанович',
            'first_name': 'Марат',
            'last_name': 'Муталипов',
            'phone': '+77761605888',
            'birth_date': '28.01.1988',
            'about_me': 'Родился 28 января 1988 года. Водительское удостоверение: 880128302163',
            'role': 'driver'
        },
        {
            'name': 'Исмаилов Розахун Рахимжанович',
            'first_name': 'Розахун',
            'last_name': 'Исмаилов',
            'phone': '+77777242458',
            'birth_date': '10.01.1997',
            'about_me': 'Родился 10 января 1997 года. Водительское удостоверение: 970110300425',
            'role': 'driver'
        },
        {
            'name': 'Касымов Шахмурат Дильмуратович',
            'first_name': 'Шахмурат',
            'last_name': 'Касымов',
            'phone': '+77079114708',
            'birth_date': '28.08.1983',
            'about_me': 'Родился 28 августа 1983 года. Водительское удостоверение: 830828300014',
            'role': 'driver'
        },
        {
            'name': 'Кудайбергенов Жасулан Берикович',
            'first_name': 'Жасулан',
            'last_name': 'Кудайбергенов',
            'phone': '+77052224788',
            'birth_date': '04.12.1988',
            'about_me': 'Родился 4 декабря 1988 года. Водительское удостоверение: 881204301349',
            'role': 'driver'
        },
        {
            'name': 'Умурбеков Елдос Болатханович',
            'first_name': 'Елдос',
            'last_name': 'Умурбеков',
            'phone': '+77759922900',
            'birth_date': '05.04.1991',
            'about_me': 'Родился 5 апреля 1991 года. Водительское удостоверение: 910405301367',
            'role': 'driver'
        }
    ]
    
    # Объединяем всех сотрудников и водителей (исключаем Алмасжана Сопашева, так как он уже создан)
    all_people = [emp for emp in employees_data if emp['phone'] != '+77057057876'] + drivers_data
    
    created_count = 0
    skipped_count = 0
    
    with transaction.atomic():
        for person in all_people:
            try:
                # Вычисляем возраст
                age = None
                if person['birth_date']:
                    age = calculate_age(person['birth_date'])
                
                # Проверяем, существует ли уже такой пользователь
                existing = User.objects.filter(username=person['phone']).first()
                
                if existing:
                    print(f'⚠️  Пользователь {person[\"first_name\"]} {person[\"last_name\"]} уже существует (ID: {existing.id})')
                    skipped_count += 1
                    continue
                
                # Создаем нового пользователя
                user = User.objects.create(
                    username=person['phone'],
                    email=f'{person[\"first_name\"].lower()}.{person[\"last_name\"].lower()}@barlau.kz',
                    first_name=person['first_name'],
                    last_name=person['last_name'],
                    phone=person['phone'],
                    role=person['role'],
                    position='Водитель' if person['role'] == 'driver' else 'Сотрудник',
                    about_me=person['about_me'],
                    age=age,
                    location='Жаркент',
                    is_active=True,
                    is_staff=False,
                    is_superuser=False
                )
                
                # Устанавливаем пароль
                user.set_password('barlau2025')
                user.save()
                
                print(f'✅ Создан: {person[\"first_name\"]} {person[\"last_name\"]} (ID: {user.id}, Телефон: {person[\"phone\"]})')
                created_count += 1
                
            except Exception as e:
                print(f'❌ Ошибка при создании {person[\"first_name\"]} {person[\"last_name\"]}: {e}')
    
    print(f'\\n📊 ИТОГИ:')
    print(f'   ✅ Создано: {created_count}')
    print(f'   ⚠️  Пропущено (уже существуют): {skipped_count}')
    print(f'   📱 Всего обработано: {len(all_people)}')
    
    return created_count > 0

print('🔄 Создание аккаунтов для всех сотрудников и водителей...')
success = create_employee_accounts()

if success:
    print('\\n✅ Создание аккаунтов завершено успешно!')
else:
    print('\\n❌ Ошибка при создании аккаунтов!')
    sys.exit(1)
"

EOF

echo "✅ Скрипт выполнен!"


