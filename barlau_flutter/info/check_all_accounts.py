#!/usr/bin/env python3
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

print('🔍 ПРОВЕРКА ВСЕХ АККАУНТОВ ===')
print()

# Проверим всех пользователей кроме админа
all_users = User.objects.exclude(username='admin').order_by('first_name', 'last_name')
print(f'Всего пользователей: {all_users.count()}')
print()

# Сгруппируем по ролям
roles_count = {}
for user in all_users:
    role = user.role
    if role not in roles_count:
        roles_count[role] = []
    roles_count[role].append(user)

for role, users in roles_count.items():
    print(f'=== {role} ({len(users)} человек) ===')
    for user in users:
        print(f'  👤 {user.first_name} {user.last_name}')
        print(f'      Логин: {user.username}')
        print(f'      Email: {user.email}')
        print(f'      Phone: {user.phone}')
        print(f'      Position: {user.position}')
        print()

print('=== ПРОВЕРКА АВТОРИЗАЦИИ ===')

successful = 0
failed = []

for user in all_users:
    username = user.username
    password = 'barlau2025'
    
    auth_user = authenticate(username=username, password=password)
    
    if auth_user:
        successful += 1
    else:
        failed.append(f'{user.first_name} {user.last_name} ({username})')

print(f'✅ Успешных входов: {successful}')
print(f'❌ Ошибок входа: {len(failed)}')

if failed:
    print('\n🔴 СПИСОК ОШИБОК:')
    for error in failed:
        print(f'   - {error}')

print('\n=== ПРОВЕРКА ПРОБЛЕМ ===')

users_with_issues = []
for user in all_users:
    issues = []
    if not user.email:
        issues.append('нет email')
    if not user.phone:
        issues.append('нет phone')
    if not user.position:
        issues.append('нет position')
    
    if issues:
        users_with_issues.append((user, issues))

if users_with_issues:
    print('Пользователи с проблемами:')
    for user, issues in users_with_issues:
        print(f'  ❌ {user.first_name} {user.last_name}: {", ".join(issues)}')
else:
    print('✅ Все пользователи имеют полные данные')

print('\n=== ПРОВЕРКА ФОРМАТОВ ===')
print('Форматы телефонов (первые 5):')
for user in all_users[:5]:
    phone = user.phone
    username = user.username
    print(f'  {user.first_name} {user.last_name}:')
    print(f'    phone: {phone}')
    print(f'    username: {username}')
    print(f'    совпадают: {phone == username}')
    print()


