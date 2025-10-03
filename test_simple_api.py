#!/usr/bin/env python3
import os
import sys
import django

# Настройка Django
sys.path.append('/Users/almaty/cursors/maro')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle
from accounts.models import User

def test_simple():
    """Простой тест GPS данных"""
    print("🧪 Простой тест GPS данных")
    print("=" * 50)
    
    # Проверяем данные в базе
    vehicles = Vehicle.objects.filter(
        gps_enabled=True,
        gps_latitude__isnull=False,
        gps_longitude__isnull=False
    )
    
    print(f"📊 Грузовиков с GPS: {vehicles.count()}")
    
    for vehicle in vehicles:
        print(f"🚛 {vehicle.number}: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
    
    # Проверяем пользователей
    users = User.objects.all()
    print(f"\n👤 Пользователей в системе: {users.count()}")
    
    for user in users:
        print(f"  {user.username} ({user.role})")

if __name__ == "__main__":
    test_simple()


