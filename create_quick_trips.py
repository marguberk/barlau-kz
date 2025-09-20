#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from core.models import Trip, Vehicle, User
from django.utils import timezone

def create_test_trips():
    print("🚀 Создаю тестовые заезды...")
    
    # Получаем существующие машины
    vehicles = Vehicle.objects.all()
    if not vehicles.exists():
        print("❌ Нет доступных машин!")
        return
    
    # Получаем пользователя admin
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("❌ Пользователь admin не найден!")
        return
    
    now = timezone.now()
    
    # 1. Активный заезд
    active_trip = Trip.objects.create(
        title="Алматы → Астана",
        start_address="Алматы, ул. Достык, 123",
        end_address="Астана, ул. Республики, 456",
        start_date=now - timedelta(hours=2),
        planned_end_date=now + timedelta(hours=4),
        status='active',
        freight=50000,
        vehicle=vehicles.first(),
        driver=admin_user,
        created_by=admin_user
    )
    print(f"✅ Создан активный заезд: {active_trip.title}")
    
    # 2. Планируемый заезд
    planned_trip = Trip.objects.create(
        title="Астана → Шымкент",
        start_address="Астана, ул. Республики, 456",
        end_address="Шымкент, ул. Тауке хана, 789",
        start_date=now + timedelta(days=1),
        planned_end_date=now + timedelta(days=1, hours=6),
        status='planned',
        freight=75000,
        vehicle=vehicles.first(),
        driver=admin_user,
        created_by=admin_user
    )
    print(f"✅ Создан планируемый заезд: {planned_trip.title}")
    
    # 3. Завершенный заезд
    completed_trip = Trip.objects.create(
        title="Шымкент → Алматы",
        start_address="Шымкент, ул. Тауке хана, 789",
        end_address="Алматы, ул. Достык, 123",
        start_date=now - timedelta(days=2),
        end_date=now - timedelta(days=1),
        planned_end_date=now - timedelta(days=1),
        status='completed',
        freight=60000,
        vehicle=vehicles.first(),
        driver=admin_user,
        created_by=admin_user
    )
    print(f"✅ Создан завершенный заезд: {completed_trip.title}")
    
    print(f"\n🎉 Создано 3 заезда!")
    print(f"📊 Всего заездов в базе: {Trip.objects.count()}")

if __name__ == '__main__':
    create_test_trips()

