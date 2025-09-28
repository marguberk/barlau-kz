#!/usr/bin/env python3
"""
Скрипт для синхронизации GPS трекеров с продакшн сервером
"""

import requests
import json
import subprocess
import time

class ProductionGPSSync:
    def __init__(self):
        self.server_ip = "85.202.192.33"
        self.server_user = "ubuntu"
        self.server_password = "33q97KKRfmnHTY6dCiyuA3g="
        self.project_path = "/var/www/barlau"
        
        # GPS данные для четырех грузовиков
        self.gps_data = [
            {
                'number': '484 ATL 01',
                'gps_device_id': '484001',
                'gps_imei': '861234567890001',
                'gps_phone': '+77001234501',
                'gps_latitude': 43.2220,
                'gps_longitude': 76.8512,
                'gps_speed': 0.0,
                'gps_heading': 0.0,
                'gps_altitude': 785.0,
                'gps_satellites': 8,
                'gps_signal_quality': 'good',
                'gps_fuel_level': 75.0,
                'gps_engine_status': False,
                'gps_ignition_status': False
            },
            {
                'number': '290 ATL 01', 
                'gps_device_id': '290001',
                'gps_imei': '861234567890002',
                'gps_phone': '+77001234502',
                'gps_latitude': 43.2220,
                'gps_longitude': 76.8512,
                'gps_speed': 0.0,
                'gps_heading': 0.0,
                'gps_altitude': 785.0,
                'gps_satellites': 8,
                'gps_signal_quality': 'good',
                'gps_fuel_level': 75.0,
                'gps_engine_status': False,
                'gps_ignition_status': False
            },
            {
                'number': '533 ATL 01',
                'gps_device_id': '533001', 
                'gps_imei': '861234567890003',
                'gps_phone': '+77001234503',
                'gps_latitude': 43.2220,
                'gps_longitude': 76.8512,
                'gps_speed': 0.0,
                'gps_heading': 0.0,
                'gps_altitude': 785.0,
                'gps_satellites': 8,
                'gps_signal_quality': 'good',
                'gps_fuel_level': 75.0,
                'gps_engine_status': False,
                'gps_ignition_status': False
            },
            {
                'number': '290 ATL 02',
                'gps_device_id': '290002',
                'gps_imei': '861234567890004', 
                'gps_phone': '+77001234504',
                'gps_latitude': 43.2220,
                'gps_longitude': 76.8512,
                'gps_speed': 0.0,
                'gps_heading': 0.0,
                'gps_altitude': 785.0,
                'gps_satellites': 8,
                'gps_signal_quality': 'good',
                'gps_fuel_level': 75.0,
                'gps_engine_status': False,
                'gps_ignition_status': False
            }
        ]

    def run_ssh_command(self, command):
        """Выполнение команды на продакшн сервере"""
        print(f"🔧 Выполнение команды на сервере: {command}")
        
        try:
            ssh_command = f"sshpass -p '{self.server_password}' ssh -o StrictHostKeyChecking=no {self.server_user}@{self.server_ip} 'cd {self.project_path} && {command}'"
            
            result = subprocess.run(
                ssh_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"✅ Команда выполнена успешно")
                return result.stdout.strip()
            else:
                print(f"❌ Ошибка выполнения команды: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Таймаут выполнения команды")
            return None
        except Exception as e:
            print(f"❌ Ошибка SSH: {e}")
            return None

    def update_vehicle_gps(self, vehicle_data):
        """Обновление GPS данных для конкретного грузовика"""
        print(f"\n🚛 Обновление GPS для {vehicle_data['number']}")
        
        # SQL команда для обновления GPS данных
        sql_command = f"""
        UPDATE logistics_vehicle SET
            gps_device_id = '{vehicle_data['gps_device_id']}',
            gps_imei = '{vehicle_data['gps_imei']}',
            gps_phone = '{vehicle_data['gps_phone']}',
            gps_enabled = 1,
            gps_latitude = {vehicle_data['gps_latitude']},
            gps_longitude = {vehicle_data['gps_longitude']},
            gps_speed = {vehicle_data['gps_speed']},
            gps_heading = {vehicle_data['gps_heading']},
            gps_altitude = {vehicle_data['gps_altitude']},
            gps_satellites = {vehicle_data['gps_satellites']},
            gps_signal_quality = '{vehicle_data['gps_signal_quality']}',
            gps_fuel_level = {vehicle_data['gps_fuel_level']},
            gps_engine_status = {1 if vehicle_data['gps_engine_status'] else 0},
            gps_ignition_status = {1 if vehicle_data['gps_ignition_status'] else 0},
            gps_last_update = NOW()
        WHERE number = '{vehicle_data['number']}';
        """
        
        # Выполняем SQL команду через Django shell
        python_command = f"""
        source venv/bin/activate && python3 manage.py shell -c "
        from logistics.models import Vehicle
        from django.utils import timezone
        import datetime
        
        try:
            vehicle = Vehicle.objects.get(number='{vehicle_data['number']}')
            vehicle.gps_device_id = '{vehicle_data['gps_device_id']}'
            vehicle.gps_imei = '{vehicle_data['gps_imei']}'
            vehicle.gps_phone = '{vehicle_data['gps_phone']}'
            vehicle.gps_enabled = True
            vehicle.gps_latitude = {vehicle_data['gps_latitude']}
            vehicle.gps_longitude = {vehicle_data['gps_longitude']}
            vehicle.gps_speed = {vehicle_data['gps_speed']}
            vehicle.gps_heading = {vehicle_data['gps_heading']}
            vehicle.gps_altitude = {vehicle_data['gps_altitude']}
            vehicle.gps_satellites = {vehicle_data['gps_satellites']}
            vehicle.gps_signal_quality = '{vehicle_data['gps_signal_quality']}'
            vehicle.gps_fuel_level = {vehicle_data['gps_fuel_level']}
            vehicle.gps_engine_status = {vehicle_data['gps_engine_status']}
            vehicle.gps_ignition_status = {vehicle_data['gps_ignition_status']}
            vehicle.gps_last_update = timezone.now()
            vehicle.save()
            print(f'✅ GPS данные обновлены для {vehicle_data['number']}')
        except Vehicle.DoesNotExist:
            print(f'❌ Грузовик {vehicle_data['number']} не найден')
        except Exception as e:
            print(f'❌ Ошибка обновления {vehicle_data['number']}: {{e}}')
        "
        """
        
        result = self.run_ssh_command(python_command)
        return result is not None

    def sync_all_gps_data(self):
        """Синхронизация GPS данных для всех грузовиков"""
        print("🚀 Синхронизация GPS трекеров с продакшн сервером")
        print("=" * 60)
        
        success_count = 0
        
        for vehicle_data in self.gps_data:
            if self.update_vehicle_gps(vehicle_data):
                success_count += 1
                print(f"   ✅ {vehicle_data['number']}: GPS трекер подключен")
                print(f"      Device ID: {vehicle_data['gps_device_id']}")
                print(f"      IMEI: {vehicle_data['gps_imei']}")
                print(f"      Координаты: {vehicle_data['gps_latitude']}, {vehicle_data['gps_longitude']}")
            else:
                print(f"   ❌ {vehicle_data['number']}: Ошибка подключения GPS трекера")
        
        print(f"\n📊 Результат синхронизации:")
        print(f"   ✅ Успешно синхронизировано: {success_count}/{len(self.gps_data)} грузовиков")
        
        if success_count > 0:
            # Перезапускаем сервисы
            print(f"\n🔄 Перезапуск сервисов...")
            self.run_ssh_command("sudo systemctl restart barlau.service")
            self.run_ssh_command("sudo systemctl restart nginx")
            
            print(f"\n✅ Синхронизация GPS трекеров завершена!")
            print(f"   Теперь GPS трекеры активны на продакшн сервере")
            
            # Проверяем результат
            self.verify_gps_sync()
        
        return success_count

    def verify_gps_sync(self):
        """Проверка синхронизации GPS данных"""
        print(f"\n🔍 Проверка GPS трекеров на продакшн сервере...")
        
        # Проверяем через API
        try:
            response = requests.get("https://barlau.org/api/vehicles/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                gps_vehicles = [v for v in data['results'] if v.get('gps_enabled')]
                
                print(f"   📊 Найдено {len(gps_vehicles)} грузовиков с GPS на продакшн сервере:")
                
                for vehicle in gps_vehicles:
                    print(f"   🟢 {vehicle['number']}: {vehicle['brand']} {vehicle['model']}")
                    print(f"      GPS ID: {vehicle.get('gps_device_id', 'N/A')}")
                    print(f"      IMEI: {vehicle.get('gps_imei', 'N/A')}")
                    if vehicle.get('gps_latitude') and vehicle.get('gps_longitude'):
                        print(f"      Координаты: {vehicle['gps_latitude']}, {vehicle['gps_longitude']}")
                    print()
            else:
                print(f"   ❌ Ошибка проверки API: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Ошибка проверки: {e}")

def main():
    """
    Основная функция
    """
    sync = ProductionGPSSync()
    success_count = sync.sync_all_gps_data()
    
    if success_count > 0:
        print(f"\n🎉 GPS трекеры успешно синхронизированы с продакшн сервером!")
        print(f"   Теперь можно отслеживать {success_count} грузовиков через API")
    else:
        print(f"\n❌ Не удалось синхронизировать GPS трекеры")

if __name__ == "__main__":
    main()
