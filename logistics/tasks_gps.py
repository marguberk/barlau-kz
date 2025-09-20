from celery import shared_task
from logistics.services.stavtrack_service import StavTrackService
import logging

logger = logging.getLogger(__name__)

@shared_task
def sync_gps_data_periodic():
    """
    Периодическая синхронизация GPS данных с StavTrack
    Выполняется каждые 5 секунд
    """
    logger.info("🛰️ Запуск периодической синхронизации GPS данных")
    
    try:
        service = StavTrackService()
        success = service.sync_all_vehicles()
        
        if success:
            logger.info("✅ Периодическая синхронизация GPS данных завершена успешно")
            return "success"
        else:
            logger.error("❌ Ошибка периодической синхронизации GPS данных")
            return "error"
            
    except Exception as e:
        logger.error(f"❌ Исключение при периодической синхронизации: {str(e)}")
        return "error"

@shared_task
def sync_vehicle_gps_data(vehicle_number):
    """
    Синхронизация GPS данных для конкретного грузовика
    """
    logger.info(f"🛰️ Синхронизация GPS данных для грузовика: {vehicle_number}")
    
    try:
        service = StavTrackService()
        success = service.sync_vehicle_gps_data(vehicle_number)
        
        if success:
            logger.info(f"✅ GPS данные для {vehicle_number} синхронизированы")
            return "success"
        else:
            logger.error(f"❌ Ошибка синхронизации GPS данных для {vehicle_number}")
            return "error"
            
    except Exception as e:
        logger.error(f"❌ Исключение при синхронизации {vehicle_number}: {str(e)}")
        return "error"
