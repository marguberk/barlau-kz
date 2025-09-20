#!/usr/bin/env python3
"""
Простое тестирование GPS мониторинга
"""

import requests
import time
import webbrowser
import os

def test_gps_api():
    """Тестирование GPS API"""
    
    print("🛰️ Тестирование GPS API")
    print("=" * 50)
    
    try:
        response = requests.get("https://barlau.org/api/vehicles/9/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API работает!")
            print(f"📍 Координаты: {data.get('gps_latitude')}, {data.get('gps_longitude')}")
            print(f"🛰️ GPS enabled: {data.get('gps_enabled')}")
            print(f"📱 Device ID: {data.get('gps_device_id')}")
            return True
        else:
            print(f"❌ API не работает: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def create_simple_gps_page():
    """Создание простой GPS страницы"""
    
    print("\n📄 Создание простой GPS страницы...")
    
    # Создаем простую HTML страницу
    html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛰️ GPS Мониторинг - 484 ATL 01</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            color: #333;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .coordinates {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            text-align: center;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .coordinates h2 {
            font-size: 1.8rem;
            margin-bottom: 15px;
        }
        .coords {
            font-size: 1.5rem;
            font-weight: bold;
            font-family: monospace;
        }
        .status {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-top: 15px;
        }
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #10b981;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .info-item {
            background: #f8fafc;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #3b82f6;
        }
        .info-item h3 {
            color: #1e40af;
            margin-bottom: 5px;
            font-size: 0.9rem;
        }
        .info-item .value {
            font-size: 1.2rem;
            font-weight: bold;
            color: #1f2937;
        }
        .controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 20px 0;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: #3b82f6;
            color: white;
        }
        .btn-primary:hover {
            background: #2563eb;
        }
        .btn-success {
            background: #10b981;
            color: white;
        }
        .btn-success:hover {
            background: #059669;
        }
        .btn-danger {
            background: #ef4444;
            color: white;
        }
        .btn-danger:hover {
            background: #dc2626;
        }
        .log {
            background: #1f2937;
            color: #f9fafb;
            padding: 15px;
            border-radius: 10px;
            font-family: monospace;
            font-size: 0.9rem;
            max-height: 200px;
            overflow-y: auto;
        }
        .log-entry {
            margin-bottom: 3px;
            padding: 2px 0;
        }
        .timestamp {
            color: #6b7280;
        }
        .success { color: #34d399; }
        .error { color: #f87171; }
        .warning { color: #fbbf24; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛰️ GPS Мониторинг</h1>
            <p>Грузовик 484 ATL 01 - Обновление каждые 5 секунд</p>
        </div>
        
        <div class="coordinates">
            <h2>📍 Текущие координаты</h2>
            <div class="coords" id="coordinates">Загрузка...</div>
            <div class="status">
                <div class="status-dot" id="statusDot"></div>
                <span id="statusText">Подключение...</span>
            </div>
        </div>
        
        <div class="info-grid">
            <div class="info-item">
                <h3>🚛 Грузовик</h3>
                <div class="value">484 ATL 01</div>
            </div>
            <div class="info-item">
                <h3>📱 Device ID</h3>
                <div class="value" id="deviceId">-</div>
            </div>
            <div class="info-item">
                <h3>🛰️ GPS Статус</h3>
                <div class="value" id="gpsStatus">-</div>
            </div>
            <div class="info-item">
                <h3>⏰ Обновление</h3>
                <div class="value" id="lastUpdate">-</div>
            </div>
        </div>
        
        <div class="controls">
            <button class="btn btn-primary" onclick="startMonitoring()">▶️ Запустить</button>
            <button class="btn btn-success" onclick="updateOnce()">🔄 Обновить</button>
            <button class="btn btn-danger" onclick="stopMonitoring()">⏹️ Остановить</button>
        </div>
        
        <div class="log" id="log"></div>
    </div>

    <script>
        let monitoringInterval;
        let isMonitoring = false;
        
        function log(message, type = 'info') {
            const logContainer = document.getElementById('log');
            const timestamp = new Date().toLocaleTimeString();
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry ${type}`;
            logEntry.innerHTML = `<span class="timestamp">[${timestamp}]</span> ${message}`;
            logContainer.appendChild(logEntry);
            logContainer.scrollTop = logContainer.scrollHeight;
        }
        
        async function updateGPSData() {
            try {
                log('🔄 Запрос GPS данных...', 'info');
                
                const response = await fetch('https://barlau.org/api/vehicles/9/');
                const data = await response.json();
                
                if (response.ok) {
                    const lat = data.gps_latitude;
                    const lng = data.gps_longitude;
                    
                    if (lat && lng) {
                        document.getElementById('coordinates').textContent = `${lat}, ${lng}`;
                        document.getElementById('deviceId').textContent = data.gps_device_id || '-';
                        document.getElementById('gpsStatus').textContent = data.gps_enabled ? '✅ Включен' : '❌ Выключен';
                        document.getElementById('lastUpdate').textContent = data.gps_last_update || 'Не обновлялось';
                        
                        document.getElementById('statusDot').style.background = '#10b981';
                        document.getElementById('statusText').textContent = '✅ Данные получены';
                        
                        log(`✅ GPS данные: ${lat}, ${lng}`, 'success');
                    } else {
                        document.getElementById('coordinates').textContent = 'Координаты не найдены';
                        document.getElementById('statusDot').style.background = '#fbbf24';
                        document.getElementById('statusText').textContent = '⚠️ Нет координат';
                        
                        log('⚠️ GPS координаты не найдены', 'warning');
                    }
                } else {
                    throw new Error(`HTTP ${response.status}`);
                }
                
            } catch (error) {
                log(`❌ Ошибка: ${error.message}`, 'error');
                document.getElementById('statusDot').style.background = '#ef4444';
                document.getElementById('statusText').textContent = '❌ Ошибка подключения';
            }
        }
        
        function startMonitoring() {
            if (isMonitoring) return;
            
            isMonitoring = true;
            log('▶️ Запуск мониторинга каждые 5 секунд', 'success');
            
            updateGPSData();
            monitoringInterval = setInterval(updateGPSData, 5000);
        }
        
        function stopMonitoring() {
            if (!isMonitoring) return;
            
            isMonitoring = false;
            clearInterval(monitoringInterval);
            log('⏹️ Мониторинг остановлен', 'warning');
            
            document.getElementById('statusDot').style.background = '#6b7280';
            document.getElementById('statusText').textContent = '⏹️ Остановлено';
        }
        
        function updateOnce() {
            log('🔄 Однократное обновление', 'info');
            updateGPSData();
        }
        
        // Автозапуск при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            log('🚀 GPS мониторинг загружен', 'success');
            setTimeout(() => {
                startMonitoring();
            }, 1000);
        });
        
        window.addEventListener('beforeunload', function() {
            if (isMonitoring) {
                stopMonitoring();
            }
        });
    </script>
</body>
</html>
"""
    
    # Сохраняем файл
    with open('gps_monitor_simple.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Простая GPS страница создана: gps_monitor_simple.html")
    return True

def open_gps_page():
    """Открытие GPS страницы"""
    
    print("\n🌐 Открытие GPS страницы...")
    
    # Получаем абсолютный путь к файлу
    file_path = os.path.abspath('gps_monitor_simple.html')
    file_url = f"file://{file_path}"
    
    try:
        webbrowser.open(file_url)
        print(f"✅ GPS страница открыта: {file_url}")
        return True
    except Exception as e:
        print(f"❌ Ошибка открытия: {e}")
        return False

def monitor_gps_updates():
    """Мониторинг обновлений GPS"""
    
    print("\n🔄 Мониторинг GPS обновлений...")
    print("=" * 50)
    
    previous_coordinates = None
    update_count = 0
    
    try:
        while True:
            try:
                response = requests.get("https://barlau.org/api/vehicles/9/", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    current_coordinates = (data.get('gps_latitude'), data.get('gps_longitude'))
                    last_update = data.get('gps_last_update')
                    
                    print(f"🔄 Проверка {update_count + 1}: {time.strftime('%H:%M:%S')}")
                    print(f"   📍 Координаты: {current_coordinates}")
                    print(f"   🕐 Обновление: {last_update}")
                    
                    if previous_coordinates and current_coordinates != previous_coordinates:
                        print(f"   ✅ Координаты изменились!")
                        print(f"   📊 Было: {previous_coordinates}")
                        print(f"   📊 Стало: {current_coordinates}")
                    elif previous_coordinates and current_coordinates == previous_coordinates:
                        print(f"   ⚠️ Координаты не изменились")
                    else:
                        print(f"   📝 Начальные координаты")
                    
                    previous_coordinates = current_coordinates
                    update_count += 1
                    
                else:
                    print(f"❌ Ошибка: {response.status_code}")
                
                print()
                time.sleep(5)
                
            except KeyboardInterrupt:
                print(f"\n🛑 Мониторинг остановлен")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                time.sleep(5)
                
    except KeyboardInterrupt:
        print(f"\n🛑 Мониторинг остановлен")
    
    print(f"\n📊 Статистика:")
    print(f"   Проверок: {update_count}")
    print(f"   Время: {update_count * 5} секунд")

def main():
    print("🛰️ Простое тестирование GPS мониторинга")
    print("=" * 60)
    
    # Тестируем API
    api_working = test_gps_api()
    
    if api_working:
        # Создаем простую страницу
        page_created = create_simple_gps_page()
        
        if page_created:
            # Открываем страницу
            page_opened = open_gps_page()
            
            if page_opened:
                print(f"\n🎉 GPS мониторинг готов!")
                print(f"✅ API работает")
                print(f"✅ Страница создана")
                print(f"✅ Страница открыта")
                print(f"✅ Мониторинг каждые 5 секунд")
                
                # Спрашиваем про мониторинг
                print(f"\n❓ Хотите запустить мониторинг в терминале?")
                print(f"   (Нажмите Enter для запуска, Ctrl+C для остановки)")
                
                try:
                    input()
                    monitor_gps_updates()
                except KeyboardInterrupt:
                    print(f"\n👋 Мониторинг отменен")
            else:
                print(f"\n⚠️ Не удалось открыть страницу")
        else:
            print(f"\n⚠️ Не удалось создать страницу")
    else:
        print(f"\n❌ GPS API не работает")

if __name__ == "__main__":
    main()








































