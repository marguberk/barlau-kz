from django.core.management.base import BaseCommand
from logistics.services.stavtrack_service import StavTrackService
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Синхронизация GPS данных с StavTrack'

    def add_arguments(self, parser):
        parser.add_argument(
            '--device-id',
            type=str,
            help='ID конкретного GPS устройства для синхронизации',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительная синхронизация всех устройств',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Начинаем синхронизацию GPS данных с StavTrack...')
        )
        
        try:
            stavtrack_service = StavTrackService()
            
            if options['device_id']:
                # Синхронизация конкретного устройства
                self.stdout.write(f'Синхронизация устройства {options["device_id"]}...')
                position = stavtrack_service.get_vehicle_position(options['device_id'])
                if position:
                    self.stdout.write(
                        self.style.SUCCESS(f'Позиция устройства {options["device_id"]} получена')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'Не удалось получить позицию устройства {options["device_id"]}')
                    )
            else:
                # Синхронизация всех устройств
                self.stdout.write('Синхронизация всех GPS устройств...')
                success = stavtrack_service.sync_vehicle_positions()
                
                if success:
                    self.stdout.write(
                        self.style.SUCCESS('Синхронизация GPS данных завершена успешно')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR('Ошибка при синхронизации GPS данных')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Исключение при синхронизации: {str(e)}')
            )
            logger.error(f'Ошибка в команде sync_gps_data: {str(e)}')







































