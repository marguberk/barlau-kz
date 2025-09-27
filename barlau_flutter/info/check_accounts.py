#!/usr/bin/env python3
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

print('🔍 ПРОВЕРКА АККАУНТОВ ПОЛЬЗОВАТЕЛЕЙ ===')
print()

test_users = User.objects.filter(username__contains='+').exclude(username='admin')[:10]

for user in test_users:
    print(f'👤 {user.first_name} {user.last_name}:')
    print(f'   Email: {user.email if user.email else "НЕТ"}')
    print(f'   Phone: {user.phone if user.phone else "НЕТ"}')
    print(f'   Position: {user.position if user.position else "НЕТ"}')
    print(f'   Role: {user.role}')
    print(f'   Photo: {"есть" if user.photo else "нет"}')
    print()

print('=== ПРОВЕРКА АВТОРИЗАЦИИ ===')

successful = 0
failed = 0

for user in test_users:
    username = user.username
    password = 'barlau2025'
    
    print(f'🔄 {user.first_name} {user.last_name}: {username}')
    
    auth_user = authenticate(username=username, password=password)
    
    if auth_user:
        print(f'   ✅ Вход успешен')
        successful += 1
    else:
        print(f'   ❌ Ошибка входа')
        failed += 1
    
    print()

print(f'📊 ИТОГИ:')
print(f'   ✅ Успешных входов: {successful}')
print(f'   ❌ Ошибок входа: {failed}')

print()
print('=== ПРОВЕРКА ПРОБЛЕМ ===')

users_without_email = User.objects.filter(email='').exclude(username='admin')
print(f'Пользователей без email: {users_without_email.count()}')

users_without_phone = User.objects.filter(phone='').exclude(username='admin')
print(f'Пользователей без phone: {users_without_phone.count()}')

users_without_position = User.objects.filter(position='').exclude(username='admin')
print(f'Пользователей без position: {users_without_position.count()}')

print()
print('=== PHONE vs USERNAME ===')
for user in test_users[:5]:
    phone = user.phone
    username = user.username
    print(f'{user.first_name} {user.last_name}:')
    print(f'   phone: {phone}')
    print(f'   username: {username}')
    print(f'   match: {phone == username}')
    print()


