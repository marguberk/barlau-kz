import requests
import json
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from logistics.models import Vehicle
import time

logger = logging.getLogger(__name__)

class StavTrackService:
    """
    Сервис для автоматической синхронизации GPS данных с StavTrack
    """
    
    def __init__(self):
        self.base_url = "http://online.stavtrack.kz"
        self.username = "42719"
        self.password = "Barlauqalqan-2025"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self._authenticated = False
        self.token = None
    
    def authenticate(self):
        """
        Авторизация в системе StavTrack через Wialon API
        """
        try:
            # Получаем токен авторизации
            auth_url = f"{self.base_url}/wialon/ajax.html"
            auth_data = {
                "svc": "token/login",
                "params": json.dumps({
                    "token": self._get_auth_token()
                })
            }
            
            response = self.session.post(auth_url, data=auth_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('error') == 0:
                    self._authenticated = True
                    self.token = result.get('eid')
                    logger.info("Успешная авторизация в StavTrack")
                    return True
                else:
                    logger.error(f"Ошибка авторизации StavTrack: {result.get('error')}")
                    return False
            else:
                logger.error(f"Ошибка HTTP при авторизации StavTrack: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Исключение при авторизации StavTrack: {str(e)}")
            return False
    
    def _get_auth_token(self):
        """
        Получение токена авторизации (нужно реализовать)
        """
        # TODO: Реализовать получение токена через OAuth или другой метод
        return "temp_token"
    
    def get_vehicle_positions(self):
        """
        Получение позиций всех транспортных средств
        """
        if not self._authenticated:
            if not self.authenticate():
                return []
        
        try:
            url = f"{self.base_url}/wialon/ajax.html"
            data = {
                "svc": "core/search_items",
                "params": json.dumps({
                    "spec": {
                        "itemsType": "avl_unit",
                        "propName": "sys_name",
                        "propValueMask": "*",
                        "sortType": "sys_name"
                    },
                    "force": 1,
                    "flags": 1,
                    "from": 0,
                    "to": 0
                })
            }
            
            response = self.session.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('error') == 0:
                    units = result.get('items', [])
                    logger.info(f"Получено {len(units)} единиц из StavTrack")
                    return units
                else:
                    logger.error(f"Ошибка получения единиц: {result.get('error')}")
                    return []
            else:
                logger.error(f"Ошибка HTTP при получении единиц: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Исключение при получении позиций: {str(e)}")
            return []
    
    def get_unit_position(self, unit_id):
        """
        Получение позиции конкретной единицы
        """
        if not self._authenticated:
            if not self.authenticate():
                return None
        
        try:
            url = f"{self.base_url}/wialon/ajax.html"
            data = {
                "svc": "core/get_units_info",
                "params": json.dumps({
                    "unitIds": [unit_id],
                    "flags": 0x1 | 0x2 | 0x4 | 0x8 | 0x10 | 0x20 | 0x40 | 0x80 | 0x100 | 0x200 | 0x400 | 0x800 | 0x1000 | 0x2000 | 0x4000 | 0x8000 | 0x10000 | 0x20000 | 0x40000 | 0x80000 | 0x100000 | 0x200000 | 0x400000 | 0x800000 | 0x1000000 | 0x2000000 | 0x4000000 | 0x8000000 | 0x10000000 | 0x20000000 | 0x40000000 | 0x80000000
                })
            }
            
            response = self.session.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('error') == 0:
                    units = result.get('units', [])
                    if units:
                        return units[0]
                else:
                    logger.error(f"Ошибка получения позиции единицы: {result.get('error')}")
            else:
                logger.error(f"Ошибка HTTP при получении позиции: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Исключение при получении позиции единицы: {str(e)}")
        
        return None
    
    def find_vehicle_484(self, units):
        """
        Поиск грузовика 484 ATL 01 среди единиц
        """
        search_terms = ["484 ATL 01", "484ATL01", "484_ATL_01", "484", "ATL01"]
        
        for unit in units:
            unit_name = unit.get('nm', '')
            for term in search_terms:
                if term.lower() in unit_name.lower():
                    logger.info(f"Найден грузовик 484 ATL 01: {unit_name} (ID: {unit.get('id')})")
                    return unit
        
        logger.warning("Грузовик 484 ATL 01 не найден в StavTrack")
        return None
    
    def sync_vehicle_gps_data(self, vehicle_number="484 ATL 01"):
        """
        Синхронизация GPS данных для конкретного грузовика
        """
        try:
            # Получаем список единиц
            units = self.get_vehicle_positions()
            if not units:
                logger.error("Не удалось получить список единиц из StavTrack")
                return False
            
            # Ищем наш грузовик
            vehicle_unit = self.find_vehicle_484(units)
            if not vehicle_unit:
                logger.error(f"Грузовик {vehicle_number} не найден в StavTrack")
                return False
            
            # Получаем позицию грузовика
            position = self.get_unit_position(vehicle_unit['id'])
            if not position:
                logger.error(f"Не удалось получить позицию грузовика {vehicle_number}")
                return False
            
            # Обновляем GPS данные в Django
            return self._update_django_vehicle(vehicle_number, position)
            
        except Exception as e:
            logger.error(f"Ошибка синхронизации GPS данных: {str(e)}")
            return False
    
    def _update_django_vehicle(self, vehicle_number, position_data):
        """
        Обновление GPS данных в Django модели
        """
        try:
            vehicle = Vehicle.objects.get(number=vehicle_number)
            
            # Извлекаем GPS данные из позиции
            pos = position_data.get('pos', {})
            
            # Обновляем GPS поля
            vehicle.gps_enabled = True
            vehicle.gps_device_id = str(position_data.get('id', ''))
            vehicle.gps_latitude = pos.get('y')
            vehicle.gps_longitude = pos.get('x')
            vehicle.gps_speed = pos.get('s', 0.0)
            vehicle.gps_heading = pos.get('c', 0.0)
            vehicle.gps_altitude = pos.get('z', 0.0)
            vehicle.gps_last_update = timezone.now()
            
            # Дополнительные данные (если доступны)
            vehicle.gps_satellites = pos.get('sat', 0)
            vehicle.gps_signal_quality = "good" if pos.get('sat', 0) > 3 else "poor"
            
            vehicle.save()
            
            logger.info(f"GPS данные для {vehicle_number} успешно обновлены")
            logger.info(f"Координаты: {vehicle.gps_latitude}, {vehicle.gps_longitude}")
            logger.info(f"Скорость: {vehicle.gps_speed} км/ч")
            
            return True
            
        except Vehicle.DoesNotExist:
            logger.error(f"Грузовик {vehicle_number} не найден в Django")
            return False
        except Exception as e:
            logger.error(f"Ошибка обновления Django модели: {str(e)}")
            return False
    
    def sync_all_vehicles(self):
        """
        Синхронизация GPS данных для всех грузовиков
        """
        logger.info("Начало синхронизации GPS данных для всех грузовиков")
        
        # Список грузовиков для синхронизации
        vehicles_to_sync = ["484 ATL 01"]
        
        success_count = 0
        for vehicle_number in vehicles_to_sync:
            if self.sync_vehicle_gps_data(vehicle_number):
                success_count += 1
        
        logger.info(f"Синхронизация завершена: {success_count}/{len(vehicles_to_sync)} грузовиков")
        return success_count > 0








































