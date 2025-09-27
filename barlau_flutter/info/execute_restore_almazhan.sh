#!/bin/bash

# Скрипт для восстановления сотрудника Алмасжан Сопашев на продакшн сервере

echo "🔄 Восстанавливаем сотрудника Алмасжан Сопашев..."

# Подключаемся к серверу и выполняем скрипт
sshpass -p '33q97KKRfmnHTY6dCiyuA3g=' ssh ubuntu@85.202.192.33 << 'EOF'

cd /var/www/barlau
source venv/bin/activate

# Выполняем Python скрипт для восстановления сотрудника
python3 -c "
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from accounts.models import User
from django.db import transaction

def restore_almazhan():
    with transaction.atomic():
        try:
            # Данные из employees.txt
            first_name = 'Алмасжан'
            last_name = 'Сопашев'
            username = '+77057057876'
            email = 'almazhan.sopashev@barlau.kz'
            birth_date = '1988-12-24'
            iin = '881224302564'
            
            about_me = '''Родился 24 декабря 1988 года в г.Жаркент.
Семейное положение-Женат.Окончил Международный университет «Silkway»'''
            
            # Проверяем, не существует ли уже такой сотрудник
            existing = User.objects.filter(
                username=username,
                first_name=first_name,
                last_name=last_name
            ).first()
            
            if existing:
                print(f'❌ Сотрудник {first_name} {last_name} уже существует (ID: {existing.id})')
                return False
            
            # Создаем нового сотрудника
            employee = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role='driver',
                position='Водитель',
                about_me=about_me,
                birth_date=birth_date,
                iin=iin,
                is_active=True,
                is_staff=False,
                is_superuser=False
            )
            
            # Устанавливаем пароль
            employee.set_password('barlau2025')
            employee.save()
            
            print(f'✅ Сотрудник {first_name} {last_name} успешно создан!')
            print(f'   ID: {employee.id}')
            print(f'   Телефон: {employee.username}')
            print(f'   Email: {employee.email}')
            print(f'   Роль: {employee.role}')
            print(f'   Должность: {employee.position}')
            print(f'   Дата рождения: {employee.birth_date}')
            print(f'   ИИН: {employee.iin}')
            
            return True
            
        except Exception as e:
            print(f'❌ Ошибка при создании сотрудника: {e}')
            return False

print('🔄 Восстановление сотрудника Алмасжан Сопашев...')
success = restore_almazhan()

if success:
    print('✅ Восстановление завершено успешно!')
else:
    print('❌ Ошибка при восстановлении сотрудника!')
    sys.exit(1)
"

EOF

echo "✅ Скрипт выполнен!"


