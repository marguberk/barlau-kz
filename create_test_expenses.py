#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from logistics.models import Expense, Vehicle
from accounts.models import User

def create_test_expenses():
    print("=== Создание тестовых данных расходов ===")
    
    # Получаем транспортные средства
    vehicles = list(Vehicle.objects.all())
    if not vehicles:
        print("❌ Нет транспортных средств в базе")
        return
    
    # Получаем пользователей
    users = list(User.objects.filter(is_active=True))
    if not users:
        print("❌ Нет активных пользователей в базе")
        return
    
    # Категории расходов
    categories = ['FUEL', 'MAINTENANCE', 'REPAIR', 'OTHER']
    
    # Создаем тестовые расходы
    for i in range(10):
        expense = Expense.objects.create(
            category=random.choice(categories),
            vehicle=random.choice(vehicles),
            amount=random.randint(1000, 50000),
            date=datetime.now().date() - timedelta(days=random.randint(0, 30)),
            description=f"Тестовый расход #{i+1} - {random.choice(['Заправка', 'Ремонт двигателя', 'Замена масла', 'Покупка запчастей', 'Мойка'])}",
            created_by=random.choice(users)
        )
        print(f"✅ Создан расход: {expense.category} - {expense.amount} ₸ - {expense.description}")
    
    print(f"\n✅ Создано {Expense.objects.count()} расходов")

if __name__ == "__main__":
    create_test_expenses() 