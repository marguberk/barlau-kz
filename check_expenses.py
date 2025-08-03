#!/usr/bin/env python3
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from logistics.models import Expense
from accounts.models import User

def check_expenses():
    print("=== Проверка данных расходов ===")
    
    # Проверяем количество расходов
    expenses_count = Expense.objects.count()
    print(f"Всего расходов в базе: {expenses_count}")
    
    if expenses_count > 0:
        print("\nПоследние 5 расходов:")
        for expense in Expense.objects.all()[:5]:
            print(f"- {expense.date}: {expense.category} - {expense.amount} тенге - {expense.description}")
    
    # Проверяем пользователей
    users_count = User.objects.filter(is_active=True).count()
    print(f"\nАктивных пользователей: {users_count}")
    
    if users_count > 0:
        print("\nПользователи:")
        for user in User.objects.filter(is_active=True)[:5]:
            print(f"- {user.first_name} {user.last_name} ({user.username}) - {user.role}")

if __name__ == "__main__":
    check_expenses() 