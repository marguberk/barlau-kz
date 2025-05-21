from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from logistics.models import VehicleDocument
from core.models import Notification
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Command(BaseCommand):
    help = 'Создаёт уведомления о скором истечении срока действия документов транспорта'

    def handle(self, *args, **options):
        today = timezone.now().date()
        notify_days = [30, 14, 7, 1]
        # Получаем всех директоров, супер-админов и суперпользователей
        recipients = User.objects.filter(is_active=True).filter(
            models.Q(role__in=['DIRECTOR', 'SUPERADMIN']) | models.Q(is_superuser=True)
        ).distinct()
        
        docs = VehicleDocument.objects.filter(expiry_date__isnull=False)
        for doc in docs:
            if not doc.expiry_date:
                continue
            days_left = (doc.expiry_date - today).days
            vehicle = doc.vehicle
            doc_type = dict(VehicleDocument.DOCUMENT_TYPE_CHOICES).get(doc.document_type, doc.document_type)
            self.stdout.write(f"Документ: {doc_type}, авто: {vehicle}, expiry_date: {doc.expiry_date}, days_left: {days_left}")
            if days_left in notify_days:
                for user in recipients:
                    Notification.objects.create(
                        user=user,
                        type=Notification.Type.DOCUMENT,
                        title=f'Скоро истекает срок документа',
                        message=f'У {vehicle.brand} {vehicle.model} ({vehicle.number}) истекает срок: {doc_type} — {doc.expiry_date.strftime("%d.%m.%Y")}',
                        link=f'/trucks/{vehicle.id}/'
                    )
                self.stdout.write(self.style.SUCCESS(f'Уведомления созданы для документа {doc_type} ({vehicle}) — осталось {days_left} дней')) 