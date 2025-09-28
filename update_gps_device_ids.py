#!/usr/bin/env python3
"""
Скрипт для обновления GPS device_id в базе данных продакшн сервера
"""

import subprocess
import sys

# Соответствие грузовиков и GPS устройств
GPS_MAPPING = {
    '484ATL01': '29603155',  # 484 ATL 01
    '290ATL01': '29682916',  # 355 ATL 01 (используем доступное устройство)
    '533ATL01': '29682864',  # 359 AUL 01 (используем доступное устройство)
    '105AGR19': '29682886',  # 695 BHS 02 (используем доступное устройство)
}

def update_gps_device_ids():
    """Обновляет GPS device_id на продакшн сервере"""
    print("🔄 Обновляем GPS device_id на продакшн сервере...")
    
    # Создаем Python скрипт для выполнения на сервере
    python_script = f"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from logistics.models import Vehicle
from django.utils import timezone

# Соответствие грузовиков и GPS устройств
gps_mapping = {GPS_MAPPING}

print("🔄 Обновляем GPS device_id для грузовиков...")

updated_count = 0
for vehicle_number, device_id in gps_mapping.items():
    try:
        vehicle = Vehicle.objects.get(number=vehicle_number)
        vehicle.gps_device_id = device_id
        vehicle.gps_enabled = True
        vehicle.gps_last_update = timezone.now()
        vehicle.save()
        
        print(f"✅ Обновлен {{vehicle_number}}: GPS device_id = {{device_id}}")
        updated_count += 1
    except Vehicle.DoesNotExist:
        print(f"❌ Грузовик {{vehicle_number}} не найден в базе данных")
    except Exception as e:
        print(f"❌ Ошибка обновления {{vehicle_number}}: {{e}}")

print(f"📊 Обновлено {{updated_count}} грузовиков")
"""
    
    # Загружаем скрипт на сервер и выполняем
    ssh_command = f"""
cd /var/www/barlau && python3 manage.py shell << 'EOF'
{python_script}
EOF
"""
    
    print("📤 Выполняем обновление на продакшн сервере...")
    
    try:
        result = subprocess.run([
            'sshpass', '-p', '33q97KKRfmnHTY6dCiyuA3g=',
            'ssh', 'ubuntu@85.202.192.33', ssh_command
        ], capture_output=True, text=True, timeout=60)
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✅ GPS device_id успешно обновлены!")
        else:
            print(f"❌ Ошибка выполнения: {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("❌ Таймаут выполнения команды")
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")

if __name__ == "__main__":
    update_gps_device_ids()
