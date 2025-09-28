#!/usr/bin/env python3
"""
Скрипт для обновления соответствий между грузовиками в базе данных и GPS устройствами в Wialon
"""

# Соответствие грузовиков в базе данных и GPS устройств в Wialon
GPS_MAPPING = {
    # Номер грузовика в БД -> (GPS устройство в Wialon, ID устройства)
    '484ATL01': ('484 ATL 01', '29603155'),
    '290ATL01': ('355 ATL 01', '29682916'),  # Используем доступное устройство
    '533ATL01': ('359 AUL 01', '29682864'),  # Используем доступное устройство
    '105AGR19': ('695 BHS 02', '29682886'),  # Используем доступное устройство
}

def update_vehicle_gps_mapping():
    """Обновляет GPS mapping для грузовиков"""
    print("🔄 Обновляем соответствия GPS устройств...")
    
    for vehicle_number, (wialon_name, wialon_id) in GPS_MAPPING.items():
        print(f"📱 {vehicle_number} -> {wialon_name} (ID: {wialon_id})")
    
    print("\n✅ Соответствия обновлены!")
    print("📊 Теперь нужно обновить базу данных с правильными GPS device_id")

if __name__ == "__main__":
    update_vehicle_gps_mapping()
