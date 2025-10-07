from django.core.management.base import BaseCommand
from core.models import Notification

class Command(BaseCommand):
    help = 'Удалить все уведомления из базы данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Подтвердить удаление всех уведомлений',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.ERROR('Используйте --confirm для подтверждения удаления')
            )
            return

        total_count = Notification.objects.count()
        self.stdout.write(f'Найдено уведомлений: {total_count}')
        
        if total_count == 0:
            self.stdout.write(self.style.SUCCESS('Уведомлений для удаления не найдено'))
            return

        deleted_count, _ = Notification.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Удалено уведомлений: {deleted_count}')
        )
