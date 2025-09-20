#!/usr/bin/env python3
"""
GPS мониторинг для продакшн сервера barlau.org
"""

import requests
import time
import json
from datetime import datetime
import subprocess
import os

class ProductionGPSMonitor:
    def __init__(self):
        self.vehicle_id = 9  # ID грузовика 484 ATL 01
        self.server_ip = "85.202.192.33"
        self.server_user = "ubuntu"
        self.server_password = "33q97KKRfmnHTY6dCiyuA3g="
        self.project_path = "/var/www/barlau"
        
    def run_ssh_command(self, command):
        """Выполнение команды на продакшн сервере"""
        print(f"🔧 Выполнение команды на сервере: {command}")
        
        try:
            # Используем sshpass для автоматической передачи пароля
            ssh_command = f"sshpass -p '{self.server_password}' ssh -o StrictHostKeyChecking=no {self.server_user}@{self.server_ip} 'cd {self.project_path} && {command}'"
            
            result = subprocess.run(
                ssh_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
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
    
    def get_current_gps_data(self):
        """Получение текущих GPS данных через API"""
        print("📍 Получение текущих GPS данных...")
        
        try:
            response = requests.get(f"https://barlau.org/api/vehicles/{self.vehicle_id}/")
            
            if response.status_code == 200:
                data = response.json()
                gps_data = {
                    "lat": data.get("gps_latitude"),
                    "lng": data.get("gps_longitude"),
                    "speed": data.get("gps_speed"),
                    "heading": data.get("gps_heading"),
                    "last_update": data.get("gps_last_update"),
                    "enabled": data.get("gps_enabled")
                }
                
                print(f"✅ GPS данные получены: {gps_data}")
                return gps_data
            else:
                print(f"❌ Ошибка получения GPS данных: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка запроса: {e}")
            return None
    
    def update_gps_via_django_admin(self, gps_data):
        """Обновление GPS данных через Django Admin на сервере"""
        print("🔧 Обновление GPS данных через Django Admin...")
        
        # Создаем Python скрипт для обновления данных
        update_script = f'''
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barlau.settings")
django.setup()

from logistics.models import Vehicle

try:
    vehicle = Vehicle.objects.get(id={self.vehicle_id})
    vehicle.gps_latitude = "{gps_data['lat']}"
    vehicle.gps_longitude = "{gps_data['lng']}"
    vehicle.gps_speed = {gps_data['speed'] if gps_data['speed'] else 'None'}
    vehicle.gps_heading = {gps_data['heading'] if gps_data['heading'] else 'None'}
    vehicle.gps_enabled = True
    vehicle.gps_last_update = "{gps_data['last_update']}"
    vehicle.save()
    
    print("✅ GPS данные обновлены успешно")
    print(f"Координаты: {gps_data['lat']}, {gps_data['lng']}")
    
except Exception as e:
    print(f"❌ Ошибка обновления: {{e}}")
'''
        
        # Сохраняем скрипт на сервере
        script_path = f"{self.project_path}/update_gps_temp.py"
        
        # Создаем скрипт на сервере
        create_script_cmd = f"cat > {script_path} << 'EOF'\n{update_script}\nEOF"
        self.run_ssh_command(create_script_cmd)
        
        # Выполняем скрипт через виртуальное окружение
        result = self.run_ssh_command(f"source venv/bin/activate && python {script_path}")
        
        # Удаляем временный скрипт
        self.run_ssh_command(f"rm {script_path}")
        
        return result is not None
    
    def test_stavtrack_connection(self):
        """Тестирование подключения к StavTrack"""
        print("🔍 Тестирование подключения к StavTrack...")
        
        try:
            response = requests.get("http://online.stavtrack.kz/login.html", timeout=10)
            if response.status_code == 200:
                print("✅ StavTrack доступен")
                return True
            else:
                print(f"❌ StavTrack недоступен: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка подключения к StavTrack: {e}")
            return False
    
    def simulate_gps_update(self):
        """Симуляция обновления GPS данных"""
        print("🔄 Симуляция обновления GPS данных...")
        
        import random
        
        # Базовые координаты Алматы
        base_lat = 43.2220
        base_lng = 76.8512
        
        # Добавляем небольшое случайное смещение
        lat = base_lat + random.uniform(-0.01, 0.01)
        lng = base_lng + random.uniform(-0.01, 0.01)
        
        gps_data = {
            "lat": round(lat, 6),
            "lng": round(lng, 6),
            "speed": random.randint(0, 80),
            "heading": random.randint(0, 360),
            "enabled": True,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"🎯 Симулированные координаты: {gps_data['lat']}, {gps_data['lng']}")
        return gps_data
    
    def run_monitoring(self, interval=5, use_simulation=True):
        """Запуск мониторинга"""
        print(f"🚀 Запуск GPS мониторинга на продакшн сервере (интервал: {interval} сек)")
        
        if use_simulation:
            print("🎭 Режим симуляции: будут использоваться тестовые координаты")
        else:
            print("🌐 Режим реальных данных: попытка подключения к StavTrack")
        
        # Тестируем подключение к серверу
        print("🔧 Тестирование подключения к продакшн серверу...")
        test_result = self.run_ssh_command("pwd")
        if not test_result:
            print("❌ Не удалось подключиться к продакшн серверу")
            return False
        
        print(f"✅ Подключение к серверу успешно: {test_result}")
        
        # Тестируем StavTrack
        if not use_simulation:
            stavtrack_ok = self.test_stavtrack_connection()
            if not stavtrack_ok:
                print("⚠️ StavTrack недоступен, переключаемся на симуляцию")
                use_simulation = True
        
        try:
            cycle_count = 0
            while True:
                cycle_count += 1
                print(f"\n🔄 Цикл #{cycle_count}: {datetime.now().strftime('%H:%M:%S')}")
                
                # Получаем текущие данные
                current_data = self.get_current_gps_data()
                
                if use_simulation:
                    # Генерируем новые координаты
                    new_gps_data = self.simulate_gps_update()
                    
                    # Обновляем данные через Django Admin на сервере
                    if self.update_gps_via_django_admin(new_gps_data):
                        print("✅ GPS данные обновлены на продакшн сервере")
                    else:
                        print("❌ Не удалось обновить GPS данные")
                else:
                    # Здесь будет код для получения реальных данных от StavTrack
                    print("🌐 Получение реальных данных от StavTrack...")
                    # TODO: Реализовать получение данных от StavTrack
                
                # Ждем до следующего цикла
                print(f"⏳ Ожидание {interval} секунд...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Мониторинг остановлен пользователем")
        except Exception as e:
            print(f"\n❌ Ошибка мониторинга: {e}")

def main():
    print("🛰️ GPS мониторинг для продакшн сервера barlau.org")
    print("=" * 60)
    
    monitor = ProductionGPSMonitor()
    
    print("Выберите режим:")
    print("1. Симуляция (тестовые координаты)")
    print("2. Реальные данные (StavTrack)")
    
    try:
        choice = input("Введите номер (1 или 2): ").strip()
        
        if choice == "2":
            monitor.run_monitoring(interval=5, use_simulation=False)
        else:
            monitor.run_monitoring(interval=5, use_simulation=True)
            
    except KeyboardInterrupt:
        print("\n👋 До свидания!")

if __name__ == "__main__":
    main()

GPS мониторинг для продакшн сервера barlau.org
"""

import requests
import time
import json
from datetime import datetime
import subprocess
import os

class ProductionGPSMonitor:
    def __init__(self):
        self.vehicle_id = 9  # ID грузовика 484 ATL 01
        self.server_ip = "85.202.192.33"
        self.server_user = "ubuntu"
        self.server_password = "33q97KKRfmnHTY6dCiyuA3g="
        self.project_path = "/var/www/barlau"
        
    def run_ssh_command(self, command):
        """Выполнение команды на продакшн сервере"""
        print(f"🔧 Выполнение команды на сервере: {command}")
        
        try:
            # Используем sshpass для автоматической передачи пароля
            ssh_command = f"sshpass -p '{self.server_password}' ssh -o StrictHostKeyChecking=no {self.server_user}@{self.server_ip} 'cd {self.project_path} && {command}'"
            
            result = subprocess.run(
                ssh_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
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
    
    def get_current_gps_data(self):
        """Получение текущих GPS данных через API"""
        print("📍 Получение текущих GPS данных...")
        
        try:
            response = requests.get(f"https://barlau.org/api/vehicles/{self.vehicle_id}/")
            
            if response.status_code == 200:
                data = response.json()
                gps_data = {
                    "lat": data.get("gps_latitude"),
                    "lng": data.get("gps_longitude"),
                    "speed": data.get("gps_speed"),
                    "heading": data.get("gps_heading"),
                    "last_update": data.get("gps_last_update"),
                    "enabled": data.get("gps_enabled")
                }
                
                print(f"✅ GPS данные получены: {gps_data}")
                return gps_data
            else:
                print(f"❌ Ошибка получения GPS данных: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка запроса: {e}")
            return None
    
    def update_gps_via_django_admin(self, gps_data):
        """Обновление GPS данных через Django Admin на сервере"""
        print("🔧 Обновление GPS данных через Django Admin...")
        
        # Создаем Python скрипт для обновления данных
        update_script = f'''
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barlau.settings")
django.setup()

from logistics.models import Vehicle

try:
    vehicle = Vehicle.objects.get(id={self.vehicle_id})
    vehicle.gps_latitude = "{gps_data['lat']}"
    vehicle.gps_longitude = "{gps_data['lng']}"
    vehicle.gps_speed = {gps_data['speed'] if gps_data['speed'] else 'None'}
    vehicle.gps_heading = {gps_data['heading'] if gps_data['heading'] else 'None'}
    vehicle.gps_enabled = True
    vehicle.gps_last_update = "{gps_data['last_update']}"
    vehicle.save()
    
    print("✅ GPS данные обновлены успешно")
    print(f"Координаты: {gps_data['lat']}, {gps_data['lng']}")
    
except Exception as e:
    print(f"❌ Ошибка обновления: {{e}}")
'''
        
        # Сохраняем скрипт на сервере
        script_path = f"{self.project_path}/update_gps_temp.py"
        
        # Создаем скрипт на сервере
        create_script_cmd = f"cat > {script_path} << 'EOF'\n{update_script}\nEOF"
        self.run_ssh_command(create_script_cmd)
        
        # Выполняем скрипт через виртуальное окружение
        result = self.run_ssh_command(f"source venv/bin/activate && python {script_path}")
        
        # Удаляем временный скрипт
        self.run_ssh_command(f"rm {script_path}")
        
        return result is not None
    
    def test_stavtrack_connection(self):
        """Тестирование подключения к StavTrack"""
        print("🔍 Тестирование подключения к StavTrack...")
        
        try:
            response = requests.get("http://online.stavtrack.kz/login.html", timeout=10)
            if response.status_code == 200:
                print("✅ StavTrack доступен")
                return True
            else:
                print(f"❌ StavTrack недоступен: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка подключения к StavTrack: {e}")
            return False
    
    def simulate_gps_update(self):
        """Симуляция обновления GPS данных"""
        print("🔄 Симуляция обновления GPS данных...")
        
        import random
        
        # Базовые координаты Алматы
        base_lat = 43.2220
        base_lng = 76.8512
        
        # Добавляем небольшое случайное смещение
        lat = base_lat + random.uniform(-0.01, 0.01)
        lng = base_lng + random.uniform(-0.01, 0.01)
        
        gps_data = {
            "lat": round(lat, 6),
            "lng": round(lng, 6),
            "speed": random.randint(0, 80),
            "heading": random.randint(0, 360),
            "enabled": True,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"🎯 Симулированные координаты: {gps_data['lat']}, {gps_data['lng']}")
        return gps_data
    
    def run_monitoring(self, interval=5, use_simulation=True):
        """Запуск мониторинга"""
        print(f"🚀 Запуск GPS мониторинга на продакшн сервере (интервал: {interval} сек)")
        
        if use_simulation:
            print("🎭 Режим симуляции: будут использоваться тестовые координаты")
        else:
            print("🌐 Режим реальных данных: попытка подключения к StavTrack")
        
        # Тестируем подключение к серверу
        print("🔧 Тестирование подключения к продакшн серверу...")
        test_result = self.run_ssh_command("pwd")
        if not test_result:
            print("❌ Не удалось подключиться к продакшн серверу")
            return False
        
        print(f"✅ Подключение к серверу успешно: {test_result}")
        
        # Тестируем StavTrack
        if not use_simulation:
            stavtrack_ok = self.test_stavtrack_connection()
            if not stavtrack_ok:
                print("⚠️ StavTrack недоступен, переключаемся на симуляцию")
                use_simulation = True
        
        try:
            cycle_count = 0
            while True:
                cycle_count += 1
                print(f"\n🔄 Цикл #{cycle_count}: {datetime.now().strftime('%H:%M:%S')}")
                
                # Получаем текущие данные
                current_data = self.get_current_gps_data()
                
                if use_simulation:
                    # Генерируем новые координаты
                    new_gps_data = self.simulate_gps_update()
                    
                    # Обновляем данные через Django Admin на сервере
                    if self.update_gps_via_django_admin(new_gps_data):
                        print("✅ GPS данные обновлены на продакшн сервере")
                    else:
                        print("❌ Не удалось обновить GPS данные")
                else:
                    # Здесь будет код для получения реальных данных от StavTrack
                    print("🌐 Получение реальных данных от StavTrack...")
                    # TODO: Реализовать получение данных от StavTrack
                
                # Ждем до следующего цикла
                print(f"⏳ Ожидание {interval} секунд...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Мониторинг остановлен пользователем")
        except Exception as e:
            print(f"\n❌ Ошибка мониторинга: {e}")

def main():
    print("🛰️ GPS мониторинг для продакшн сервера barlau.org")
    print("=" * 60)
    
    monitor = ProductionGPSMonitor()
    
    print("Выберите режим:")
    print("1. Симуляция (тестовые координаты)")
    print("2. Реальные данные (StavTrack)")
    
    try:
        choice = input("Введите номер (1 или 2): ").strip()
        
        if choice == "2":
            monitor.run_monitoring(interval=5, use_simulation=False)
        else:
            monitor.run_monitoring(interval=5, use_simulation=True)
            
    except KeyboardInterrupt:
        print("\n👋 До свидания!")

if __name__ == "__main__":
    main()






































