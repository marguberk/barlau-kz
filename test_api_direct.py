#!/usr/bin/env python3
import os
import sys
import django

# Настройка Django
sys.path.append('/Users/almaty/cursors/maro')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from logistics.api import vehicles_locations
from logistics.models import Vehicle
from accounts.models import User

def test_api_direct():
    """Прямое тестирование API функции"""
    print("🧪 Прямое тестирование API")
    print("=" * 50)
    
    # Создаем запрос
    factory = APIRequestFactory()
    request = factory.get('/api/vehicles/locations/')
    
    # Получаем пользователя
    user = User.objects.filter(role='SUPERADMIN').first()
    if not user:
        print("❌ Не найден пользователь SUPERADMIN")
        return
    
    request.user = user
    print(f"✅ Пользователь: {user.username} ({user.role})")
    
    # Проверяем данные в базе
    vehicles = Vehicle.objects.filter(
        gps_enabled=True,
        gps_latitude__isnull=False,
        gps_longitude__isnull=False
    )
    print(f"📊 Грузовиков в базе: {vehicles.count()}")
    
    for vehicle in vehicles:
        print(f"  🚛 {vehicle.number}: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
    
    # Тестируем API
    try:
        response = vehicles_locations(request)
        print(f"\n🌐 API Response:")
        print(f"  Status: {response.status_code}")
        print(f"  Data: {response.data}")
        
        if response.status_code == 200:
            print(f"✅ API работает! Получено {len(response.data)} грузовиков")
        else:
            print(f"❌ API вернул ошибку: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка API: {e}")
        import traceback
        traceback.print_exc()

def test_url_routing():
    """Тестирование URL routing"""
    print(f"\n🔗 Тестирование URL routing")
    print("=" * 50)
    
    from django.urls import reverse, resolve
    from django.test import Client
    
    try:
        # Тестируем с Django test client
        client = Client()
        
        # Получаем токен
        user = User.objects.filter(role='SUPERADMIN').first()
        if user:
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            
            # Тестируем endpoint
            response = client.get(
                '/api/vehicles/locations/',
                HTTP_AUTHORIZATION=f'Bearer {token}'
            )
            
            print(f"📡 HTTP Response:")
            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {response.get('Content-Type')}")
            print(f"  Data: {response.content.decode()[:200]}...")
            
    except Exception as e:
        print(f"❌ Ошибка URL routing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_direct()
    test_url_routing()
