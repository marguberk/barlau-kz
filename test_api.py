#!/usr/bin/env python3
"""
Скрипт для тестирования API заездов
"""

import os
import sys
import django
import requests
import json

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

def test_api():
    """Тестируем API заездов"""
    print("🔍 Тестируем API заездов...")
    
    # Тестируем локальный API
    try:
        response = requests.get('http://127.0.0.1:8001/api/trips/')
        print(f"📡 Локальный API статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Получено заездов: {len(data.get('results', []))}")
            
            # Показываем ID заездов
            trips = data.get('results', [])
            if trips:
                active_ids = [str(t['id']) for t in trips if t.get('status') in ['ACTIVE', 'PLANNED']]
                print(f"🎯 WEB ACTIVE TRIPS IDS: {', '.join(active_ids)}")
                
                # Показываем детали первых 3 заездов
                for i, trip in enumerate(trips[:3]):
                    print(f"\n🚛 Заезд {i+1}:")
                    print(f"   ID: {trip.get('id')}")
                    print(f"   Статус: {trip.get('status')}")
                    print(f"   Маршрут: {trip.get('start_address', 'N/A')} → {trip.get('end_address', 'N/A')}")
                    print(f"   Грузовик: {trip.get('vehicle_details', {}).get('number', 'N/A') if trip.get('vehicle_details') else 'N/A'}")
                    print(f"   Водитель: {trip.get('driver_details', {}).get('first_name', 'N/A') if trip.get('driver_details') else 'N/A'}")
        else:
            print(f"❌ Ошибка API: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")
    
    print("\n" + "="*50)
    
    # Тестируем продакшн API (для сравнения)
    try:
        response = requests.get('https://barlau.org/api/trips/', 
                              headers={'Authorization': 'Bearer demo_token_for_web'})
        print(f"📡 Продакшн API статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Получено заездов: {len(data.get('results', []))}")
            
            # Показываем ID заездов
            trips = data.get('results', [])
            if trips:
                active_ids = [str(t['id']) for t in trips if t.get('status') in ['ACTIVE', 'PLANNED']]
                print(f"🎯 FLUTTER ACTIVE TRIPS IDS: {', '.join(active_ids)}")
        else:
            print(f"❌ Ошибка продакшн API: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка подключения к продакшн API: {e}")

if __name__ == '__main__':
    test_api() 