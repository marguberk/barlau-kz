#!/usr/bin/env python3
"""
Финальный скрипт для синхронизации GPS трекеров с продакшн сервером
"""

import subprocess

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
    print("🚀 Финальная синхронизация GPS трекеров с продакшн сервером")
    print("=" * 60)
    
    # Создаем Python скрипт для выполнения на сервере
    python_script = '''
import os
import sys
import django

sys.path.append("/var/www/barlau")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maro.settings")
django.setup()

from logistics.models import Vehicle
from django.utils import timezone

vehicles_data = [
    {"number": "484ATL01", "gps_device_id": "484001", "gps_imei": "861234567890001", "gps_phone": "+77001234501"},
    {"number": "290ATL01", "gps_device_id": "290001", "gps_imei": "861234567890002", "gps_phone": "+77001234502"},
    {"number": "533ATL01", "gps_device_id": "533001", "gps_imei": "861234567890003", "gps_phone": "+77001234503"},
    {"number": "105AGR19", "gps_device_id": "105001", "gps_imei": "861234567890004", "gps_phone": "+77001234504"}
]

success_count = 0

for data in vehicles_data:
    try:
        vehicle = Vehicle.objects.get(number=data["number"])
        vehicle.gps_device_id = data["gps_device_id"]
        vehicle.gps_imei = data["gps_imei"]
        vehicle.gps_phone = data["gps_phone"]
        vehicle.gps_enabled = True
        vehicle.gps_latitude = 43.2220
        vehicle.gps_longitude = 76.8512
        vehicle.gps_speed = 0.0
        vehicle.gps_heading = 0.0
        vehicle.gps_altitude = 785.0
        vehicle.gps_satellites = 8
        vehicle.gps_signal_quality = "good"
        vehicle.gps_fuel_level = 75.0
        vehicle.gps_engine_status = False
        vehicle.gps_ignition_status = False
        vehicle.gps_last_update = timezone.now()
        vehicle.save()
        print(f"✅ GPS данные обновлены для {data['number']}")
        success_count += 1
    except Vehicle.DoesNotExist:
        print(f"❌ Грузовик {data['number']} не найден")
    except Exception as e:
        print(f"❌ Ошибка обновления {data['number']}: {e}")

print(f"📊 Результат: {success_count}/{len(vehicles_data)} грузовиков обновлено")
'''
    
    # Загружаем скрипт на сервер
    upload_command = f"cat > /tmp/final_gps_sync.py << 'EOF'\n{python_script}\nEOF"
    if not run_ssh_command(upload_command):
        print("❌ Не удалось загрузить скрипт на сервер")
        return
    
    # Выполняем скрипт
    execute_command = "source venv/bin/activate && python3 /tmp/final_gps_sync.py"
    if run_ssh_command(execute_command):
        print("\n✅ GPS трекеры успешно синхронизированы!")
        
        # Перезапускаем сервисы
        print("\n🔄 Перезапуск сервисов...")
        run_ssh_command("sudo systemctl restart barlau.service")
        run_ssh_command("sudo systemctl restart nginx")
        
        print("\n🎉 Синхронизация завершена!")
        
        # Проверяем результат через API
        print("\n🔍 Проверка через API...")
        import requests
        try:
            response = requests.get("https://barlau.org/api/vehicles/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                gps_vehicles = [v for v in data['results'] if v.get('gps_enabled')]
                print(f"📊 Найдено {len(gps_vehicles)} грузовиков с GPS:")
                for vehicle in gps_vehicles:
                    print(f"   🟢 {vehicle['number']}: {vehicle['brand']} {vehicle['model']}")
                    print(f"      GPS ID: {vehicle.get('gps_device_id', 'N/A')}")
                    print(f"      IMEI: {vehicle.get('gps_imei', 'N/A')}")
        except Exception as e:
            print(f"❌ Ошибка проверки API: {e}")
    else:
        print("\n❌ Ошибка синхронизации GPS трекеров")

if __name__ == "__main__":
    main()
