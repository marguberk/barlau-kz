from django.core.management.base import BaseCommand
from logistics.services.wialon_service import WialonService
from logistics.models import Vehicle
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Синхронизация GPS данных с Wialon API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--vehicle',
            type=str,
            help='Номер конкретного грузовика для синхронизации (например: 484ATL01)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительная синхронизация всех грузовиков',
        )
        parser.add_argument(
            '--list-units',
            action='store_true',
            help='Показать список всех доступных GPS устройств',
        )

    def handle(self, *args, **options):
        wialon_service = WialonService()
        
        try:
            # Авторизация
            if not wialon_service.authenticate():
                self.stdout.write(
                    self.style.ERROR('❌ Ошибка авторизации в Wialon API')
                )
                return
            
            # Показать список устройств
            if options['list_units']:
                self.stdout.write('📡 Получение списка GPS устройств...')
                units = wialon_service.get_units_list()
                if units:
                    self.stdout.write(f'✅ Найдено {len(units)} GPS устройств:')
                    for unit in units:
                        self.stdout.write(f'  • {unit["nm"]} (ID: {unit["id"]})')
                else:
                    self.stdout.write(self.style.WARNING('⚠️ Не удалось получить список устройств'))
                return
            
            # Синхронизация конкретного грузовика
            if options['vehicle']:
                vehicle_number = options['vehicle']
                self.stdout.write(f'🚛 Синхронизация грузовика {vehicle_number}...')
                
                try:
                    vehicle = Vehicle.objects.get(number=vehicle_number)
                except Vehicle.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Грузовик {vehicle_number} не найден в базе данных')
                    )
                    return
                
                if not vehicle.gps_enabled:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️ GPS не включен для грузовика {vehicle_number}')
                    )
                    return
                
                success = wialon_service.update_vehicle_gps_data(vehicle)
                if success:
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ GPS данные обновлены для {vehicle_number}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Ошибка обновления GPS данных для {vehicle_number}')
                    )
            
            # Синхронизация всех грузовиков
            else:
                if options['force']:
                    self.stdout.write('🔄 Принудительная синхронизация всех грузовиков...')
                    vehicles = Vehicle.objects.filter(gps_enabled=True)
                else:
                    self.stdout.write('🔄 Синхронизация грузовиков с GPS...')
                    vehicles = Vehicle.objects.filter(gps_enabled=True)
                
                if not vehicles.exists():
                    self.stdout.write(
                        self.style.WARNING('⚠️ Нет грузовиков с включенным GPS мониторингом')
                    )
                    return
                
                self.stdout.write(f'📊 Найдено {vehicles.count()} грузовиков с GPS')
                
                updated_count = wialon_service.sync_all_vehicles_gps()
                
                if updated_count > 0:
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Синхронизация завершена: обновлено {updated_count} грузовиков')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('⚠️ Не удалось обновить GPS данные ни для одного грузовика')
                    )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка синхронизации: {e}')
            )
            logger.error(f"Ошибка синхронизации GPS: {e}")
        
        finally:
            # Выход из системы
            wialon_service.logout()
