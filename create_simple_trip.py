#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timezone

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from core.models import Trip
from logistics.models import Vehicle
from accounts.models import User

def create_simple_trip():
    """Создать простой заезд в базе данных"""
    try:
        # Получаем первый доступный грузовик и водителя
        vehicle = Vehicle.objects.first()
        driver = User.objects.filter(role='DRIVER').first()
        
        if not vehicle:
            print("❌ Нет доступных грузовиков")
            return False
            
        if not driver:
            print("❌ Нет доступных водителей")
            return False
        
        # Создаем заезд
        trip = Trip.objects.create(
            title='Тестовый заезд',
            status='PLANNED',
            vehicle=vehicle,
            driver=driver,
            start_address='Астана',
            end_address='Алматы',
            planned_start_date=datetime.now(timezone.utc),
            planned_end_date=datetime.now(timezone.utc),
            notes='Создан через простой скрипт'
        )
        
        print(f"✅ Заезд создан успешно!")
        print(f"   ID: {trip.id}")
        print(f"   Название: {trip.title}")
        print(f"   Статус: {trip.status}")
        print(f"   Грузовик: {trip.vehicle}")
        print(f"   Водитель: {trip.driver}")
        print(f"   Всего заездов: {Trip.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания заезда: {e}")
        return False

if __name__ == '__main__':
    create_simple_trip() 
 