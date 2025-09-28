#!/usr/bin/env python3
"""
Простой скрипт для синхронизации GPS трекеров с продакшн сервером
"""

import subprocess
import time

def run_ssh_command(command):
    """Выполнение команды на продакшн сервере"""
    print(f"🔧 Выполнение: {command}")
    
    try:
        ssh_command = f"sshpass -p '33q97KKRfmnHTY6dCiyuA3g=' ssh -o StrictHostKeyChecking=no ubuntu@85.202.192.33 'cd /var/www/barlau && {command}'"
        
        result = subprocess.run(
            ssh_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"✅ Успешно: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Ошибка: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

def main():
    """
    Основная функция
    """
    print("🚀 Синхронизация GPS трекеров с продакшн сервером")
    print("=" * 60)
    
    # Создаем временный Python файл для выполнения на сервере
    python_script = '''
import os
import sys
import django

# Настройка Django
sys.path.append("/var/www/barlau")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maro.settings")
django.setup()

from logistics.models import Vehicle
from django.utils import timezone

# GPS данные для четырех грузовиков
vehicles_data = [
    {
        "number": "484ATL01",
        "gps_device_id": "484001",
        "gps_imei": "861234567890001",
        "gps_phone": "+77001234501",
        "gps_latitude": 43.2220,
        "gps_longitude": 76.8512,
        "gps_speed": 0.0,
        "gps_heading": 0.0,
        "gps_altitude": 785.0,
        "gps_satellites": 8,
        "gps_signal_quality": "good",
        "gps_fuel_level": 75.0,
        "gps_engine_status": False,
        "gps_ignition_status": False
    },
    {
        "number": "290ATL01", 
        "gps_device_id": "290001",
        "gps_imei": "861234567890002",
        "gps_phone": "+77001234502",
        "gps_latitude": 43.2220,
        "gps_longitude": 76.8512,
        "gps_speed": 0.0,
        "gps_heading": 0.0,
        "gps_altitude": 785.0,
        "gps_satellites": 8,
        "gps_signal_quality": "good",
        "gps_fuel_level": 75.0,
        "gps_engine_status": False,
        "gps_ignition_status": False
    },
    {
        "number": "533ATL01",
        "gps_device_id": "533001", 
        "gps_imei": "861234567890003",
        "gps_phone": "+77001234503",
        "gps_latitude": 43.2220,
        "gps_longitude": 76.8512,
        "gps_speed": 0.0,
        "gps_heading": 0.0,
        "gps_altitude": 785.0,
        "gps_satellites": 8,
        "gps_signal_quality": "good",
        "gps_fuel_level": 75.0,
        "gps_engine_status": False,
        "gps_ignition_status": False
    },
    {
        "number": "105AGR19",
        "gps_device_id": "105001",
        "gps_imei": "861234567890004", 
        "gps_phone": "+77001234504",
        "gps_latitude": 43.2220,
        "gps_longitude": 76.8512,
        "gps_speed": 0.0,
        "gps_heading": 0.0,
        "gps_altitude": 785.0,
        "gps_satellites": 8,
        "gps_signal_quality": "good",
        "gps_fuel_level": 75.0,
        "gps_engine_status": False,
        "gps_ignition_status": False
    }
]

success_count = 0

for vehicle_data in vehicles_data:
    try:
        vehicle = Vehicle.objects.get(number=vehicle_data["number"])
        vehicle.gps_device_id = vehicle_data["gps_device_id"]
        vehicle.gps_imei = vehicle_data["gps_imei"]
        vehicle.gps_phone = vehicle_data["gps_phone"]
        vehicle.gps_enabled = True
        vehicle.gps_latitude = vehicle_data["gps_latitude"]
        vehicle.gps_longitude = vehicle_data["gps_longitude"]
        vehicle.gps_speed = vehicle_data["gps_speed"]
        vehicle.gps_heading = vehicle_data["gps_heading"]
        vehicle.gps_altitude = vehicle_data["gps_altitude"]
        vehicle.gps_satellites = vehicle_data["gps_satellites"]
        vehicle.gps_signal_quality = vehicle_data["gps_signal_quality"]
        vehicle.gps_fuel_level = vehicle_data["gps_fuel_level"]
        vehicle.gps_engine_status = vehicle_data["gps_engine_status"]
        vehicle.gps_ignition_status = vehicle_data["gps_ignition_status"]
        vehicle.gps_last_update = timezone.now()
        vehicle.save()
        print(f"✅ GPS данные обновлены для {vehicle_data['number']}")
        success_count += 1
    except Vehicle.DoesNotExist:
        print(f"❌ Грузовик {vehicle_data['number']} не найден")
    except Exception as e:
        print(f"❌ Ошибка обновления {vehicle_data['number']}: {e}")

print(f"📊 Результат: {success_count}/{len(vehicles_data)} грузовиков обновлено")
'''
    
    # Сохраняем скрипт во временный файл на сервере
    upload_command = f"cat > /tmp/gps_sync.py << 'EOF'\n{python_script}\nEOF"
    if not run_ssh_command(upload_command):
        print("❌ Не удалось загрузить скрипт на сервер")
        return
    
    # Выполняем скрипт
    execute_command = "source venv/bin/activate && python3 /tmp/gps_sync.py"
    if run_ssh_command(execute_command):
        print("\n✅ GPS трекеры успешно синхронизированы!")
        
        # Перезапускаем сервисы
        print("\n🔄 Перезапуск сервисов...")
        run_ssh_command("sudo systemctl restart barlau.service")
        run_ssh_command("sudo systemctl restart nginx")
        
        print("\n🎉 Синхронизация завершена!")
    else:
        print("\n❌ Ошибка синхронизации GPS трекеров")

if __name__ == "__main__":
    main()
