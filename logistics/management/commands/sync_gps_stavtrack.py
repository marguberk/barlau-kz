from django.core.management.base import BaseCommand
from logistics.services.stavtrack_service import StavTrackService
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Синхронизация GPS данных с StavTrack'

    def add_arguments(self, parser):
        parser.add_argument(
            '--vehicle',
            type=str,
            help='Номер грузовика для синхронизации (по умолчанию: все)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительная синхронизация',
        )

    def handle(self, *args, **options):
        vehicle_number = options.get('vehicle')
        force = options.get('force', False)
        
        self.stdout.write('🛰️ Начало синхронизации GPS данных с StavTrack')
        
        service = StavTrackService()
        
        if vehicle_number:
            self.stdout.write(f'📡 Синхронизация грузовика: {vehicle_number}')
            success = service.sync_vehicle_gps_data(vehicle_number)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ GPS данные для {vehicle_number} успешно синхронизированы')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Ошибка синхронизации GPS данных для {vehicle_number}')
                )
        else:
            self.stdout.write('📡 Синхронизация всех грузовиков')
            success = service.sync_all_vehicles()
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✅ GPS данные успешно синхронизированы')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Ошибка синхронизации GPS данных')
                )
