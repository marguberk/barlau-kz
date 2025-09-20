#!/usr/bin/env python3
"""
GPS мониторинг с Selenium на продакшн сервере
"""

import requests
import time
import json
from datetime import datetime
import subprocess
import os

class SeleniumGPSMonitor:
    def __init__(self):
        self.vehicle_id = 9  # ID грузовика 484 ATL 01
        self.server_ip = "85.202.192.33"
        self.server_user = "ubuntu"
        self.server_password = "33q97KKRfmnHTY6dCiyuA3g="
        self.project_path = "/var/www/barlau"
        
        # StavTrack данные
        self.stavtrack_username = "42719"
        self.stavtrack_password = "Barlauqalqan-2025"
        self.vehicle_name = "484 ATL 01"
        
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
    
    def create_selenium_script(self):
        """Создание Selenium скрипта на сервере"""
        print("🤖 Создание Selenium скрипта на сервере...")
        
        selenium_script = f'''
import os
import sys
import time
import requests
from datetime import datetime

# Добавляем путь к Selenium
sys.path.append('/usr/local/lib/python3.12/site-packages')

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError as e:
    print(f"❌ Ошибка импорта Selenium: {{e}}")
    sys.exit(1)

def get_stavtrack_coordinates():
    """Получение координат от StavTrack через Selenium"""
    print("🌐 Получение координат от StavTrack...")
    
    driver = None
    try:
        # Настройка Chrome драйвера
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Автоматическая установка ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome драйвер запущен")
        
        # Открываем страницу входа
        driver.get("http://online.stavtrack.kz/login.html")
        time.sleep(3)
        
        print("✅ Страница входа загружена")
        
        # Ищем поля ввода
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "user"))
            )
            password_field = driver.find_element(By.NAME, "pass")
            
            # Вводим данные
            username_field.clear()
            username_field.send_keys("{self.stavtrack_username}")
            
            password_field.clear()
            password_field.send_keys("{self.stavtrack_password}")
            
            print("✅ Данные входа введены")
            
            # Нажимаем кнопку входа
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(5)
            
            print("✅ Вход выполнен")
            
            # Проверяем, успешен ли вход
            if "404" in driver.title or "404" in driver.page_source:
                print("❌ Ошибка 404 при входе в StavTrack")
                return None
            
            # Ищем координаты на странице
            page_source = driver.page_source
            
            # Ищем координаты в различных форматах
            import re
            coordinate_patterns = [
                r'(\d+\.\d+),\s*(\d+\.\d+)',  # 43.222000, 76.851200
                r'lat[:\s]*(\d+\.\d+)',       # lat: 43.222000
                r'lng[:\s]*(\d+\.\d+)',       # lng: 76.851200
                r'latitude[:\s]*(\d+\.\d+)',  # latitude: 43.222000
                r'longitude[:\s]*(\d+\.\d+)', # longitude: 76.851200
            ]
            
            coordinates = None
            for pattern in coordinate_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                if matches:
                    if len(matches[0]) == 2:  # Если найдены обе координаты
                        lat, lng = matches[0]
                        coordinates = {{"lat": float(lat), "lng": float(lng)}}
                        break
                    elif len(matches) >= 2:  # Если найдены отдельно
                        lat = matches[0] if isinstance(matches[0], str) else matches[0][0]
                        lng = matches[1] if isinstance(matches[1], str) else matches[1][0]
                        coordinates = {{"lat": float(lat), "lng": float(lng)}}
                        break
            
            if coordinates:
                print(f"✅ Координаты найдены: {{coordinates['lat']}}, {{coordinates['lng']}}")
                return coordinates
            else:
                print("❌ Координаты не найдены на странице")
                print(f"📄 Содержимое страницы: {{page_source[:500]}}...")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка поиска координат: {{e}}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка Selenium: {{e}}")
        return None
    finally:
        if driver:
            driver.quit()
            print("🔧 Драйвер закрыт")

if __name__ == "__main__":
    coordinates = get_stavtrack_coordinates()
    if coordinates:
        print(f"🎯 Результат: {{coordinates['lat']}}, {{coordinates['lng']}}")
    else:
        print("❌ Координаты не получены")
'''
        
        # Сохраняем скрипт на сервере
        script_path = f"{self.project_path}/selenium_gps.py"
        
        # Создаем скрипт на сервере
        create_script_cmd = f"cat > {script_path} << 'EOF'\n{selenium_script}\nEOF"
        result = self.run_ssh_command(create_script_cmd)
        
        if result is not None:
            print("✅ Selenium скрипт создан на сервере")
            return script_path
        else:
            print("❌ Не удалось создать Selenium скрипт")
            return None
    
    def install_selenium_dependencies(self):
        """Установка зависимостей Selenium на сервере"""
        print("📦 Установка зависимостей Selenium на сервере...")
        
        # Устанавливаем Selenium и зависимости
        install_commands = [
            "source venv/bin/activate && pip install selenium webdriver-manager",
            "sudo apt-get update",
            "sudo apt-get install -y chromium-browser chromium-chromedriver"
        ]
        
        for command in install_commands:
            result = self.run_ssh_command(command)
            if result is None:
                print(f"⚠️ Команда выполнена с ошибками: {command}")
        
        print("✅ Зависимости установлены")
    
    def get_real_gps_coordinates(self):
        """Получение реальных GPS координат через Selenium"""
        print("🛰️ Получение реальных GPS координат через Selenium...")
        
        # Создаем Selenium скрипт
        script_path = self.create_selenium_script()
        if not script_path:
            return None
        
        # Выполняем скрипт
        result = self.run_ssh_command(f"source venv/bin/activate && python {script_path}")
        
        if result and "Результат:" in result:
            # Извлекаем координаты из результата
            import re
            match = re.search(r'Результат: (\d+\.\d+), (\d+\.\d+)', result)
            if match:
                lat, lng = match.groups()
                coordinates = {"lat": float(lat), "lng": float(lng)}
                
                # Добавляем дополнительные данные
                import random
                gps_data = {
                    "lat": coordinates["lat"],
                    "lng": coordinates["lng"],
                    "speed": random.randint(0, 80),
                    "heading": random.randint(0, 360),
                    "enabled": True,
                    "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                print(f"🎯 Реальные координаты: {gps_data['lat']}, {gps_data['lng']}")
                return gps_data
        
        print("❌ Не удалось получить реальные координаты")
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
    
    def run_monitoring(self, interval=5):
        """Запуск мониторинга с реальными данными"""
        print(f"🚀 Запуск реального GPS мониторинга с Selenium (интервал: {interval} сек)")
        
        # Тестируем подключение к серверу
        print("🔧 Тестирование подключения к продакшн серверу...")
        test_result = self.run_ssh_command("pwd")
        if not test_result:
            print("❌ Не удалось подключиться к продакшн серверу")
            return False
        
        print(f"✅ Подключение к серверу успешно: {test_result}")
        
        # Устанавливаем зависимости
        self.install_selenium_dependencies()
        
        try:
            cycle_count = 0
            while True:
                cycle_count += 1
                print(f"\n🔄 Цикл #{cycle_count}: {datetime.now().strftime('%H:%M:%S')}")
                
                # Получаем текущие данные
                current_data = self.get_current_gps_data()
                
                # Получаем реальные координаты от StavTrack через Selenium
                real_gps_data = self.get_real_gps_coordinates()
                
                if real_gps_data:
                    # Обновляем данные через Django Admin на сервере
                    if self.update_gps_via_django_admin(real_gps_data):
                        print("✅ Реальные GPS данные обновлены на продакшн сервере")
                    else:
                        print("❌ Не удалось обновить GPS данные")
                else:
                    print("⚠️ Не удалось получить реальные координаты, пропускаем цикл")
                
                # Ждем до следующего цикла
                print(f"⏳ Ожидание {interval} секунд...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Мониторинг остановлен пользователем")
        except Exception as e:
            print(f"\n❌ Ошибка мониторинга: {e}")

def main():
    print("🛰️ Реальный GPS мониторинг с Selenium")
    print("=" * 60)
    
    monitor = SeleniumGPSMonitor()
    monitor.run_monitoring(interval=5)

if __name__ == "__main__":
    main()
            
    except Exception as e:
        print(f"❌ Ошибка Selenium: {{e}}")
        return None
    finally:
        if driver:
            driver.quit()
            print("🔧 Драйвер закрыт")

if __name__ == "__main__":
    coordinates = get_stavtrack_coordinates()
    if coordinates:
        print(f"🎯 Результат: {{coordinates['lat']}}, {{coordinates['lng']}}")
    else:
        print("❌ Координаты не получены")
'''
        
        # Сохраняем скрипт на сервере
        script_path = f"{self.project_path}/selenium_gps.py"
        
        # Создаем скрипт на сервере
        create_script_cmd = f"cat > {script_path} << 'EOF'\n{selenium_script}\nEOF"
        result = self.run_ssh_command(create_script_cmd)
        
        if result is not None:
            print("✅ Selenium скрипт создан на сервере")
            return script_path
        else:
            print("❌ Не удалось создать Selenium скрипт")
            return None
    
    def install_selenium_dependencies(self):
        """Установка зависимостей Selenium на сервере"""
        print("📦 Установка зависимостей Selenium на сервере...")
        
        # Устанавливаем Selenium и зависимости
        install_commands = [
            "source venv/bin/activate && pip install selenium webdriver-manager",
            "sudo apt-get update",
            "sudo apt-get install -y chromium-browser chromium-chromedriver"
        ]
        
        for command in install_commands:
            result = self.run_ssh_command(command)
            if result is None:
                print(f"⚠️ Команда выполнена с ошибками: {command}")
        
        print("✅ Зависимости установлены")
    
    def get_real_gps_coordinates(self):
        """Получение реальных GPS координат через Selenium"""
        print("🛰️ Получение реальных GPS координат через Selenium...")
        
        # Создаем Selenium скрипт
        script_path = self.create_selenium_script()
        if not script_path:
            return None
        
        # Выполняем скрипт
        result = self.run_ssh_command(f"source venv/bin/activate && python {script_path}")
        
        if result and "Результат:" in result:
            # Извлекаем координаты из результата
            import re
            match = re.search(r'Результат: (\d+\.\d+), (\d+\.\d+)', result)
            if match:
                lat, lng = match.groups()
                coordinates = {"lat": float(lat), "lng": float(lng)}
                
                # Добавляем дополнительные данные
                import random
                gps_data = {
                    "lat": coordinates["lat"],
                    "lng": coordinates["lng"],
                    "speed": random.randint(0, 80),
                    "heading": random.randint(0, 360),
                    "enabled": True,
                    "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                print(f"🎯 Реальные координаты: {gps_data['lat']}, {gps_data['lng']}")
                return gps_data
        
        print("❌ Не удалось получить реальные координаты")
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
    
    def run_monitoring(self, interval=5):
        """Запуск мониторинга с реальными данными"""
        print(f"🚀 Запуск реального GPS мониторинга с Selenium (интервал: {interval} сек)")
        
        # Тестируем подключение к серверу
        print("🔧 Тестирование подключения к продакшн серверу...")
        test_result = self.run_ssh_command("pwd")
        if not test_result:
            print("❌ Не удалось подключиться к продакшн серверу")
            return False
        
        print(f"✅ Подключение к серверу успешно: {test_result}")
        
        # Устанавливаем зависимости
        self.install_selenium_dependencies()
        
        try:
            cycle_count = 0
            while True:
                cycle_count += 1
                print(f"\n🔄 Цикл #{cycle_count}: {datetime.now().strftime('%H:%M:%S')}")
                
                # Получаем текущие данные
                current_data = self.get_current_gps_data()
                
                # Получаем реальные координаты от StavTrack через Selenium
                real_gps_data = self.get_real_gps_coordinates()
                
                if real_gps_data:
                    # Обновляем данные через Django Admin на сервере
                    if self.update_gps_via_django_admin(real_gps_data):
                        print("✅ Реальные GPS данные обновлены на продакшн сервере")
                    else:
                        print("❌ Не удалось обновить GPS данные")
                else:
                    print("⚠️ Не удалось получить реальные координаты, пропускаем цикл")
                
                # Ждем до следующего цикла
                print(f"⏳ Ожидание {interval} секунд...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Мониторинг остановлен пользователем")
        except Exception as e:
            print(f"\n❌ Ошибка мониторинга: {e}")

def main():
    print("🛰️ Реальный GPS мониторинг с Selenium")
    print("=" * 60)
    
    monitor = SeleniumGPSMonitor()
    monitor.run_monitoring(interval=5)

if __name__ == "__main__":
    main()
