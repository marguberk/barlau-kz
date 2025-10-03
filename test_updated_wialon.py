#!/usr/bin/env python3
"""
Тестирование обновленного Wialon сервиса с правильными флагами
"""
import os
import django
from datetime import datetime
from django.utils import timezone

# Настройка Django для продакшн
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle
from logistics.services.wialon_service import WialonService

def test_updated_wialon():
    """Тестируем обновленный Wialon сервис"""
    print("🧪 ТЕСТИРОВАНИЕ ОБНОВЛЕННОГО WIALON СЕРВИСА")
    print("=" * 60)
    
    try:
        wialon_service = WialonService()
        
        # Тестируем все четыре грузовика
        target_vehicles = [
            {"number": "484ATL01", "wialon_name": "484 ATL 01"},
            {"number": "355ATL01", "wialon_name": "355 ATL 01"},
            {"number": "359AUL01", "wialon_name": "359 AUL 01"},
            {"number": "695BHS02", "wialon_name": "695 BHS 02"}
        ]
        
        for vehicle_info in target_vehicles:
            print(f"\n🚛 Тестируем {vehicle_info['number']} ({vehicle_info['wialon_name']})")
            
            try:
                # Находим грузовик в базе
                vehicle = Vehicle.objects.filter(number=vehicle_info['number']).first()
                if not vehicle:
                    print(f"   ❌ Грузовик {vehicle_info['number']} не найден в базе")
                    continue
                
                print(f"   📋 Грузовик найден: GPS включен={vehicle.gps_enabled}, device_id={vehicle.gps_device_id}")
                
                # Пытаемся обновить GPS данные
                print(f"   🔄 Обновляем GPS данные...")
                success = wialon_service.update_vehicle_gps_data(vehicle)
                
                if success:
                    # Получаем обновленные данные
                    vehicle.refresh_from_db()
                    print(f"   ✅ Успешно обновлено:")
                    print(f"      📍 Координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
                    print(f"      🚗 Скорость: {vehicle.gps_speed} км/ч")
                    print(f"      🧭 Направление: {vehicle.gps_heading}°")
                    print(f"      📡 Спутники: {vehicle.gps_satellites}")
                    print(f"      ⏰ Последнее обновление: {vehicle.gps_last_update}")
                else:
                    print(f"   ❌ Не удалось обновить GPS данные")
                
            except Exception as e:
                print(f"   ❌ Ошибка для {vehicle_info['number']}: {e}")
        
        # Проверяем финальное состояние всех грузовиков
        print(f"\n📊 ФИНАЛЬНОЕ СОСТОЯНИЕ ВСЕХ ГРУЗОВИКОВ:")
        for vehicle_info in target_vehicles:
            try:
                vehicle = Vehicle.objects.filter(number=vehicle_info['number']).first()
                if vehicle and vehicle.gps_enabled:
                    print(f"   {vehicle_info['number']}: {vehicle.gps_latitude}, {vehicle.gps_longitude} (обновлено: {vehicle.gps_last_update.strftime('%H:%M:%S') if vehicle.gps_last_update else 'N/A'})")
                else:
                    print(f"   {vehicle_info['number']}: GPS отключен или не найден")
            except Exception as e:
                print(f"   {vehicle_info['number']}: Ошибка - {e}")
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")

if __name__ == "__main__":
    test_updated_wialon()


