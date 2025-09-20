#!/usr/bin/env python3
"""
Создание тестового заезда для проверки страницы деталей
"""

import os
import sys
import django

# Настройка Django
sys.path.append('/Users/almaty/cursors/maro')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from core.models import Trip
from logistics.models import Vehicle
from accounts.models import User
from datetime import datetime, timedelta

def create_test_trip():
    """Создание тестового заезда с GPS данными"""
    
    try:
        # Получаем грузовик 484 ATL 01
        vehicle = Vehicle.objects.get(number='484 ATL 01')
        print(f"✅ Найден грузовик: {vehicle.number}")
        
        # Получаем водителя
        driver = User.objects.filter(role='DRIVER').first()
        if not driver:
            print("❌ Водитель не найден")
            return None
        
        print(f"✅ Найден водитель: {driver.get_full_name()}")
        
        # Создаем тестовый заезд
        trip = Trip.objects.create(
            title='Тестовый заезд с GPS',
            status='ACTIVE',
            vehicle=vehicle,
            driver=driver,
            start_address='Алматы, Казахстан',
            end_address='Астана, Казахстан',
            start_latitude=43.2220,
            start_longitude=76.8512,
            end_latitude=51.1694,
            end_longitude=71.4491,
            cargo_description='Тестовый груз',
            cargo_weight=1500.0,
            freight_amount=50000.0,
            planned_start_date=datetime.now(),
            planned_end_date=datetime.now() + timedelta(days=1),
            notes='Тестовый заезд для проверки GPS интеграции'
        )
        
        print(f"✅ Создан тестовый заезд: {trip.id}")
        print(f"   - Статус: {trip.status}")
        print(f"   - Транспорт: {trip.vehicle.number}")
        print(f"   - Водитель: {trip.driver.get_full_name()}")
        print(f"   - Маршрут: {trip.start_address} → {trip.end_address}")
        print(f"   - GPS координаты транспорта: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
        
        return trip
        
    except Vehicle.DoesNotExist:
        print("❌ Грузовик 484 ATL 01 не найден")
        return None
    except Exception as e:
        print(f"❌ Ошибка создания заезда: {e}")
        return None

def main():
    print("🚀 Создание тестового заезда для проверки GPS интеграции")
    print("=" * 60)
    
    trip = create_test_trip()
    
    if trip:
        print(f"\n🎉 Тестовый заезд создан успешно!")
        print(f"📱 URL для просмотра: http://localhost:8000/trips/{trip.id}/")
        print(f"🔗 API URL: http://localhost:8000/api/trips/{trip.id}/")
    else:
        print("\n❌ Не удалось создать тестовый заезд")

if __name__ == "__main__":
    main()

Создание тестового заезда для проверки страницы деталей
"""

import os
import sys
import django

# Настройка Django
sys.path.append('/Users/almaty/cursors/maro')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from core.models import Trip
from logistics.models import Vehicle
from accounts.models import User
from datetime import datetime, timedelta

def create_test_trip():
    """Создание тестового заезда с GPS данными"""
    
    try:
        # Получаем грузовик 484 ATL 01
        vehicle = Vehicle.objects.get(number='484 ATL 01')
        print(f"✅ Найден грузовик: {vehicle.number}")
        
        # Получаем водителя
        driver = User.objects.filter(role='DRIVER').first()
        if not driver:
            print("❌ Водитель не найден")
            return None
        
        print(f"✅ Найден водитель: {driver.get_full_name()}")
        
        # Создаем тестовый заезд
        trip = Trip.objects.create(
            title='Тестовый заезд с GPS',
            status='ACTIVE',
            vehicle=vehicle,
            driver=driver,
            start_address='Алматы, Казахстан',
            end_address='Астана, Казахстан',
            start_latitude=43.2220,
            start_longitude=76.8512,
            end_latitude=51.1694,
            end_longitude=71.4491,
            cargo_description='Тестовый груз',
            cargo_weight=1500.0,
            freight_amount=50000.0,
            planned_start_date=datetime.now(),
            planned_end_date=datetime.now() + timedelta(days=1),
            notes='Тестовый заезд для проверки GPS интеграции'
        )
        
        print(f"✅ Создан тестовый заезд: {trip.id}")
        print(f"   - Статус: {trip.status}")
        print(f"   - Транспорт: {trip.vehicle.number}")
        print(f"   - Водитель: {trip.driver.get_full_name()}")
        print(f"   - Маршрут: {trip.start_address} → {trip.end_address}")
        print(f"   - GPS координаты транспорта: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
        
        return trip
        
    except Vehicle.DoesNotExist:
        print("❌ Грузовик 484 ATL 01 не найден")
        return None
    except Exception as e:
        print(f"❌ Ошибка создания заезда: {e}")
        return None

def main():
    print("🚀 Создание тестового заезда для проверки GPS интеграции")
    print("=" * 60)
    
    trip = create_test_trip()
    
    if trip:
        print(f"\n🎉 Тестовый заезд создан успешно!")
        print(f"📱 URL для просмотра: http://localhost:8000/trips/{trip.id}/")
        print(f"🔗 API URL: http://localhost:8000/api/trips/{trip.id}/")
    else:
        print("\n❌ Не удалось создать тестовый заезд")

if __name__ == "__main__":
    main()






































