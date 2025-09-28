import requests
import json
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from logistics.models import Vehicle
import time

logger = logging.getLogger(__name__)

class WialonService:
    """
    Сервис для автоматической синхронизации GPS данных с Wialon API
    """
    
    def __init__(self):
        self.base_url = "https://hst-api.wialon.com"
        self.access_token = "84582de9332f6d15227795a639a37d94DD3C6E56E170623AAC680089A097C9D1CBD30C52"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'BARLAU-GPS-SYNC/1.0'
        })
        self._authenticated = False
    
    def authenticate(self):
        """
        Авторизация в системе Wialon через токен доступа
        """
        try:
            # Проверяем токен
            auth_url = f"{self.base_url}/wialon/ajax.html"
            params = {
                'svc': 'token/login',
                'params': json.dumps({
                    'token': self.access_token
                }),
                'sid': ''  # Пустой SID для начала
            }
            
            response = self.session.get(auth_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if isinstance(data, dict) and 'eid' in data:
                self.sid = data['eid']  # Сохраняем SID для последующих запросов
                self._authenticated = True
                logger.info("✅ Успешная авторизация в Wialon API")
                return True
            elif isinstance(data, list) and len(data) > 0 and 'error' not in data[0]:
                self.sid = data[0]['eid']  # Сохраняем SID для последующих запросов
                self._authenticated = True
                logger.info("✅ Успешная авторизация в Wialon API")
                return True
            else:
                error_msg = data.get('error', 'Неизвестная ошибка') if isinstance(data, dict) else (data[0].get('error', 'Неизвестная ошибка') if isinstance(data, list) and len(data) > 0 else 'Ошибка авторизации')
                logger.error(f"❌ Ошибка авторизации в Wialon: {error_msg}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к Wialon API: {e}")
            return False
    
    def get_units_list(self):
        """
        Получение списка всех GPS устройств (единиц)
        """
        if not self._authenticated:
            if not self.authenticate():
                return None
        
        try:
            units_url = f"{self.base_url}/wialon/ajax.html"
            params = {
                'svc': 'core/search_items',
                'params': json.dumps({
                    'spec': {
                        'itemsType': 'avl_unit',
                        'propName': 'sys_name',
                        'propValueMask': '*',
                        'sortType': 'sys_name'
                    },
                    'force': 1,
                    'flags': 1,
                    'from': 0,
                    'to': 0
                }),
                'sid': self.sid
            }
            
            response = self.session.get(units_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if isinstance(data, dict) and 'items' in data:
                units = data['items']
                logger.info(f"✅ Получен список GPS устройств: {len(units)} единиц")
                return units
            elif isinstance(data, list) and len(data) > 0 and 'error' not in data[0]:
                units = data[0]['items']
                logger.info(f"✅ Получен список GPS устройств: {len(units)} единиц")
                return units
            else:
                error_msg = data.get('error', 'Неизвестная ошибка') if isinstance(data, dict) else (data[0].get('error', 'Неизвестная ошибка') if isinstance(data, list) and len(data) > 0 else 'Ошибка получения списка устройств')
                logger.error(f"❌ Ошибка получения списка устройств: {error_msg}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения списка устройств: {e}")
            return None
    
    def find_vehicle_unit(self, vehicle_number):
        """
        Поиск GPS устройства по номеру грузовика
        """
        units = self.get_units_list()
        if not units:
            return None
        
        # Маппинг номеров грузовиков на GPS устройства
        vehicle_mapping = {
            '484ATL01': '484 ATL 01',
            '290ATL01': '355 ATL 01',  # Используем доступное устройство
            '533ATL01': '359 AUL 01',  # Используем доступное устройство
            '105AGR19': '695 BHS 02',  # Используем доступное устройство
        }
        
        # Ищем устройство по маппингу
        if vehicle_number in vehicle_mapping:
            target_name = vehicle_mapping[vehicle_number]
            for unit in units:
                if unit.get('nm', '') == target_name:
                    logger.info(f"✅ Найдено GPS устройство для {vehicle_number}: {unit['nm']} (ID: {unit['id']})")
                    return unit
        
        # Fallback: поиск по номеру грузовика в разных форматах
        search_patterns = [
            vehicle_number,
            vehicle_number.replace(' ', ''),
            vehicle_number.replace(' ', '-'),
            vehicle_number.lower(),
            vehicle_number.upper()
        ]
        
        for unit in units:
            unit_name = unit.get('nm', '').lower()
            for pattern in search_patterns:
                if pattern.lower() in unit_name or unit_name in pattern.lower():
                    logger.info(f"✅ Найдено GPS устройство для {vehicle_number}: {unit['nm']} (ID: {unit['id']})")
                    return unit
        
        logger.warning(f"⚠️ GPS устройство для грузовика {vehicle_number} не найдено")
        return None
    
    def get_unit_position(self, unit_id):
        """
        Получение текущей позиции GPS устройства
        """
        if not self._authenticated:
            if not self.authenticate():
                return None
        
        try:
            position_url = f"{self.base_url}/wialon/ajax.html"
            params = {
                'svc': 'core/search_item',
                'params': json.dumps({
                    'id': unit_id,
                    'flags': 0x1  # Флаг для получения позиции
                }),
                'sid': self.sid
            }
            
            response = self.session.get(position_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Position API response for {unit_id}: {data}")
            
            if isinstance(data, dict) and 'item' in data:
                unit_data = data['item']
                if 'pos' in unit_data:
                    pos = unit_data['pos']
                    position = {
                        'latitude': pos.get('y', 0),
                        'longitude': pos.get('x', 0),
                        'speed': pos.get('s', 0) * 3.6,  # Конвертируем м/с в км/ч
                        'heading': pos.get('c', 0),
                        'altitude': pos.get('z', 0),
                        'satellites': pos.get('sc', 0),
                        'timestamp': pos.get('t', 0)
                    }
                    logger.info(f"✅ Получена позиция для устройства {unit_id}: {position['latitude']}, {position['longitude']}")
                    return position
                else:
                    logger.warning(f"⚠️ Нет данных о позиции для устройства {unit_id}")
                    return None
            elif isinstance(data, list) and len(data) > 0 and 'error' not in data[0]:
                unit_data = data[0]
                if 'pos' in unit_data:
                    pos = unit_data['pos']
                    position = {
                        'latitude': pos.get('y', 0),
                        'longitude': pos.get('x', 0),
                        'speed': pos.get('s', 0) * 3.6,  # Конвертируем м/с в км/ч
                        'heading': pos.get('c', 0),
                        'altitude': pos.get('z', 0),
                        'satellites': pos.get('sc', 0),
                        'timestamp': pos.get('t', 0)
                    }
                    logger.info(f"✅ Получена позиция для устройства {unit_id}: {position['latitude']}, {position['longitude']}")
                    return position
                else:
                    logger.warning(f"⚠️ Нет данных о позиции для устройства {unit_id}")
                    return None
            else:
                error_msg = data.get('error', 'Неизвестная ошибка') if isinstance(data, dict) else (data[0].get('error', 'Неизвестная ошибка') if isinstance(data, list) and len(data) > 0 else 'Ошибка получения позиции')
                logger.error(f"❌ Ошибка получения позиции: {error_msg}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения позиции устройства {unit_id}: {e}")
            return None
    
    def update_vehicle_gps_data(self, vehicle):
        """
        Обновление GPS данных для конкретного грузовика
        """
        try:
            if not vehicle.gps_enabled or not vehicle.gps_device_id:
                logger.warning(f"⚠️ GPS не включен или нет device_id для грузовика {vehicle.number}")
                return False
            
            # Ищем GPS устройство
            unit = self.find_vehicle_unit(vehicle.number)
            if not unit:
                logger.warning(f"⚠️ GPS устройство для грузовика {vehicle.number} не найдено в Wialon")
                return False
            
            # Получаем позицию
            position = self.get_unit_position(unit['id'])
            if not position:
                logger.warning(f"⚠️ Не удалось получить позицию для грузовика {vehicle.number}")
                return False
            
            # Обновляем данные в базе
            vehicle.gps_latitude = str(position['latitude'])
            vehicle.gps_longitude = str(position['longitude'])
            vehicle.gps_speed = str(position['speed'])
            vehicle.gps_heading = str(position['heading'])
            vehicle.gps_altitude = str(position['altitude'])
            vehicle.gps_satellites = position['satellites']
            vehicle.gps_signal_quality = 'good' if position['satellites'] > 4 else 'poor'
            vehicle.gps_last_update = timezone.now()
            
            # Определяем статус двигателя и зажигания по скорости
            speed = float(position['speed'])
            vehicle.gps_engine_status = speed > 1.0  # Двигатель работает если скорость > 1 км/ч
            vehicle.gps_ignition_status = speed > 0.5  # Зажигание включено если скорость > 0.5 км/ч
            
            vehicle.save()
            
            logger.info(f"✅ GPS данные обновлены для грузовика {vehicle.number}: {position['latitude']}, {position['longitude']}, скорость: {speed} км/ч")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка обновления GPS данных для {vehicle.number}: {e}")
            return False
    
    def sync_all_vehicles_gps(self):
        """
        Синхронизация GPS данных для всех грузовиков с включенным GPS
        """
        try:
            vehicles = Vehicle.objects.filter(gps_enabled=True)
            logger.info(f"🔄 Начинаем синхронизацию GPS данных для {vehicles.count()} грузовиков")
            
            updated_count = 0
            for vehicle in vehicles:
                if self.update_vehicle_gps_data(vehicle):
                    updated_count += 1
                    time.sleep(1)  # Пауза между запросами
            
            logger.info(f"✅ Синхронизация завершена: обновлено {updated_count} из {vehicles.count()} грузовиков")
            return updated_count
            
        except Exception as e:
            logger.error(f"❌ Ошибка синхронизации всех GPS данных: {e}")
            return 0
    
    def logout(self):
        """
        Выход из системы Wialon
        """
        if self._authenticated and hasattr(self, 'sid'):
            try:
                logout_url = f"{self.base_url}/wialon/ajax.html"
                params = {
                    'svc': 'core/logout',
                    'sid': self.sid
                }
                
                response = self.session.get(logout_url, params=params, timeout=10)
                logger.info("✅ Успешный выход из Wialon API")
                
            except Exception as e:
                logger.warning(f"⚠️ Ошибка при выходе из Wialon: {e}")
            
            self._authenticated = False
            self.sid = None
