from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import logging

from core.signals import check_expiring_documents

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Проверяет истекающие сроки документов транспорта и отправляет уведомления'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Количество дней для проверки истечения (по умолчанию: 30)'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Подробный вывод информации'
        )

    def handle(self, *args, **options):
        if options['verbose']:
            self.stdout.write(
                self.style.SUCCESS('Начинаем проверку истечения сроков документов...')
            )
        
        try:
            # Вызываем функцию из signals.py
            check_expiring_documents()
            
            if options['verbose']:
                self.stdout.write(
                    self.style.SUCCESS('Проверка завершена успешно!')
                )
                
        except Exception as e:
            error_msg = f'Ошибка при проверке документов: {e}'
            logger.error(error_msg)
            self.stdout.write(
                self.style.ERROR(error_msg)
            )
            raise 